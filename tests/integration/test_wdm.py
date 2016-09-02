# -*- coding: utf-8 -*-
from mock import patch
import os
import pprint
import shutil
import subprocess
import unittest

from pyspatialite import dbapi2 as db
import qgis.core  # Need to import this before PyQt to ensure QGIS parts work
from PyQt4.QtSql import QSqlQuery, QSqlDatabase


from Roadnet.database import connect_and_open
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.ramp import wdm
from Roadnet.bin import shapefile_attributes

this_dir = os.path.dirname(os.path.abspath(__file__))

SQL_SCRIPT = """
INSERT INTO rdpoly VALUES (
1, 11, 1, 'CGWAY', 'LAR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'C119/10', '/CGWAY/', '/CGWAY//', NULL, NULL, 11111,
GeomFromText("MULTIPOLYGON(((287500 691400, 287500 691500, 287600 691500, 287600 691400 )))",  27700) );
INSERT INTO rdpoly VALUES (
2, 11, 2, 'FTWAY', 'LAF', NULL, NULL, NULL, 'E', 1, 1, NULL, 'C119/10', '/FTWAY/1', '/FTWAY/E/1', NULL, NULL, 22222,
GeomFromText("MULTIPOLYGON(((288000 691400, 288000 691500, 288100 691500, 288100 691400 )))",  27700) );
INSERT INTO rdpoly VALUES (
3, 11, 3, 'FTWAY', 'LAF', NULL, NULL, NULL, 'E', 2, 2, NULL, 'C119/10', '/FTWAY/2', '/FTWAY/E/2', NULL, NULL, 33333,
GeomFromText("MULTIPOLYGON(((287500 691900, 287500 692000, 287600 692000, 287600 691900 )))",  27700) );
INSERT INTO rdpoly VALUES (
4, 11, 4, 'FTWAY', 'LAF', NULL, NULL, NULL, 'S', 1, 1, NULL, 'C119/20', '/FTWAY/1', '/FTWAY/S/1', NULL, NULL, 44444,
GeomFromText("MULTIPOLYGON(((287800 692200, 287800 692300, 287900 692300, 287900 692200 )))",  27700) );

INSERT INTO mcl VALUES (
1, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
NULL, 30, 'U', 'FT', 'Public', 11111, 'U', NULL, NULL,
GeomFromText("MULTILINESTRING((0 0,0 1,0 2))", 27700) );
INSERT INTO mcl VALUES (
2, 20573, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 50,
'Test MCL Two',
NULL, 30, 'U', 'FT', 'Public', 22222, 'U', NULL, NULL,
GeomFromText("MULTILINESTRING((293166.277 680074.52,293180.28 680074.606,293181.610 680074.83))", 27700) );
INSERT INTO mcl VALUES (
3, 18163, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 40,
'Test MCL Three',
NULL, 30, 'U', 'FT', 'Public', 33333, 'U', NULL, NULL,
GeomFromText("MULTILINESTRING((293141.8919999999 680074.376,293166.2779999999 680074.5219999999))", 27700) );
INSERT INTO mcl VALUES (
4, 18163, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 40,
'Test MCL Four',
NULL, 30, 'U', 'FT', 'Public', 44444, 'U', NULL, NULL,
GeomFromText("MULTILINESTRING((293141.8919999999 680074.376,293166.2779999999 680074.5219999999))", 27700) );
"""


