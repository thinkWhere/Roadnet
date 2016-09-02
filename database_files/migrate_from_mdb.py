#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from subprocess import CalledProcessError
from textwrap import dedent

try:
    import pyodbc
    from pyspatialite import dbapi2 as db
    from pyspatialite.dbapi2 import OperationalError
except ImportError:
    print('This script requires pyodbc and pyspatialite and must be run from '
          'the 32bit OSGeo4W shell with GDAL installed.')
    sys.exit(1)

import sql_scripts

OUTPUT_DB_PATH = 'roadnet_migrated.sqlite'
INPUT_DB_PATH = 'C:\dev\Roadnet.mdb'


def main():
    if len(sys.argv) < 2:
        raise IOError('Usage: python migrate_from_db.py input_file.mdb')

    input_db_path = sys.argv[1]
    if not os.path.isfile(input_db_path):
        raise IOError('{} is not a file.'.format(input_db_path))
    if not input_db_path.endswith('mdb'):
        raise IOError('{} is not an mdb file.'.format(input_db_path))

    council = None
    if len(sys.argv) > 2:
        council = sys.argv[2]
        custom_councils = ['Clacks', 'Renfrew', 'AyrshireRoads']
        if council not in custom_councils:
            raise IOError('"{}" not in list of councils.\nPossible values: {}'.format(
                council, custom_councils))

    migrator = MdbMigrator()
    migrator.input_db_path = input_db_path

    create_new = True
    if create_new:
        if os.path.exists(OUTPUT_DB_PATH):
            os.remove(OUTPUT_DB_PATH)
        migrator.create_new_spatialite_db()
        migrator.create_roadnet_tables()

    copy_geometry_tables = True
    if copy_geometry_tables:
        migrator.copy_geometry_tables_via_ogr()
        migrator.populate_geometry_tables()
        migrator.fix_rdpoly_nulls()
        migrator.create_spatial_indexes()
        if council:
            migrator.run_custom_sql(council)

    copy_non_geometry_tables = True
    if copy_non_geometry_tables:
        migrator.populate_non_geometry_tables()
        migrator.populate_layer_styles_table()

    migrator.print_tables_not_copied()
    migrator.drop_temporary_tables()


