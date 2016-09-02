# -*- coding: utf-8 -*-
from mock import patch
import os
import pprint
import shutil
import subprocess
import unittest

from textwrap import dedent
from pyspatialite import dbapi2 as db
import qgis.core  # Need to import this before PyQt to ensure QGIS parts work
from PyQt4.QtSql import QSqlQuery, QSqlDatabase

from Roadnet.database import connect_and_open
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.ramp import length_of_roads as lor

this_dir = os.path.dirname(os.path.abspath(__file__))

SQL_SCRIPT = """
INSERT INTO mcl VALUES (
1, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
1, 30, 'U', 'CW', 'Public', 11111, 'U', NULL, 'Single',
GeomFromText("MULTILINESTRING((0 0,0 1,0 100))", 27700) );
INSERT INTO mcl VALUES (
2, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
1, 30, 'A', 'CW', 'Public', 11111, 'U', NULL, 'Single',
GeomFromText("MULTILINESTRING((0 0,0 1,0 1000))", 27700) );
INSERT INTO mcl VALUES (
3, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
3, 30, 'U', 'CW', 'Public', 11111, 'B', NULL, 'Single',
GeomFromText("MULTILINESTRING((0 0,0 1,0 200))", 27700) );
INSERT INTO mcl VALUES (
4, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
2, 30, 'U', 'CW', 'Public', 11111, 'U', NULL, 'Dual',
GeomFromText("MULTILINESTRING((0 0,0 1,0 2000))", 27700) );
INSERT INTO mcl VALUES (
5, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
2, 30, 'U', 'FT', 'Public', 11111, 'U', NULL, 'Single',
GeomFromText("MULTILINESTRING((0 0,0 1,0 9999))", 27700) );
"""


class TestLORExports(QgisTestCase):

    empty_db_path = os.path.join('database_files', 'roadnet_empty.sqlite')
    test_db_path = os.path.join(this_dir, 'roadnet_test.sqlite')
    test_directory = os.path.join(this_dir, 'test_dir')
    db = None

    def setUp(self):
        super(TestLORExports, self).setUp()
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
        super(TestLORExports, self).tearDown()
        if self.db:  # Just in case self.db doesn't get set
            self.db.close()
            del self.db
            QSqlDatabase.removeDatabase('integration_testing')

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def tidy(self):
        shutil.rmtree(self.test_directory, ignore_errors=True)

    def test_prepare_sql_c_urban_3lanes(self):
        # Arrange
        street_classification = 'C'
        rural_urban_id = 'U'
        lanes_key = 'Three lane'
        expected = dedent("""
        SELECT Round(Sum(GLength(geometry))/1000, 2) AS length
        FROM mcl
        WHERE section_type = 'CW' AND
            street_classification = "C"
            AND speed_limit IN ('20PT/30', '20PT/40', '20', '30', '40')
            AND lane_number = 3 AND Carriageway = 'Single'
            ;""")

        # Act
        sql = lor.prepare_sql(street_classification, lanes_key, rural_urban_id)

        # Assert
        print("\nExpected:{}".format(expected))
        print("\nActual:{}".format(sql))
        self.assertEqual(expected, sql,
                         "Incorrect SQL generated.")

    @patch.object(rn_except.QMessageBoxWarningError, 'show_message_box')
    def test_get_length_of_roads_text(self, mock_error):
        # Arrange
        expected = get_expected_text()

        # Act
        try:
            lor_text = lor.get_length_of_roads_text(self.db)
        except rn_except.BadSpatialiteVersionError:
            msg = "Host machine has Spatialite version < 4.3.0."
            raise unittest.SkipTest(msg)

        # Assert
        lor_text = lor_text.strip()
        print("\nExpected:")
        print(expected)
        print("\nActual:")
        print(lor_text)
        self.assertEqual(expected, lor_text,
                         "Incorrect length of roads text returned.")


def get_expected_text():
    """
    Returns expected text.  Defined here to save cluttering test code.
    :return: str expected text
    """
    expected = """\
        A Roads, Urban (<=40 mph), Rural (>40 mph)
        Single Track / two lane, 0, 0
        Three lane, 0, 0
        Four lane, 0, 0
        Five lane, 0, 0
        Six lane, 0, 0
        Total, 0, 0
        Of which Dual Carriageway, 0, 0

        B Roads, Urban (<=40 mph), Rural (>40 mph)
        Single Track / two lane, 0, 0
        Three lane, 0.2, 0
        Four lane, 0, 0
        Five lane, 0, 0
        Six lane, 0, 0
        Total, 0.2, 0
        Of which Dual Carriageway, 0, 0

        C Roads, Urban (<=40 mph), Rural (>40 mph)
        Single Track / two lane, 0, 0
        Three lane, 0, 0
        Four lane, 0, 0
        Five lane, 0, 0
        Six lane, 0, 0
        Total, 0, 0
        Of which Dual Carriageway, 0, 0

        Unclassified Roads, Urban (<=40 mph), Rural (>40 mph)
        Single Track / two lane, 1.1, 0
        Three lane, 0, 0
        Four lane, 0, 0
        Five lane, 0, 0
        Six lane, 0, 0
        Total, 3.1, 0
        Of which Dual Carriageway, 2.0, 0"""
    return dedent(expected)


if __name__ == '__main__':
    unittest.main()