class TestWDMExports(QgisTestCase):

    empty_db_path = os.path.join('database_files', 'roadnet_empty.sqlite')
    test_db_path = os.path.join(this_dir, 'roadnet_test.sqlite')
    test_directory = os.path.join(this_dir, 'test_dir')
    db = None

    def setUp(self):
        super(TestWDMExports, self).setUp()
        # Make copy of empty database to work on
        shutil.copy(self.empty_db_path, self.test_db_path)

        # Populate with example data
        conn = db.connect(self.test_db_path)
        curs = conn.cursor()
        try:
            curs.executescript(SQL_SCRIPT)
        finally:
            conn.close()

        # Open connection for tests
        self.tidy()
        os.makedirs(self.test_directory)
        self.db = connect_and_open(self.test_db_path, 'integration_testing')

    def tearDown(self):
        super(TestWDMExports, self).tearDown()
        if self.db:  # Just in case self.db doesn't get set
            self.db.close()
            del self.db
            QSqlDatabase.removeDatabase('integration_testing')

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def tidy(self):
        shutil.rmtree(self.test_directory, ignore_errors=True)

    def test_query_db_for_features_success(self):
        # Arrange and Act
        q = wdm.query_db_for_features('FTWAY', self.db)

        # Assert
        try:
            self.assertTrue(isinstance(q, QSqlQuery),
                            "An active QSqlQuery wasn't returned ({})".format(type(q)))
        finally:
            q.finish()
            del q

    def test_ftway_export_returns_three_features(self):
        # Arrange
        features_query = wdm.query_db_for_features('FTWAY', self.db)
        vlayer = wdm.create_temp_layer_in_memory()

        # Act
        wdm.add_features_to_vlayer(features_query, vlayer)

        # Assert
        expected = 3
        count = vlayer.featureCount()
        self.assertEqual(
            expected, count,
            "Number of exported FTWAY features was not {} ({})".format(expected, count))

    @patch.object(rn_except.QMessageBoxWarningError, 'show_message_box')
    def test_exported_attributes(self, mock_error):
        # Arrange
        outfile_names = {'CGWAY': 'RAMPEXPORT_Carriageway.shp',
                         'CYCLE': 'RAMPEXPORT_Cycleway_Path.shp',
                         'FTWAY': 'RAMPEXPORT_Footway.shp'}
        expected_attributes = {
            'CGWAY': [['1', 'CGWAY', 'LAR', '', '', '', '2.000000000000000',
                       '11111', '14305470', 'F-5470', '60', 'Test MCL One', '',
                       '30', 'U', 'U', '']],
            'CYCLE': [],
            'FTWAY': [
                ['2', 'FTWAY', 'LAF', 'E', '1', '1', '', '22222', '14305470',
                 'F-5470', '50', 'Test MCL Two', '', '30', 'U', 'U', ''],
                ['3', 'FTWAY', 'LAF', 'E', '2', '2', '', '33333', '14305470',
                 'F-5470', '40', 'Test MCL Three', '', '30', 'U', 'U', ''],
                ['4', 'FTWAY', 'LAF', 'S', '1', '1', '', '44444', '14305470',
                 'F-5470', '40', 'Test MCL Four', '', '30', 'U', 'U', '']]}

        # Act
        for element_type in outfile_names:
            shapefile_path = os.path.join(self.test_directory,
                                          outfile_names[element_type])
            wdm.export(element_type, self.db, self.test_directory)
            attr = shapefile_attributes.get_ogr2csv(shapefile_path)

            # Assert
            print("-------------")
            print("Expected")
            pprint.pprint(expected_attributes[element_type])
            print("")
            print("Actual")
            pprint.pprint(attr)
            print("-------------")
            self.assertEqual(expected_attributes[element_type], attr)

    def test_create_sql_command_without_length(self):
        # Arrange
        expected = """
        SELECT AsBinary(rdpoly.geometry) AS geometry, rd_pol_id, element, hierarchy,
        desc_2, desc_3, ref_3, currency_flag, feature_length, r_usrn,
        mcl_ref, usrn, lor_ref_1, lor_ref_2, lor_desc, lane_number,
        speed_limit, rural_urban_id, street_classification, carriageway
        FROM rdpoly
        LEFT OUTER JOIN mcl
        ON rdpoly.mcl_cref = mcl.mcl_ref
        WHERE element = "FTWAY"
        AND rdpoly.symbol IN (11, 12);"""

        # Act
        sql = wdm.create_sql_command("FTWAY")

        # Assert
        self.assertEqual(expected, sql)

    def test_create_sql_command_with_length(self):
        # Arrange
        expected = """
        SELECT AsBinary(rdpoly.geometry) AS geometry, rd_pol_id, element, hierarchy,
        desc_2, desc_3, ref_3, currency_flag, GLength(mcl.geometry) AS feature_length, r_usrn,
        mcl_ref, usrn, lor_ref_1, lor_ref_2, lor_desc, lane_number,
        speed_limit, rural_urban_id, street_classification, carriageway
        FROM rdpoly
        LEFT OUTER JOIN mcl
        ON rdpoly.mcl_cref = mcl.mcl_ref
        WHERE element = "CGWAY"
        AND rdpoly.symbol IN (11, 12);"""

        # Act
        sql = wdm.create_sql_command("CGWAY")

        # Assert
        self.assertEqual(expected, sql)


def get_ogr_output_feature_count(shapefile_path):
    cmd = ["ogrinfo", shapefile_path, "-al"]
    ogr_output = subprocess.check_output(cmd)
    for line in ogr_output.split('\n'):
        if line.startswith("Feature Count"):
            count = line.split(':')[1]
            count = count.strip()
            return int(count)
    raise RuntimeError('Feature Count line not found in {}'.format(shapefile_path))

if __name__ == '__main__':
    unittest.main()
