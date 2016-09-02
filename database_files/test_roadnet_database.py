#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import sys
import unittest
from sqlite3 import OperationalError


class TestDatabaseStructure(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(database_file_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        self.conn = None

    def test_sqlite_version(self):
        sql = """SELECT sqlite_version();"""
        self.cursor.execute(sql)
        version_text = self.cursor.fetchone()[0]
        version = int(version_text.replace('.', ''))
        self.assertGreaterEqual(
            version, 382,
            'SQLite version ({}) is less than 3.8.2'.format(version_text))

    def test_column_order(self):
        specs = {'esu': (u'PK_UID', u'esu_id', u'symbol', u'geometry'),
                 'rdpoly': (u'PK_UID', u'symbol', u'rd_pol_id', u'element',
                            u'hierarchy', u'ref_1', u'ref_2', u'desc_1',
                            u'desc_2', u'desc_3', u'ref_3', u'currency_flag',
                            u'part_label', u'label', u'label1',
                            u'feature_length', u'r_usrn', u'mcl_cref',
                            u'geometry'),
                 'mcl': (u'PK_UID', u'esu_id', u'symbol',
                         u'usrn', u'rec_type', u'desc_text', u'locality',
                         u'town', u'entry_date', u'typ_3_usrn', u'typ_3_desc',
                         u'typ_4_usrn', u'typ_4_desc', u'lor_ref_1',
                         u'lor_ref_2', u'lor_desc', u'lane_number',
                         u'speed_limit', u'rural_urban_id', u'section_type',
                         u'adoption_status', u'mcl_ref',
                         u'street_classification', u'in_pilot',
                         u'carriageway', u'geometry'),
                 'layer_styles': (u'id', u'f_table_catalog', u'f_table_schema', u'f_table_name',
                                  u'f_geometry_column', u'styleName', u'styleQML', u'styleSLD',
                                  u'useAsDefault', u'description', u'owner', u'ui', u'update_time'),
                 'lnkESU_STREET': (u'PK_UID', u'esu_id', u'usrn', u'esu_version_no',
                                   u'usrn_version_no', u'currency_flag', u'entry_date',
                                   u'update_date', u'closure_date'),
                 'lnkMAINT_RD_POL': (u'PK_UID', u'rd_pol_id', u'currency_flag', u'maint_id'),
                 'tblESU': (u'PK_UID', u'esu_id', u'version_no', u'currency_flag', u'xref',
                            u'yref', u'entry_date', u'closure_date', u'start_xref', u'start_yref',
                            u'end_xref', u'end_yref', u'tolerance', u'parent_esu_id', u'gqc',
                            u'lor_no', u'private', u'comments', u'start_date', u'update_date'),
                 'tblGazMetadata': (u'PK_UID', u'name', u'scope', u'territory', u'owner',
                                    u'custodian', u'coord_sys', u'coord_units', u'metadata_date',
                                    u'class_scheme', u'code_scheme', u'current_date',
                                    u'gaz_language', u'charset', u'custodian_code'),
                 'tblMAINT': (u'PK_UID', u'maint_id', u'version_no', u'usrn', u'reference_no',
                              u'swa_org_ref', u'location_text', u'whole_road', u'road_status_ref',
                              u'start_xref', u'start_yref', u'end_xref', u'end_yref', u'entry_date',
                              u'entered_by', u'closure_date', u'closed_by', u'adoption_date',
                              u'currency_flag', u'lor_no', u'route', u'notes'),
                 'tblRD_POL': (u'PK_UID', u'rd_pol_id', u'xref', u'yref', u'currency_flag',
                               u'entry_date', u'version_no', u'parent_rd_pol_id', u'comments',
                               u'closure_date'),
                 'tblREINS_CAT': (u'PK_UID', u'reins_cat_id', u'version_no', u'currency_flag',
                                  u'usrn', u'reference_no', u'reinstatement_code', u'location_text',
                                  u'start_xref', u'start_yref', u'end_xref', u'end_yref',
                                  u'whole_road', u'entry_date', u'closure_date', u'entered_by',
                                  u'closed_by', u'notes'),
                 'tblSPEC_DES': (u'PK_UID', u'spec_des_id', u'version_no', u'currency_flag',
                                 u'usrn', u'reference_no', u'designation_code', u'location_text',
                                 u'start_xref', u'start_yref', u'end_xref', u'end_yref',
                                 u'whole_road', u'swa_org_ref', u'designation_date', u'description',
                                 u'entry_date', u'entered_by', u'closure_date', u'closed_by',
                                 u'notes'),
                 'tblSTREET': (u'PK_UID', u'usrn', u'version_no', u'currency_flag',
                               u'street_ref_type', u'description', u'entry_date', u'update_date',
                               u'start_date', u'authority', u'closure_date', u'start_xref',
                               u'start_yref', u'end_xref', u'end_yref', u'tolerance',
                               u'street_sub_type', u'street_state', u'state_date', u'street_class',
                               u'loc_ref', u'county_ref', u'town_ref', u'updated_by', u'closed_by',
                               u'min_x', u'min_y', u'max_x', u'max_y', u'description_alt'),
                 'tblUsers': (u'PK_UID', u'username', u'userpwd', u'usertype'),
                 'tlkpAUTHORITY': (u'PK_UID', u'auth_code', u'description'),
                 'tlkpCOUNTY': (u'PK_UID', u'county_ref', u'name', u'alt_name'),
                 'tlkpLOCALITY': (u'PK_UID', u'loc_ref', u'name', u'alt_name'),
                 'tlkpORG': (u'PK_UID', u'swa_org_ref', u'description'),
                 'tlkpREINS_CAT': (u'PK_UID', u'reinstatement_code', u'description', u'category'),
                 'tlkpROAD_STATUS': (u'PK_UID', u'road_status_ref', u'description'),
                 'tlkpSPEC_DES': (u'PK_UID', u'designation_code', u'designation_text', u'date_text',
                                  u'mandatory_fields'),
                 'tlkpSTREET_CLASS':  (u'PK_UID', u'class_ref', u'street_classification'),
                 'tlkpSTREET_REF_TYPE': (u'PK_UID', u'street_ref', u'description'),
                 'tlkpSTREET_STATE': (u'PK_UID', u'state_ref', u'state_desc'),
                 'tlkpTOWN': (u'PK_UID', u'town_ref', u'name', u'alt_name'),
                 'tlkpWHOLE_ROAD': (u'PK_UID', u'whole_road', u'description')}

        for table, required_cols in specs.iteritems():
            cols, types = self.get_table_columns_and_types(table)
            self.assertEqual(cols, required_cols)

    def test_column_types(self):
        specs = {'esu': (u'INTEGER', u'INTEGER', u'INTEGER',
                         u'MULTILINESTRING'),
                 'rdpoly': (u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT',
                            u'TEXT', u'TEXT', u'INTEGER', u'TEXT', u'TEXT',
                            u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT',
                            u'TEXT', u'TEXT', u'DOUBLE', u'INTEGER',
                            u'INTEGER', u'MULTIPOLYGON'),
                 'mcl': (u'INTEGER', u'DOUBLE', u'INTEGER',
                         u'INTEGER', u'INTEGER', u'TEXT', u'TEXT', u'TEXT',
                         u'INTEGER', u'INTEGER', u'TEXT', u'INTEGER', u'TEXT',
                         u'TEXT', u'INTEGER', u'TEXT', u'INTEGER', u'TEXT',
                         u'TEXT', u'TEXT', u'TEXT', u'DOUBLE', u'TEXT',
                         u'TEXT', u'TEXT', u'MULTILINESTRING'),
                 'layer_styles': (u'INTEGER', u'varchar(256)', u'varchar(256)', u'varchar(256)',
                                  u'varchar(256)', u'varchar(30)', u'text', u'text', u'boolean',
                                  u'text', u'varchar(30)', u'text', u'timestamp'),
                 'lnkESU_STREET': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                                   u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER'),
                 'lnkMAINT_RD_POL': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER'),
                 'tblESU': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                            u'INTEGER', u'INTEGER', u'DOUBLE', u'DOUBLE', u'DOUBLE', u'DOUBLE',
                            u'INTEGER', u'INTEGER', u'TEXT', u'TEXT', u'TEXT', u'TEXT', u'INTEGER',
                            u'INTEGER'),
                 'tblGazMetadata': (u'INTEGER', u'TEXT', u'TEXT', u'TEXT', u'TEXT', u'TEXT',
                                    u'TEXT', u'TEXT', u'INTEGER', u'TEXT', u'TEXT', u'INTEGER',
                                    u'TEXT', u'TEXT', u'INTEGER'),
                 'tblMAINT': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT',
                              u'TEXT', u'INTEGER', u'INTEGER', u'DOUBLE', u'DOUBLE', u'DOUBLE',
                              u'DOUBLE', u'INTEGER', u'TEXT', u'INTEGER', u'TEXT', u'INTEGER',
                              u'INTEGER', u'TEXT', u'TEXT', u'TEXT'),
                 'tblRD_POL': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                               u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT', u'INTEGER'),
                 'tblREINS_CAT':  (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                                   u'INTEGER', u'INTEGER', u'TEXT', u'DOUBLE', u'DOUBLE', u'DOUBLE',
                                   u'DOUBLE', u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT', u'TEXT',
                                   u'TEXT'),
                 'tblSPEC_DES': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                                 u'INTEGER', u'INTEGER', u'TEXT', u'DOUBLE', u'DOUBLE', u'DOUBLE',
                                 u'DOUBLE', u'INTEGER', u'TEXT', u'INTEGER', u'TEXT', u'INTEGER',
                                 u'TEXT', u'INTEGER', u'TEXT', u'TEXT'),
                 'tblSTREET': (u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'TEXT',
                               u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                               u'DOUBLE', u'DOUBLE', u'DOUBLE', u'DOUBLE', u'INTEGER', u'INTEGER',
                               u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER', u'INTEGER',
                               u'INTEGER', u'TEXT', u'TEXT', u'INTEGER', u'INTEGER', u'INTEGER',
                               u'INTEGER', u'TEXT'),
                 'tblUsers': (u'INTEGER', u'TEXT', u'TEXT', u'TEXT'),
                 'tlkpAUTHORITY': (u'INTEGER', u'INTEGER', u'TEXT'),
                 'tlkpCOUNTY': (u'INTEGER', u'INTEGER', u'TEXT', u'TEXT'),
                 'tlkpLOCALITY': (u'INTEGER', u'INTEGER', u'TEXT', u'TEXT'),
                 'tlkpORG': (u'INTEGER', u'TEXT', u'TEXT'),
                 'tlkpREINS_CAT': (u'INTEGER', u'INTEGER', u'TEXT', u'INTEGER'),
                 'tlkpROAD_STATUS':  (u'INTEGER', u'INTEGER', u'TEXT'),
                 'tlkpSPEC_DES': (u'INTEGER', u'INTEGER', u'TEXT', u'TEXT', u'TEXT'),
                 'tlkpSTREET_CLASS': (u'INTEGER', u'INTEGER', u'TEXT'),
                 'tlkpSTREET_REF_TYPE': (u'INTEGER', u'INTEGER', u'TEXT'),
                 'tlkpSTREET_STATE': (u'INTEGER', u'INTEGER', u'TEXT'),
                 'tlkpTOWN': (u'INTEGER', u'INTEGER', u'TEXT', u'TEXT'),
                 'tlkpWHOLE_ROAD': (u'INTEGER', u'INTEGER', u'TEXT')}

        for table, required_types in specs.iteritems():
            cols, types = self.get_table_columns_and_types(table)
            self.assertEqual(types, required_types)

    def get_table_columns_and_types(self, table):
        """
        Query database to get column names and types of a table.
        :param table: Name of table
        :returns: tuple, tuple
        """
        sql = """PRAGMA table_info({});""".format(table)
        self.cursor.execute(sql)
        # zip converts list of rows to list of columns
        result_as_rows = self.cursor.fetchall()
        results = zip(*result_as_rows)
        try:
            columns, types = results[1:3]
            return columns, types
        except ValueError:
            # Return empty values if table doesn't exist.
            return (), ()

    def test_null_or_empty_in_columns(self):
        """
        Some non-primary ID columns cannot be NULL or empty.
        """
        cols_to_check = {
            'esu': ('esu_id', 'geometry'),
            'rdpoly': ('symbol', 'rd_pol_id', 'currency_flag', 'geometry'),
            'mcl': ('geometry',),
            'layer_styles': (),
            'lnkESU_STREET': ('esu_id', 'usrn', 'currency_flag'),
            'lnkMAINT_RD_POL': ('rd_pol_id', 'currency_flag', 'maint_id'),
            'tblESU': ('esu_id', 'version_no', 'currency_flag', 'start_date'),
            'tblGazMetadata': (),
            'tblMAINT': ('maint_id', 'version_no', 'usrn', 'currency_flag'),
            'tblRD_POL': ('rd_pol_id', 'version_no', 'currency_flag'),
            'tblREINS_CAT':  ('reins_cat_id', 'version_no', 'currency_flag', 'usrn'),
            'tblSPEC_DES': ('spec_des_id', 'version_no', 'currency_flag', 'usrn'),
            'tblSTREET': ('usrn', 'version_no', 'currency_flag', 'start_date'),
            'tblUsers': ('username'),
            'tlkpAUTHORITY': ('auth_code',),
            'tlkpCOUNTY': ('county_ref',),
            'tlkpLOCALITY': ('loc_ref',),
            'tlkpORG': ('swa_org_ref',),
            'tlkpREINS_CAT': ('reinstatement_code',),
            'tlkpROAD_STATUS':  ('road_status_ref',),
            'tlkpSPEC_DES': ('designation_code',),
            'tlkpSTREET_CLASS': ('class_ref',),
            'tlkpSTREET_REF_TYPE': ('street_ref',),
            'tlkpSTREET_STATE': ('state_ref',),
            'tlkpTOWN': ('town_ref',),
            'tlkpWHOLE_ROAD': ('whole_road',)}

        for table, columns in cols_to_check.iteritems():
            for column in columns:
                    self.assertEqual(
                        self.contains_nulls_or_empty_cells(table, column), False,
                        'Column {} in table {} contains empty or NULL values'.format(column,
                                                                                     table))

    def contains_nulls_or_empty_cells(self, table, column):
        """
        Query database to determine whether any cells in a column are null or empty.
        :return boolean:
        """
        sql = """SELECT COUNT(*) FROM '{}'
                 WHERE '{}' IS NULL
                 OR '{}' IS '';""".format(table, column, column)
        try:
            self.cursor.execute(sql)
            count = self.cursor.fetchone()[0]
        except OperationalError:
            # Non-existent table counts as empty rows for purpose of this test
            count = 1

        if count > 0:
            return True
        else:
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        database_file_path = sys.argv[1]  # Get file path from command line
        print('Testing {}'.format(database_file_path, os.getcwd()))
        unittest.main(argv=[sys.argv[0]])  # Pass remaining args to unittest
    else:
        print('No database specified.')
