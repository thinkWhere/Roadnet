import os
import pprint
from mock import MagicMock, patch
import shutil
import unittest

from pyspatialite import dbapi2 as db
import qgis.core  # Need to import this before PyQt to ensure QGIS parts work
from qgis.core import QgsVectorLayer
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt, QPyNullVariant

from Roadnet.database import connect_and_open
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase
from Roadnet import vector_layers
import Roadnet.roadnet_exceptions as rn_except
import Roadnet.ramp.mcl_auto_numbering_tool as mant

this_dir = os.path.dirname(os.path.abspath(__file__))

SQL_SCRIPT = """
INSERT INTO mcl VALUES (
1, 20574, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 60,
'Test MCL One',
NULL, 30, 'R', 'FTfff', 'Public', 11111, 'U', NULL, 'Single',
GeomFromText("MULTILINESTRING((0 0,0 1,0 2))", 27700) );
INSERT INTO mcl VALUES (
2, 20573, NULL, 14305470, NULL, NULL, NULL, 'Grangemouth', NULL, NULL, NULL, NULL, NULL, 'F-5470', 50,
'Test MCL Two',
NULL, 30, 'R', 'FT', 'Public', 22222, 'U', NULL, 'Dual',
GeomFromText("MULTILINESTRING((293166.277 680074.52,293180.28 680074.606,293181.610 680074.83))", 27700) );
"""


class TestRampMclAutoNumbering(QgisTestCase):

    empty_db_path = os.path.join('database_files', 'roadnet_empty.sqlite')
    test_db_path = os.path.join(this_dir, 'roadnet_test.sqlite')
    db = None
    mcl = None

    def setUp(self):
        super(TestRampMclAutoNumbering, self).setUp()
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
        self.db = connect_and_open(self.test_db_path, 'integration_testing')

        # Add vector layer
        self.mcl = vector_layers.add_styled_spatialite_layer(
            'mcl', 'MCL', self.db.databaseName(), self.iface)

    def tearDown(self):
        super(TestRampMclAutoNumbering, self).tearDown()
        if self.db:  # Just in case self.db doesn't get set
            self.db.close()
            del self.db
            QSqlDatabase.removeDatabase('integration_testing')

        if self.mcl:
            del self.mcl

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def load_mcl_layer(self):
        """
        Add mcl layer for tests that need it.
        """
        self.mcl = vector_layers.add_styled_spatialite_layer(
            'mcl', 'MCL', self.db.databaseName(), self.iface)

    @patch.object(mant.MclAutoNumberingTool, 'warn_and_revert_selection')
    def test_update_current_mcls_add_one(self, mock_warn):
        # Arrange
        mock_vlayer = MagicMock(spec=QgsVectorLayer)
        auto_num_tool = mant.MclAutoNumberingTool(mock_vlayer, self.db, self.iface)
        mcls = ['1', '2', '3']
        auto_num_tool.current_mcls = mcls
        selected = ['3', '2', '1', '4']
        expected = ['1', '2', '3', '4']

        # Act
        result = auto_num_tool.update_current_mcls(selected)

        # Assert
        self.assertEqual(expected, result)

    @patch.object(mant.MclAutoNumberingTool, 'warn_and_revert_selection')
    def test_update_current_mcls_remove_many(self, mock_warn):
        # Arrange
        mock_vlayer = MagicMock(spec=QgsVectorLayer)
        auto_num_tool = mant.MclAutoNumberingTool(mock_vlayer, self.db, self.iface)
        mcls = ['1', '2', '3', '4']
        auto_num_tool.current_mcls = mcls
        selected = ['3', '2']
        expected = ['2', '3']

        # Act
        result = auto_num_tool.update_current_mcls(selected)

        # Assert
        self.assertEqual(expected, result)

    @patch.object(mant.MclAutoNumberingTool, 'warn_and_revert_selection')
    def test_update_current_mcls_add_many(self, mock_warn):
        # Arrange
        mock_vlayer = MagicMock(spec=QgsVectorLayer)
        auto_num_tool = mant.MclAutoNumberingTool(mock_vlayer, self.db, self.iface)
        mcls = ['1', '2', '3']
        auto_num_tool.current_mcls = mcls
        selected = ['1', '2', '4', '5', '6' '3']
        expected = ['1', '2', '3']

        # Act
        result = auto_num_tool.update_current_mcls(selected)

        # Assert
        self.assertEqual(expected, result)

    @patch.object(rn_except.QMessageBoxWarningError, 'show_message_box')
    def test_set_db_mcl_number_bad_mcl(self, mock_msg):
        # Arrange
        mock_vlayer = MagicMock(spec=QgsVectorLayer)
        auto_num_tool = mant.MclAutoNumberingTool(mock_vlayer, self.db, self.iface)
        auto_num_tool.dlg.ui.mclListWidget.addItems(['bad', 'items'])

        # Act and assert
        with self.assertRaises(rn_except.RampMclNumberingFailedPopupError):
            auto_num_tool.number_mcls()

    def test_apply(self):
        # Arrange
        self.load_mcl_layer()
        auto_num_tool = mant.MclAutoNumberingTool(self.mcl, self.db, self.iface)
        auto_num_tool.dlg.ui.mclListWidget.addItems(['22222', '11111'])
        auto_num_tool.dlg.ui.startValueSpinBox.setValue(3)
        auto_num_tool.dlg.ui.incrementSpinBox.setValue(20)
        ok_button = auto_num_tool.dlg.ui.buttonBox.button(QDialogButtonBox.Ok)
        expected = [23, 3]

        # Act
        QTest.mouseClick(ok_button, Qt.LeftButton)

        # Assert
        mcl_data = get_lor_ref_2_values(self.db)
        pprint.pprint(mcl_data)
        self.assertEqual(mcl_data, expected)

    def test_warn_and_revert_selection(self):
        # Arrange
        self.load_mcl_layer()
        auto_num_tool = mant.MclAutoNumberingTool(self.mcl, self.db, self.iface)
        expected = [11111]

        # Act
        auto_num_tool.warn_and_revert_selection(2, ['11111'])

        # Assert
        result = [f['mcl_ref'] for f in self.mcl.selectedFeatures()]
        self.assertEqual(result, expected)


def get_lor_ref_2_values(db):
    """
    Get lor_ref_2 values a list of ints.
    :param db: QSqlDatabase
    :return: list of ints
    """
    sql = "SELECT lor_ref_2 FROM mcl;"
    query = QSqlQuery(sql, db)
    data = []
    while query.next():
        record = query.record()
        # Skip last record that contains geometry
        data.append(record.value('lor_ref_2'))
    return data

if __name__ == '__main__':
    unittest.main()