class MdbMigrator(object):
    """
    Handle migration of MS Access *.mdb files to .sqlite for roadNet.
    """
    def __init__(self):
        self.prepare_sql_queries()
        self.prepare_new_col_names()
        self.prepare_custom_sql()
        self.input_db_path = INPUT_DB_PATH
        self.output_db_path = OUTPUT_DB_PATH
        self.mdb_conn = None
        self.mdb_cursor = None
        self.sqlite_conn = None
        self.sqlite_cursor = None

    def create_new_spatialite_db(self):
        """
        Create a new sqlite database with spatialite metadata tables.
        """
        print('Creating empty spatialite database')
        self.open_sqlite_connection_and_cursor()
        self.sqlite_cursor.execute(self.sql_geometry['add_spatial_metadata'])
        self.commit_and_close_sqlite()

    def create_roadnet_tables(self):
        """
        Add the roadNet tables to database with correct structure.
        """
        print('Creating empty roadNet tables')
        self.open_sqlite_connection_and_cursor()

        # Add the empty tables
        for table in self.sql_create.keys():
            self.sqlite_cursor.execute(self.sql_create[table])

        # Add geometry where required
        for table in ['esu', 'rdpoly', 'mcl']:
            key = '{}_add_geometry_column'.format(table)
            self.sqlite_cursor.execute(self.sql_geometry[key])

        self.commit_and_close_sqlite()

    def copy_geometry_tables_via_ogr(self):
        """
        Use ogr2ogr and subprocess to copy tables with geometry to new
        database.
        """
        for table in ('esu', 'rdpoly', 'mcl'):
            print('Copying table {} with ogr2ogr'.format(table))
            try:
                subprocess.check_call(
                    ['ogr2ogr', self.output_db_path, self.input_db_path,
                     table, '-nln', 'tmp_{}'.format(table),
                     '-f', 'Sqlite', '-update', '-append'])
            except CalledProcessError, e:
                print("WARNING: Table {} was not copied".format(table))

    def populate_geometry_tables(self):
        """
        Copy data from the temporary tables to main tables.
        """
        self.open_sqlite_connection_and_cursor()
        self.open_mdb_connection_and_cursor()
        for table in ('esu', 'rdpoly', 'mcl'):
            print("\n--------------------------------------------------")
            print('Updating sqlite table {}'.format(table))
            try:
                self.sqlite_cursor.execute(
                    self.sql_populate_geometry_tables[table])
            except OperationalError, e:
                print("Table structure error: {}".format(e))
                self.print_row_count(table)
                continue
            # Only print if table successfully copied
            self.print_columns_dropped_or_renamed(table)
            self.print_row_count(table)

        self.commit_and_close_mdb()
        self.commit_and_close_sqlite()

    def populate_non_geometry_tables(self):
        """
        Copy data from mdb file into non-geometry tables.
        """
        self.open_mdb_connection_and_cursor()
        self.open_sqlite_connection_and_cursor()

        for table in self.db_tables:
            if table in ('esu', 'rdpoly', 'mcl', 'layer_styles'):
                # Skip tables with geometry
                continue

            print('\nCopying data into table {}'.format(table))
            try:
                self.mdb_cursor.execute(self.sql_get_from_mdb[table])
            except pyodbc.Error, e:
                print('Failed to get data from table {} because:\n{}'.format(
                    table, e))
                continue
            rows = self.mdb_cursor.fetchall()
            rows = self.strip_newlines_from_rows(rows, table)
            self.sqlite_cursor.executemany(
                self.sql_populate_non_geometry_tables[table], rows)

            try:
                self.print_columns_dropped_or_renamed(table)
            except AttributeError, e:
                print("Table {} not found".format(table))

            self.print_row_count(table)

        self.commit_and_close_mdb()
        self.commit_and_close_sqlite()

    def strip_newlines_from_rows(self, rows, table):
        """
        Remove newline characters from text fields within rows of specific
        tables.
        :param rows: All data rows from table
        :param table: Table name (determines columns to check)
        :return: List of modified row objects
        """
        text_column_names = {'tblSTREET': ['description'],
                             'tblSPEC_DES': ['location_text', 'description'],
                             'tblMAINT': ['location_text'],
                             'tblREINS_CAT': ['location_text']}

        # Only process chosen tables
        if table not in text_column_names:
            return rows

        # Create function to check for new lines (and Windows new lines)
        def has_newlines(textstring):
            for newline_char in ['\n', '\r']:
                if textstring.find(newline_char) != -1:
                    return True
            return False

        # Update fields in rows
        for row in rows[:]:
            # Some tables have more than one text column
            for column in text_column_names[table]:
                text = getattr(row, column)
                if isinstance(text, type(None)):
                    # Empty rows are None
                    continue

                if not has_newlines(text):
                    # Row contains no newlines
                    continue

                # Process lines with newlines
                while has_newlines(text):
                    # Fix newlines
                    text = self.fix_newlines(text)

                setattr(row, column, text)
                msg = ("Removed newline from {column} in {table} for USRN: {usrn}\n"
                       "New value: {fixed_text}")
                print(msg.format(column=column, table=table,
                                 usrn=row.usrn, fixed_text=text))

        return rows

    @staticmethod
    def fix_newlines(text):
        """
        Remove newlines (\n, \r) from text string
        :param text: text to remove newlines from
        :return: text without newlines
        """
        # Remove all \r (these are always paired with a \n)
        text = text.replace('\r', '')

        # Replace \n with space, but strip back off if at end
        text = text.replace('\n', ' ').strip()

        # Replace double spaces
        text = text.replace('  ', ' ')
        return text

    def fix_rdpoly_nulls(self):
        """
        Replace different forms of NULL in rdpoly
        """
        print("Replacing empty values with NULLs in rdpoly element and hierarchy")
        self.open_sqlite_connection_and_cursor()
        sql = """
          UPDATE rdpoly SET element = NULL WHERE element IN ('NULL', 'Null', '');
          UPDATE rdpoly SET hierarchy = NULL WHERE hierarchy IN ('NULL', 'Null', '');
          """
        self.sqlite_cursor.executescript(sql)
        self.commit_and_close_sqlite()

    def populate_layer_styles_table(self):
        """
        Populate layer style table.
        """
        print('Adding style definitions to table layer_styles')
        self.open_sqlite_connection_and_cursor()
        self.sqlite_cursor.executescript(sql_scripts.populate_layer_styles)
        self.commit_and_close_sqlite()

    def create_spatial_indexes(self):
        """
        Add spatial indexing to tables.
        """
        self.open_sqlite_connection_and_cursor()
        for table in ('esu', 'rdpoly', 'mcl'):
            print('Adding spatial index to table {}'.format(table))
            self.sqlite_cursor.execute(
                self.sql_create_spatial_indexes[table])
        self.commit_and_close_sqlite()

    def drop_temporary_tables(self):
        """
        Remove temporary tables.
        """
        self.open_sqlite_connection_and_cursor()
        tables = ('tmp_esu', 'tmp_rdpoly', 'tmp_mcl')
        for table in tables:
            self.sqlite_cursor.execute(
                "SELECT DisableSpatialIndex('{}', 'geometry')".format(table))
            self.sqlite_cursor.execute(
                "SELECT DiscardGeometryColumn('{}', 'geometry')".format(table))
            self.sqlite_cursor.execute(
                "DROP TABLE IF EXISTS {};".format(table))
            self.sqlite_cursor.execute(
                "DROP TABLE IF EXISTS idx_{}_GEOMETRY;".format(table))
            self.sqlite_cursor.execute(
                "DROP TABLE IF EXISTS idx_{}_GEOMETRY_node;".format(table))
            self.sqlite_cursor.execute(
                "DROP TABLE IF EXISTS idx_{}_GEOMETRY_parent;".format(table))
            self.sqlite_cursor.execute(
                "DROP TABLE IF EXISTS idx_{}_GEOMETRY_rowid;".format(table))
        self.sqlite_cursor.execute("VACUUM;")
        self.commit_and_close_sqlite()

    def print_tables_not_copied(self):
        """
        Print a list of tables from the .mdb file that were not copied
        over into the SQLite file
        """
        print("\n_________________________")
        print("The following tables were not copied from the .mdb file:")

        mdb_tables = self.list_mdb_tables()
        for table in mdb_tables:
            if table not in self.db_tables:
                print(table)
        print("_________________________")

    def list_mdb_tables(self):
        """
        Get a list of tables present in mdb database.
        :return mdb_tables: list of tables
        """
        self.open_mdb_connection_and_cursor()
        mdb_tables = []
        for row in self.mdb_cursor.tables():
            mdb_tables.append(row.table_name)
        self.commit_and_close_mdb()
        return mdb_tables

    def print_columns_dropped_or_renamed(self, table_name):
        """
        Print a list of columns from mdb database tables that are not
        copied over to the sqlite database.
        :param table_name: Table to compare
        :return unused_columns: List of column names
        """
        mdb_columns = self.list_mdb_table_columns(table_name)
        sqlite_columns = self.list_sqlite_table_columns(table_name)
        lower_sqlite_columns = [col.lower() for col in sqlite_columns]
        try:
            columns_to_rename = self.new_col_names[table_name].keys()
        except KeyError:
            # If table doesn't have anything to rename
            columns_to_rename = []
        unused_columns = []
        renamed_columns = []
        for column in mdb_columns:
            if column.lower() not in lower_sqlite_columns:
                if column in columns_to_rename:
                    renamed_columns.append(column)
                else:
                    unused_columns.append(column)

        if len(unused_columns) > 0:
            print("Table {} should have the following columns:\n{}".format(
                table_name, ', '.join(sqlite_columns)))
            print("The following columns were dropped:")
            print(', '.join(unused_columns))

        if len(renamed_columns) > 0:
            print("The following columns were renamed:")
            for column in renamed_columns:
                print("{} becomes {}".format(
                    column, self.new_col_names[table_name][column]))

    def list_mdb_table_columns(self, table_name):
        """
        Get a list of column names for a table in the mdb database.  A
        connection to the database must already be open
        :param table_name: string name of table to query
        :return columns: list of column names
        """
        query = "SELECT * FROM {}".format(table_name)
        first_row = self.mdb_cursor.execute(query).fetchone()
        columns = zip(*first_row.cursor_description)[0]
        return columns

    def list_sqlite_table_columns(self, table_name):
        """
        Get a list of column names for a table in the sqlite database.  A
        connection to the database must already be open.
        :param table_name: string name of table to query
        :return columns: list of column names
        """
        query = "SELECT * FROM {}".format(table_name)
        cursor = self.sqlite_conn.execute(query)
        columns = zip(*cursor.description)[0]
        return columns

    def open_mdb_connection_and_cursor(self):
        """
        Connect to Access .mdb database.
        """
        connection_string = """
            DRIVER={{Microsoft Access Driver (*.mdb)}};
            DBQ={};""".format(self.input_db_path)
        self.mdb_conn = pyodbc.connect(connection_string)
        self.mdb_cursor = self.mdb_conn.cursor()

    def commit_and_close_mdb(self):
        """
        Commit transaction and close connection to mdb database.
        """
        self.mdb_conn.commit()
        self.mdb_conn.close()
        self.mdb_conn = None
        self.mdb_cursor = None

    def open_sqlite_connection_and_cursor(self):
        """
        Connect to sqlite database.
        """
        self.sqlite_conn = db.connect(self.output_db_path)
        self.sqlite_conn.row_factory = db.Row
        self.sqlite_cursor = self.sqlite_conn.cursor()

    def commit_and_close_sqlite(self):
        """
        Commit transaction and close connection to sqlite database.
        """
        self.sqlite_conn.commit()
        self.sqlite_conn.close()
        self.sqlite_conn = None
        self.sqlite_cursor = None

    def prepare_sql_queries(self):
        """
        Store SQL commands
        """
        self.db_tables = [
            'lnkESU_STREET', 'tblESU', 'tlkpCOUNTY', 'tblGazMetadata',
            'tlkpROAD_STATUS', 'esu', 'tlkpSPEC_DES', 'tlkpSTREET_STATE',
            'tblSPEC_DES', 'layer_styles', 'mcl', 'tlkpWHOLE_ROAD',
            'tblRD_POL', 'tblREINS_CAT', 'tblSTREET', 'tblUsers',
            'tlkpREINS_CAT', 'tlkpTOWN', 'tlkpORG', 'tblMAINT',
            'tlkpSTREET_CLASS', 'tlkpSTREET_REF_TYPE', 'rdpoly',
            'tlkpLOCALITY', 'lnkMAINT_RD_POL', 'tlkpAUTHORITY']

        self.sql_create = {
            'esu': """
                CREATE TABLE IF NOT EXISTS "esu" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "esu_id" INTEGER, "symbol" INTEGER);""",
            'rdpoly': """
                CREATE TABLE IF NOT EXISTS "rdpoly" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "symbol" INTEGER, "rd_pol_id" INTEGER, "element" TEXT,
                    "hierarchy" TEXT, "ref_1" TEXT, "ref_2" INTEGER, "desc_1" TEXT,
                    "desc_2" TEXT, "desc_3" INTEGER, "ref_3" INTEGER,
                    "currency_flag" INTEGER, "part_label" TEXT, "label" TEXT,
                    "label1" TEXT, "feature_length" DOUBLE, "r_usrn" INTEGER,
                    "mcl_cref" INTEGER);""",
            'mcl': """
                CREATE TABLE IF NOT EXISTS "mcl" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "esu_id" INTEGER, "symbol" INTEGER, "usrn" INTEGER,
                    "rec_type" INTEGER, "desc_text" TEXT, "locality" TEXT, "town" TEXT,
                    "entry_date" INTEGER, "typ_3_usrn" INTEGER, "typ_3_desc" TEXT,
                    "typ_4_usrn" INTEGER, "typ_4_desc" TEXT, "lor_ref_1" TEXT,
                    "lor_ref_2" INTEGER, "lor_desc" TEXT, "lane_number" INTEGER,
                    "speed_limit" TEXT, "rural_urban_id" TEXT, "section_type" TEXT,
                    "adoption_status" TEXT, "mcl_ref" INTEGER,
                    "street_classification" TEXT, "in_pilot" TEXT, "carriageway" TEXT);""",
            'lnkESU_STREET': """
                CREATE TABLE "lnkESU_STREET" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "esu_id" INTEGER, "usrn" INTEGER, "esu_version_no" INTEGER,
                    "usrn_version_no" INTEGER, "currency_flag" INTEGER,
                    "entry_date" INTEGER, "update_date" INTEGER,
                    "closure_date" INTEGER);""",
            'lnkMAINT_RD_POL': """
                CREATE TABLE "lnkMAINT_RD_POL" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "rd_pol_id" INTEGER, "currency_flag" INTEGER,
                    "maint_id" INTEGER);""",
            'tblESU': """
                CREATE TABLE "tblESU" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "esu_id" INTEGER, "version_no" INTEGER, "currency_flag" INTEGER,
                    "xref" INTEGER, "yref" INTEGER, "entry_date" INTEGER,
                    "closure_date" INTEGER, "start_xref" DOUBLE, "start_yref" DOUBLE,
                    "end_xref" DOUBLE, "end_yref" DOUBLE, "tolerance" INTEGER,
                    "parent_esu_id" INTEGER, "gqc" TEXT, "lor_no" TEXT,
                    "private" TEXT, "comments" TEXT, "start_date" INTEGER,
                    "update_date" INTEGER);""",
            'tblRD_POL': """
                CREATE TABLE "tblRD_POL" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "rd_pol_id" INTEGER, "xref" INTEGER, "yref" INTEGER,
                    "currency_flag" INTEGER, "entry_date" INTEGER,
                    "version_no" INTEGER, "parent_rd_pol_id" INTEGER, "comments" TEXT,
                    "closure_date" INTEGER);""",
            'tblGazMetadata': """
                CREATE TABLE "tblGazMetadata" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "name" TEXT, "scope" TEXT, "territory" TEXT, "owner" TEXT,
                    "custodian" TEXT, "coord_sys" TEXT, "coord_units" TEXT,
                    "metadata_date" INTEGER, "class_scheme" TEXT, "code_scheme" TEXT,
                    "current_date" INTEGER, "gaz_language" TEXT, "charset" TEXT,
                    "custodian_code" INTEGER);""",
            'tblMAINT': """
                CREATE TABLE "tblMAINT" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "maint_id" INTEGER, "version_no" INTEGER, "usrn" INTEGER,
                    "reference_no" INTEGER, "swa_org_ref" TEXT, "location_text" TEXT,
                    "whole_road" INTEGER, "road_status_ref" INTEGER, "start_xref" DOUBLE,
                    "start_yref" DOUBLE, "end_xref" DOUBLE, "end_yref" DOUBLE,
                    "entry_date" INTEGER, "entered_by" TEXT, "closure_date" INTEGER,
                    "closed_by" TEXT, "adoption_date" INTEGER, "currency_flag" INTEGER,
                    "lor_no" TEXT, "route" TEXT, "notes" TEXT);""",
            'tblREINS_CAT': """
                CREATE TABLE "tblREINS_CAT" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "reins_cat_id" INTEGER, "version_no" INTEGER, "currency_flag" INTEGER,
                    "usrn" INTEGER, "reference_no" INTEGER, "reinstatement_code" INTEGER,
                    "location_text" TEXT, "start_xref" DOUBLE, "start_yref" DOUBLE,
                    "end_xref" DOUBLE, "end_yref" DOUBLE, "whole_road" INTEGER,
                    "entry_date" INTEGER, "closure_date" INTEGER, "entered_by" TEXT,
                    "closed_by" TEXT, "notes" TEXT);""",
            'tblSPEC_DES': """
                CREATE TABLE "tblSPEC_DES" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "spec_des_id" INTEGER, "version_no" INTEGER, "currency_flag" INTEGER,
                    "usrn" INTEGER, "reference_no" INTEGER, "designation_code" INTEGER,
                    "location_text" TEXT, "start_xref" DOUBLE, "start_yref" DOUBLE,
                    "end_xref" DOUBLE, "end_yref" DOUBLE, "whole_road" INTEGER,
                    "swa_org_ref" TEXT, "designation_date" INTEGER, "description" TEXT,
                    "entry_date" INTEGER, "entered_by" TEXT, "closure_date" INTEGER,
                    "closed_by" TEXT, "notes" TEXT);""",
            'tblSTREET': """
                CREATE TABLE "tblSTREET" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "usrn" INTEGER, "version_no" INTEGER, "currency_flag" INTEGER,
                    "street_ref_type" INTEGER, "description" TEXT, "entry_date" INTEGER,
                    "update_date" INTEGER, "start_date" INTEGER, "authority" INTEGER,
                    "closure_date" INTEGER, "start_xref" DOUBLE, "start_yref" DOUBLE,
                    "end_xref" DOUBLE, "end_yref" DOUBLE, "tolerance" INTEGER,
                    "street_sub_type" INTEGER, "street_state" INTEGER,
                    "state_date" INTEGER, "street_class" INTEGER, "loc_ref" INTEGER,
                    "county_ref" INTEGER, "town_ref" INTEGER, "updated_by" TEXT,
                    "closed_by" TEXT, "min_x" INTEGER, "min_y" INTEGER, "max_x" INTEGER,
                    "max_y" INTEGER, "description_alt" TEXT);""",
            'tlkpCOUNTY': """
                CREATE TABLE "tlkpCOUNTY" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "county_ref" INTEGER, "name" TEXT, "alt_name" TEXT);""",
            'tlkpLOCALITY': """
                CREATE TABLE "tlkpLOCALITY" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "loc_ref" INTEGER, "name" TEXT, "alt_name" TEXT);""",
            'tlkpORG': """
                CREATE TABLE "tlkpORG" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "swa_org_ref" TEXT, "description" TEXT);""",
            'tlkpREINS_CAT': """
                CREATE TABLE "tlkpREINS_CAT" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "reinstatement_code" INTEGER, "description" TEXT,
                    "category" INTEGER);""",
            'tlkpROAD_STATUS': """
                CREATE TABLE "tlkpROAD_STATUS" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "road_status_ref" INTEGER, "description" TEXT);""",
            'tlkpSPEC_DES': """
                CREATE TABLE "tlkpSPEC_DES" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "designation_code" INTEGER, "designation_text" TEXT,
                    "date_text" TEXT, "mandatory_fields" TEXT);""",
            'tlkpSTREET_CLASS': """
                CREATE TABLE "tlkpSTREET_CLASS" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "class_ref" INTEGER, "street_classification" TEXT);""",
            'tlkpSTREET_REF_TYPE': """
                CREATE TABLE "tlkpSTREET_REF_TYPE" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "street_ref" INTEGER, "description" TEXT);""",
            'tlkpSTREET_STATE': """
                CREATE TABLE "tlkpSTREET_STATE" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "state_ref" INTEGER, "state_desc" TEXT);""",
            'tlkpTOWN': """
                CREATE TABLE "tlkpTOWN" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "town_ref" INTEGER, "name" TEXT, "alt_name" TEXT);""",
            'tblUsers': """
                CREATE TABLE "tblUsers" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "username" TEXT, "userpwd" TEXT, "usertype" TEXT);""",
            'tlkpAUTHORITY': """
                CREATE TABLE "tlkpAUTHORITY" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "auth_code" INTEGER,
                    "description" TEXT);""",
            'tlkpWHOLE_ROAD': """
                CREATE TABLE "tlkpWHOLE_ROAD" (
                    "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "whole_road" INTEGER, "description" TEXT);""",
            'layer_styles': """
                CREATE TABLE "layer_styles" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "f_table_catalog" varchar(256), "f_table_schema" varchar(256),
                    "f_table_name" varchar(256), "f_geometry_column" varchar(256),
                    "styleName" varchar(30), "styleQML" text, "styleSLD" text,
                    "useAsDefault" boolean, "description" text, "owner" varchar(30),
                    "ui" text, "update_time" timestamp DEFAULT CURRENT_TIMESTAMP);"""}

        self.sql_create_spatial_indexes = {
            'esu': """
                SELECT CreateSpatialIndex("esu", "geometry");""",
            'rdpoly': """
                SELECT CreateSpatialIndex("rdpoly", "geometry");""",
            'mcl': """
                SELECT CreateSpatialIndex("mcl", "geometry");"""}

        self.sql_populate_geometry_tables = {
            'esu': """
                INSERT INTO esu (geometry, esu_id, symbol)
                SELECT
                    GeomFromText(AsText(CastToMultiLinestring(geometry)),
                                        27700), esu_id, symbol
                FROM tmp_esu;""",
            'rdpoly': """
                INSERT INTO rdpoly (geometry,
                    symbol, rd_pol_id, element, hierarchy, ref_1, ref_2,
                    desc_1, desc_2, desc_3, ref_3,
                    part_label, label, label1, feature_length, r_usrn,
                    mcl_cref)
                SELECT
                    GeomFromText(AsText(CastToMultiPolygon(geometry)),
                    27700), symbol, rd_pol_id, element, hierarchy, ref_1,
                    ref_2, desc_1, desc_2, desc_3, ref_3,
                    part_label, label, label1, feature_length, r_usrn,
                    mcl_cref
                FROM tmp_rdpoly;""",
            'mcl': """
                INSERT INTO mcl (geometry,
                    esu_id, symbol, usrn, rec_type, desc_text,
                    locality, town, entry_date, typ_3_usrn, typ_3_desc,
                    typ_4_usrn, typ_4_desc, lor_ref_1, lor_ref_2, lor_desc,
                    lane_number, speed_limit, rural_urban_id, section_type,
                    adoption_status, mcl_ref, street_classification,
                    carriageway)
                SELECT
                    GeomFromText(AsText(CastToMultiLinestring(geometry)),
                    27700), esu_id, symbol, usrn, rec_type, desctxt,
                    locality, town, entry_date, typ3usrn, typ3desc,
                    typ4usrn, typ4desc, lor_ref_1, lor_ref_2, lor_desc,
                    lane_number, speed_limit, rural_urban_id, section_type,
                    adoption_status, mcl_ref, street_classification,
                    carriageway
                FROM tmp_mcl;"""}

        self.sql_geometry = {
            'add_spatial_metadata': """
                SELECT InitSpatialMetadata(1);""",
            'esu_add_geometry_column': """
                SELECT AddGeometryColumn('esu', 'geometry', 27700,
                    'MULTILINESTRING', 'XY', 0);""",
            'rdpoly_add_geometry_column': """
                SELECT AddGeometryColumn('rdpoly', 'geometry', 27700,
                    'MULTIPOLYGON', 'XY', 0);""",
            'mcl_add_geometry_column': """
                SELECT AddGeometryColumn('mcl', 'geometry', 27700,
                    'MULTILINESTRING', 'XY', 0);"""}

        self.sql_get_from_mdb = {
            'lnkESU_STREET': """
                SELECT esu_id, usrn, esu_version_no, usrn_version_no,
                currency_flag, entry_date, update_date, closure_date
                FROM lnkESU_STREET;""",
            'lnkMAINT_RD_POL': """
                SELECT rd_pol_id, currency_flag, maint_id
                FROM lnkMAINT_RD_POL;""",
            'tblESU': """
                SELECT esu_id, version_no, currency_flag, xref, yref,
                entry_date, closure_date, start_xref, start_yref, end_xref,
                end_yref, tolerance, parent_esu_id, gqc, LorNo, private,
                comments, start_date, update_date
                FROM tblESU;""",
            'tblGazMetadata': """
                SELECT name, scope, territory, owner, custodian,
                coordsys, coordunits, metadatadate, NULL,  NULL, NULL,
                NULL, NULL, NULL
                FROM tblGazMetadata;""",
            'tblMAINT': """
                SELECT maint_id, version_no, usrn, reference_no, swa_org_ref,
                location_text, whole_road, road_status_ref, start_xref,
                start_yref, end_xref, end_yref, entry_date, entered_by,
                closure_date, closed_by, adoption_date, currency_flag,
                lor_no, route, notes
                FROM tblMAINT;""",
            'tblRD_POL': """
                SELECT rd_pol_id, xref, yref, currency_flag, entry_date,
                version_no, parent_rd_pol_id, comments, closure_date
                FROM tblRD_POL;""",
            'tblREINS_CAT': """
                SELECT reins_cat_id, version_no, currency_flag, usrn,
                reference_no, reinstatement_code, location_text, start_xref,
                start_yref, end_xref, end_yref, whole_road, entry_date,
                closure_date, entered_by, closed_by, notes
                FROM tblREINS_CAT;""",
            'tblSPEC_DES': """
                SELECT spec_des_id, version_no, currency_flag, usrn,
                reference_no, designation_code, location_text, start_xref,
                start_yref, end_xref, end_yref, whole_road, swa_org_ref,
                designation_date, description, entry_date, entered_by,
                closure_date, closed_by, notes
                FROM tblSPEC_DES;""",
            'tblSTREET': """
                SELECT usrn, version_no, currency_flag, street_ref_type,
                description, entry_date, update_date, start_date, authority,
                closure_date, start_xref, start_yref, end_xref, end_yref,
                tolerance, street_state, state_date,
                street_class, loc_ref, county_ref, town_ref, updated_by,
                closed_by, min_x, min_y, max_x, max_y, description_alt
                FROM tblSTREET;""",
            'tblUsers': """
                SELECT username, userpwd, usertype
                FROM tblUsers;""",
            'tlkpAUTHORITY': """
                SELECT auth_code, description
                FROM tlkpAUTHORITY;""",
            'tlkpCOUNTY': """
                SELECT county_ref, name, alt_name
                FROM tlkpCOUNTY;""",
            'tlkpLOCALITY': """
                SELECT loc_ref, name, alt_name
                FROM tlkpLOCALITY;""",
            'tlkpORG': """
                SELECT swa_org_ref, description
                FROM tlkpORG;""",
            'tlkpREINS_CAT': """
                SELECT reinstatement_code, description, category
                FROM tlkpREINS_CAT;""",
            'tlkpROAD_STATUS': """
                SELECT road_status_ref, description
                FROM tlkpROAD_STATUS;""",
            'tlkpSPEC_DES': """
                SELECT designation_code, designation_text, date_text,
                mandatory_fields
                FROM tlkpSPEC_DES;""",
            'tlkpSTREET_CLASS': """
                SELECT class_ref, street_classification
                FROM tlkpSTREET_CLASS;""",
            'tlkpSTREET_REF_TYPE': """
                SELECT street_ref_type, description
                FROM tlkpSTREET_REF_TYPE;""",
            'tlkpSTREET_STATE': """
                SELECT state_ref, state_desc
                FROM tlkpSTREET_STATE;""",
            'tlkpTOWN': """
                SELECT town_ref, name, alt_name
                FROM tlkpTOWN;""",
            'tlkpWHOLE_ROAD': """
                SELECT whole_road, description
                FROM tlkpWHOLE_ROAD;""" }

        self.sql_populate_non_geometry_tables = {
            'lnkESU_STREET': """
                INSERT INTO lnkESU_STREET (esu_id, usrn, esu_version_no,
                                             usrn_version_no, currency_flag,
                                              entry_date, update_date,
                                             closure_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            'lnkMAINT_RD_POL': """
                INSERT INTO lnkMAINT_RD_POL (rd_pol_id, currency_flag,
                                               maint_id)
                VALUES (?, ?, ?);""",
            'tblESU': """
                INSERT INTO tblESU (esu_id, version_no, currency_flag,
                                    xref, yref, entry_date, closure_date,
                                    start_xref, start_yref, end_xref,
                                    end_yref, tolerance, parent_esu_id,
                                    gqc, lor_no, private, comments,
                                    start_date, update_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?);""",
            'tblGazMetadata': """
                INSERT INTO tblGazMetadata (name, scope, territory, owner,
                                            custodian, coord_sys, coord_units,
                                            metadata_date, class_scheme,
                                            code_scheme, current_date,
                                            gaz_language, charset,
                                            custodian_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            'tblMAINT': """
                INSERT INTO tblMAINT (
                    maint_id, version_no, usrn, reference_no, swa_org_ref,
                    location_text, whole_road, road_status_ref, start_xref,
                    start_yref, end_xref, end_yref, entry_date, entered_by,
                    closure_date, closed_by, adoption_date, currency_flag,
                    lor_no, route, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?);""",
            'tblRD_POL': """
                INSERT INTO tblRD_POL (
                    rd_pol_id, xref, yref, currency_flag, entry_date,
                    version_no, parent_rd_pol_id, comments, closure_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            'tblREINS_CAT': """
                INSERT INTO tblREINS_CAT (
                    reins_cat_id, version_no, currency_flag,
                    usrn, reference_no, reinstatement_code, location_text,
                    start_xref, start_yref, end_xref, end_yref, whole_road,
                    entry_date, closure_date, entered_by, closed_by, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?);""",
            'tblSPEC_DES': """
                INSERT INTO tblSPEC_DES (
                    spec_des_id, version_no, currency_flag,
                    usrn, reference_no, designation_code, location_text,
                    start_xref, start_yref, end_xref, end_yref, whole_road,
                    swa_org_ref, designation_date, description, entry_date,
                    entered_by, closure_date, closed_by, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?);""",
            'tblSTREET': """
                INSERT INTO tblSTREET (
                    usrn, version_no, currency_flag, street_ref_type,
                    description, entry_date, update_date, start_date,
                    authority, closure_date, start_xref, start_yref,
                    end_xref, end_yref, tolerance, street_sub_type,
                    street_state, state_date, street_class, loc_ref,
                    county_ref, town_ref, updated_by, closed_by, min_x,
                    min_y, max_x, max_y, description_alt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            'tblUsers': """
                INSERT INTO tblUsers (username, userpwd, usertype)
                VALUES (?, ?, ?);""",
            'tlkpAUTHORITY': """
                INSERT INTO tlkpAUTHORITY (auth_code, description)
                VALUES (?, ?);""",
            'tlkpCOUNTY': """
                INSERT INTO tlkpCOUNTY (county_ref, name, alt_name)
                VALUES (?, ?, ?);""",
            'tlkpLOCALITY': """
                INSERT INTO tlkpLOCALITY (loc_ref, name, alt_name)
                VALUES (?, ?, ?);""",
            'tlkpORG': """
                INSERT INTO tlkpORG (swa_org_ref, description)
                VALUES (?, ?);""",
            'tlkpREINS_CAT': """
                INSERT INTO tlkpREINS_CAT (reinstatement_code, description,
                                           category)
                VALUES (?, ?, ?);""",
            'tlkpROAD_STATUS': """
                INSERT INTO tlkpROAD_STATUS (road_status_ref, description)
                VALUES (?, ?);""",
            'tlkpSPEC_DES': """
                INSERT INTO tlkpSPEC_DES (designation_code, designation_text,
                                          date_text, mandatory_fields)
                VALUES (?, ?, ?, ?);""",
            'tlkpSTREET_CLASS': """
                INSERT INTO tlkpSTREET_CLASS (class_ref, street_classification)
                VALUES (?, ?);""",
            'tlkpSTREET_REF_TYPE': """
                INSERT INTO tlkpSTREET_REF_TYPE (street_ref, description)
                VALUES (?, ?);""",
            'tlkpSTREET_STATE': """
                INSERT INTO tlkpSTREET_STATE (state_ref, state_desc)
                VALUES (?, ?);""",
            'tlkpTOWN': """
                INSERT INTO tlkpTOWN (town_ref, name, alt_name)
                VALUES (?, ?, ?);""",
            'tlkpWHOLE_ROAD': """
               INSERT INTO tlkpWHOLE_ROAD (whole_road, description)
                VALUES (?, ?);"""}


    def prepare_new_col_names(self):
        """
        Prepare dictionary of columns to be renamed in each table.
        """
        self.new_col_names = {
            'mcl': {'DescTxt': 'desc_txt', 'Typ3USRN': 'type_3_usrn',
                    'Typ3Desc': 'type_3_desc', 'Typ4USRN': 'type_4_usrn',
                    'Typ4Desc': 'type_4_desc'},
            'tblESU': {'LorNo': 'lor_no'},
            'tblGazMetadata': {'Coordsys': 'coord_sys',
                               'CoordUnits': 'coord_units',
                               'MetadataDate': 'metadata_date',
                               'ClassScheme': 'class_scheme',
                               'CodeScheme': 'code_scheme',
                               'CurrentDate': 'current_date',
                               'GazLanguage': 'gaz_language',
                               'CustodianCode': 'custodian_code'}}

    def prepare_custom_sql(self):
        self.custom_table_amendments = {
            'Clacks': ["DELETE FROM rdpoly;",
                       "DELETE FROM sqlite_sequence WHERE name='rdpoly';",
                       "ALTER TABLE rdpoly ADD COLUMN SW_LOCAL TEXT;",
                       "ALTER TABLE rdpoly ADD COLUMN MATERIAL TEXT;",
                       "ALTER TABLE rdpoly ADD COLUMN CONDITION DOUBLE;",
                       "ALTER TABLE rdpoly ADD COLUMN EXTENT DOUBLE;",
                       "ALTER TABLE rdpoly ADD COLUMN HIER_FACT INTEGER;",
                       "ALTER TABLE rdpoly ADD COLUMN COND_EXT_SCORE INTEGER;",
                       "ALTER TABLE rdpoly ADD COLUMN COND_EXT_FACT INTEGER;",
                       "ALTER TABLE rdpoly ADD COLUMN RATING INTEGER;",
                       "ALTER TABLE rdpoly ADD COLUMN TREAT_RATE TEXT;",
                       "ALTER TABLE rdpoly ADD COLUMN AREA TEXT;",
                       "ALTER TABLE rdpoly ADD COLUMN WORKS_COST TEXT;",
                       "ALTER TABLE rdpoly ADD COLUMN INSP_DATE DATE;",
                       """\
                          INSERT INTO rdpoly (geometry, symbol, rd_pol_id,
                              element, hierarchy, ref_1, ref_2, desc_1, desc_2,
                              desc_3, ref_3, part_label, label, label1,
                              feature_length, r_usrn, mcl_cref, SW_LOCAL,
                              MATERIAL, CONDITION, EXTENT, HIER_FACT,
                              COND_EXT_SCORE, COND_EXT_FACT, RATING,
                              TREAT_RATE, AREA, WORKS_COST, INSP_DATE)
                          SELECT GeomFromText(AsText(CastToMultiPolygon(geometry)), 27700),
                              symbol, rd_pol_id, element, hierarchy, ref_1,
                              ref_2, desc_1, desc_2, desc_3, ref_3, part_label,
                              label, label1, feature_length, r_usrn, mcl_cref,
                              SW_LOCAL, MATERIAL, CONDITION, EXTENT, HIER_FACT,
                              COND_EXT_SCORE, COND_EXT_FACT, RATING, TREAT_RATE,
                              AREA, WORKS_COST, INSP_DATE
                          FROM tmp_rdpoly;"""],

            'AyrshireRoads': [
                "DELETE FROM rdpoly;",
                "DELETE FROM sqlite_sequence WHERE name='rdpoly';",
                "ALTER TABLE rdpoly ADD COLUMN Asset_Group INTEGER;",
                "ALTER TABLE rdpoly ADD COLUMN Adoption_Status INTEGER;",
                "ALTER TABLE rdpoly ADD COLUMN Road_Class INTEGER;",
                "ALTER TABLE rdpoly ADD COLUMN Carriageway_Hierarchy INTEGER;",
                "ALTER TABLE rdpoly ADD COLUMN Footpath_Footway_Hierarchy INTEGER;",
                "ALTER TABLE rdpoly ADD COLUMN Manual_Length DOUBLE;",
                "ALTER TABLE rdpoly ADD COLUMN Environment TEXT;",
                "ALTER TABLE rdpoly ADD COLUMN Surface_Course_Material TEXT;",
                "ALTER TABLE rdpoly ADD COLUMN Average_Width DOUBLE;",
                """\
                INSERT INTO rdpoly (geometry, symbol, rd_pol_id,
                    Asset_Group, Adoption_Status, Road_Class,
                    Carriageway_Hierarchy, Footpath_Footway_Hierarchy,
                    Manual_Length, Environment, Surface_Course_Material,
                    Average_Width)
                SELECT GeomFromText(AsText(CastToMultiPolygon(geometry)), 27700),
                    symbol, rd_pol_id,
                    Asset_Group, Adoption_Status, Road_Class,
                    Carriageway_Hierarchy, Footpath_Footway_Hierarchy,
                    Manual_Length, Environment, Surface_Course_Material,
                    Average_Width
                FROM tmp_rdpoly;"""],
            'Renfrew': ["DELETE FROM rdpoly;",
                        "DELETE FROM sqlite_sequence WHERE name='rdpoly';",
                        "ALTER TABLE rdpoly ADD COLUMN COMMENTS TEXT;",
                        """\
                        INSERT INTO rdpoly (geometry, symbol, rd_pol_id,
                            element, COMMENTS)
                        SELECT
                            GeomFromText(AsText(CastToMultiPolygon(geometry)),
                                     27700),
                            symbol, rd_pol_id, element, comments
                        FROM tmp_rdpoly;"""]}

    def run_custom_sql(self, council):
        """
        Run custom commands to handle extra columns for different councils.
        :param council: Name of council with custom instructions.
        """
        self.open_sqlite_connection_and_cursor()
        print('Running custom SQL for {}'.format(council))
        for sql in self.custom_table_amendments[council]:
                print(dedent(sql))
                self.sqlite_cursor.execute(sql)
        self.commit_and_close_sqlite()

    def print_row_count(self, table):
        """
        Print the number of rows in given table.
        :param table: Name of table to check
        """
        sql = "SELECT COUNT(*) AS row_count FROM {}".format(table)
        self.sqlite_cursor.execute(sql)
        row_count = self.sqlite_cursor.fetchone()[0]
        print("{} rows copied into table {}".format(row_count, table))

    def populate_lookup_tables(self):
        """
        Populate lookup tables.  This isn't run for migrations, but can be
        used to add sensible values to a newly created database.
        """
        print('Populating lookup tables')
        self.open_sqlite_connection_and_cursor()
        self.sqlite_cursor.executescript(sql_scripts.populate_lookup_tables)
        self.commit_and_close_sqlite()


if __name__ == '__main__':
    main()
