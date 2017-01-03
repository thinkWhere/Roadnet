from mock import MagicMock
import os
import pprint
import shutil
import unittest

from pyspatialite import dbapi2 as db
import qgis.core  # Need to import this before PyQt to ensure QGIS parts work
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt, QPyNullVariant

from Roadnet.database import connect_and_open
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase
import Roadnet.roadnet_exceptions as rn_except
import Roadnet.ramp.record_editors as ramp_eds
from Roadnet.ramp.selector_tools import MclSelectorTool, RampSelectorTool

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
INSERT INTO rdpoly VALUES (
    21473, 11, 27100, 'SSTRIP', 'SS', NULL, NULL, NULL, 'S', 1, 1, NULL,
    'U-631571/10', '/SSTRIP/1', '/SSTRIP/S/1', NULL, NULL, 11111,
    NULL);
INSERT INTO rdpoly VALUES (
    26619, 11, 27104, 'SSTRIP', 'SS', NULL, NULL, NULL, 'S', 2, 2, NULL,
    'U-631571/10', '/SSTRIP/2', '/SSTRIP/S/2', NULL, NULL, 11111,
    NULL);
INSERT INTO rdpoly VALUES (
    26625, 11, 27180, 'FTWAY', 'LAF', NULL, NULL, NULL, 'S', 2, 2, NULL,
    'U-631571/10', '/FTWAY/2', '/FTWAY/S/2', NULL, NULL, 99999,
    NULL);
"""


class TestRampMclRecordEditor(QgisTestCase):

    empty_db_path = os.path.join('database_files', 'roadnet_empty.sqlite')
    test_db_path = os.path.join(this_dir, 'roadnet_test.sqlite')
    db = None

    def setUp(self):
        super(TestRampMclRecordEditor, self).setUp()
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

    def tearDown(self):
        super(TestRampMclRecordEditor, self).tearDown()
        if self.db:  # Just in case self.db doesn't get set
            self.db.close()
            del self.db
            QSqlDatabase.removeDatabase('integration_testing')

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_form_fails_on_invalid_record(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=MclSelectorTool)
        mre = ramp_eds.MclRecordEditor(self.db, mock_selection_tool, self.iface)

        # Act and assert
        with self.assertRaises(rn_except.MclFormBadMclRefError):
            mre.setup_model_and_mapper("00000")

    def test_form_populates_from_record(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=MclSelectorTool)
        mre = ramp_eds.MclRecordEditor(self.db, mock_selection_tool, self.iface)
        getters = {'mcl_ref': mre.dlg.ui.mclLineEdit.text,
                   'usrn': mre.dlg.ui.usrnLineEdit.text,
                   'street_classification': mre.dlg.ui.streetClassComboBox.currentText,
                   'ref_1': mre.dlg.ui.ref1LineEdit.text,
                   'ref_2': mre.dlg.ui.ref2LineEdit.text,
                   'lane_number': mre.dlg.ui.laneNumberComboBox.currentText,
                   'carriageway': mre.dlg.ui.carriagewayComboBox.currentText,
                   'rural_urban_id': mre.dlg.ui.ruralUrbanComboBox.currentText,
                   'speed_limit': mre.dlg.ui.speedLimitComboBox.currentText,
                   'section_type': mre.dlg.ui.sectionTypeComboBox.currentText,
                   'section_description': mre.dlg.ui.sectionDescriptionPlainTextEdit.toPlainText}
        expected = {'mcl_ref': '11111',
                    'usrn': '14305470',
                    'street_classification': 'U',
                    'ref_1': 'F-5470',
                    'ref_2': '60',
                    'lane_number': '',
                    'carriageway': 'Single',
                    'rural_urban_id': 'Rural',
                    'speed_limit': '30',
                    'section_type': '',
                    'section_description': 'Test MCL One'}

        # Act
        mre.setup_model_and_mapper("11111")

        # Print model data for debugging
        print("\nData in model:")
        idx = mre.model.index
        model_data = []
        for col in range(mre.model.columnCount() - 1):
            model_data.append(mre.model.data(idx(0, col)))
        pprint.pprint(model_data)

        print("\nData in form")
        for getter in getters:
            print("{}: {}".format(getter, getters[getter]()))

        # Assert
        self.assertEqual(mre.model.data(idx(0, ramp_eds.MCL_REF)), int('11111'))
        for key in getters.keys():
            self.assertEqual(getters[key](), expected[key],
                             "Bad form display for {}. Expected {}, got {}".format(
                                 key, expected[key], getters[key]()))

    def test_save_updates_database(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=MclSelectorTool)
        mre = ramp_eds.MclRecordEditor(self.db, mock_selection_tool, self.iface)
        getters = {'mcl_ref': mre.dlg.ui.mclLineEdit.text,
                   'usrn': mre.dlg.ui.usrnLineEdit.text,
                   'street_classification': mre.dlg.ui.streetClassComboBox.currentText,
                   'ref_1': mre.dlg.ui.ref1LineEdit.text,
                   'ref_2': mre.dlg.ui.ref2LineEdit.text,
                   'lane_number': mre.dlg.ui.laneNumberComboBox.currentText,
                   'carriageway': mre.dlg.ui.carriagewayComboBox.currentText,
                   'rural_urban_id': mre.dlg.ui.ruralUrbanComboBox.currentText,
                   'speed_limit': mre.dlg.ui.speedLimitComboBox.currentText,
                   'section_type': mre.dlg.ui.sectionTypeComboBox.currentText,
                   'section_description': mre.dlg.ui.sectionDescriptionPlainTextEdit.toPlainText}
        one_sixty_chars = ("12345678901234567890123456789012345678901234567890"
                           "12345678901234567890123456789012345678901234567890"
                           "12345678901234567890123456789012345678901234567890"
                           "1234567890")
        expected = {'mcl_ref': '11111',
                    'usrn': '12345678',
                    'street_classification': 'B',
                    'ref_1': 'A9',
                    'ref_2': '30',
                    'lane_number': '4',
                    'carriageway': 'Dual',
                    'rural_urban_id': 'Urban',
                    'speed_limit': '20PT/40',
                    'section_type': '',
                    'section_description': one_sixty_chars[:150]}
        mre.setup_model_and_mapper("11111")

        # Store list of original linked polygons (normally done on dislaying record.
        mre.original_linked_polys = mre.get_linked_polys_in_db("11111")

        # Act
        # Simulate changes
        mre.dlg.ui.usrnLineEdit.setText('12345678')
        mre.dlg.ui.ref1LineEdit.setText('A9')
        mre.dlg.ui.ref2LineEdit.setText('30')

        set_combobox_to_itemtext(mre.dlg.ui.streetClassComboBox, 'B')
        set_combobox_to_itemtext(mre.dlg.ui.laneNumberComboBox, '4')
        set_combobox_to_itemtext(mre.dlg.ui.carriagewayComboBox, 'Dual')
        set_combobox_to_itemtext(mre.dlg.ui.ruralUrbanComboBox, 'Urban')
        set_combobox_to_itemtext(mre.dlg.ui.speedLimitComboBox, '20PT/40')
        set_combobox_to_itemtext(mre.dlg.ui.sectionTypeComboBox, '')

        mre.dlg.ui.sectionDescriptionPlainTextEdit.setPlainText(one_sixty_chars)

        # Press save
        save_button = mre.dlg.ui.buttonBox.button(QDialogButtonBox.Save)
        QTest.mouseClick(save_button, Qt.LeftButton)

        # Assert
        idx = mre.model.index
        for key in getters.keys():
            self.assertEqual(getters[key](), expected[key],
                             "Bad form display for {}. Expected {}, got {}".format(
                                 key, expected[key], getters[key]()))

    def test_cancel_leaves_database_unchanged(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=MclSelectorTool)
        mre = ramp_eds.MclRecordEditor(self.db, mock_selection_tool, self.iface)
        getters = {'mcl_ref': mre.dlg.ui.mclLineEdit.text,
                   'usrn': mre.dlg.ui.usrnLineEdit.text,
                   'street_classification': mre.dlg.ui.streetClassComboBox.currentText,
                   'ref_1': mre.dlg.ui.ref1LineEdit.text,
                   'ref_2': mre.dlg.ui.ref2LineEdit.text,
                   'lane_number': mre.dlg.ui.laneNumberComboBox.currentText,
                   'carriageway': mre.dlg.ui.carriagewayComboBox.currentText,
                   'rural_urban_id': mre.dlg.ui.ruralUrbanComboBox.currentText,
                   'speed_limit': mre.dlg.ui.speedLimitComboBox.currentText,
                   'section_type': mre.dlg.ui.sectionTypeComboBox.currentText,
                   'section_description': mre.dlg.ui.sectionDescriptionPlainTextEdit.toPlainText}
        one_sixty_chars = ("12345678901234567890123456789012345678901234567890"
                           "12345678901234567890123456789012345678901234567890"
                           "12345678901234567890123456789012345678901234567890"
                           "1234567890")
        expected = {'mcl_ref': '11111',
                    'usrn': '14305470',
                    'street_classification': 'U',
                    'ref_1': 'F-5470',
                    'ref_2': '60',
                    'lane_number': '',
                    'carriageway': 'Single',
                    'rural_urban_id': 'Rural',
                    'speed_limit': '30',
                    'section_type': '',
                    'section_description': 'Test MCL One'}
        mre.setup_model_and_mapper("11111")

        # Act
        # Simulate changes
        mre.dlg.ui.usrnLineEdit.setText('12345678')
        mre.dlg.ui.ref1LineEdit.setText('A9')
        mre.dlg.ui.ref2LineEdit.setText('35')

        set_combobox_to_itemtext(mre.dlg.ui.streetClassComboBox, 'B')
        set_combobox_to_itemtext(mre.dlg.ui.laneNumberComboBox, '4')
        set_combobox_to_itemtext(mre.dlg.ui.carriagewayComboBox, 'Dual')
        set_combobox_to_itemtext(mre.dlg.ui.ruralUrbanComboBox, 'Urban')
        set_combobox_to_itemtext(mre.dlg.ui.speedLimitComboBox, '20PT/40')
        set_combobox_to_itemtext(mre.dlg.ui.sectionTypeComboBox, '')

        mre.dlg.ui.sectionDescriptionPlainTextEdit.setPlainText(one_sixty_chars)

        # Press save
        cancel_button = mre.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        QTest.mouseClick(cancel_button, Qt.LeftButton)

        # Assert
        idx = mre.model.index
        for key in getters.keys():
            self.assertEqual(getters[key](), expected[key],
                             "Data changed despite cancel: {}. Expected {}, got {}".format(
                                 key, expected[key], getters[key]()))

    def test_update_db_linked_polys(self):
        """
        Update database with new linked polygons.  27100 should be unchanged, 27104
        removed (values set to null) and 27180 added (some nulled, some new).
        :return:
        """
        # Arrange
        mock_selection_tool = MagicMock(spec=MclSelectorTool)
        mre = ramp_eds.MclRecordEditor(self.db, mock_selection_tool, self.iface)
        original_mcl_data = get_table('mcl', self.db)
        # MCL 11111 initially connected to 27100 and 27104
        mre.select_record(11111)

        mre.get_items_from_linked_poly_box = MagicMock()
        mre.get_items_from_linked_poly_box.return_value = ['27100', '27180']

        expected_rdpoly_data = [
            (21473L, 11L, 27100L, u'SSTRIP', u'SS', None, None, None, u'S', 1L,
             1L, None, u'U-631571/10', u'/SSTRIP/1', u'/SSTRIP/S/1', None,
             None, 11111L),
            (26619L, 11L, 27104L, None, None, None, None, None, None, None,
             None, None, None, None, None, None,
             None, None),
            (26625L, 11L, 27180L, None, None, None, None, None, None, None,
             None, None, 'F-5470/60', None, None, None, None,
             11111L)]

        # Act
        mre.update_db_linked_polys()

        # Assert
        # Check that MCL table is not altered
        self.assertEqual(original_mcl_data, get_table('mcl', self.db))
        # Check that rdpoly table is updated as expected
        self.assertEqual(expected_rdpoly_data, get_table('rdpoly', self.db))


class TestRampRdpolyRecordEditor(QgisTestCase):

    empty_db_path = os.path.join('database_files', 'roadnet_empty.sqlite')
    test_db_path = os.path.join(this_dir, 'roadnet_test.sqlite')
    db = None

    def setUp(self):
        super(TestRampRdpolyRecordEditor, self).setUp()
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

    def tearDown(self):
        super(TestRampRdpolyRecordEditor, self).tearDown()
        if self.db:  # Just in case self.db doesn't get set
            self.db.close()
            del self.db
            QSqlDatabase.removeDatabase('integration_testing')

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_form_fails_on_invalid_record(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=RampSelectorTool)
        rdpre = ramp_eds.RdpolyRecordEditor(self.db, mock_selection_tool, self.iface)

        # Act and assert
        with self.assertRaises(rn_except.RdpolyFormBadRdpolyRefError):
            rdpre.setup_rdpoly_model_and_mapper("00000")
        with self.assertRaises(rn_except.RdpolyFormBadMclRefError):
            rdpre.setup_mcl_model_and_mapper("00000")

    def test_form_populates_from_record(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=RampSelectorTool)
        rdpre = ramp_eds.RdpolyRecordEditor(self.db, mock_selection_tool, self.iface)
        rdpre.dlg.show = MagicMock()
        getters = {'combined_ref': rdpre.dlg.ui.combinedRefLineEdit.text,
                   'element': rdpre.dlg.ui.elementComboBox.currentText,
                   'hierarchy': rdpre.dlg.ui.hierarchyComboBox.currentText,
                   'lane_number': rdpre.dlg.ui.laneNumberLineEdit.text,
                   'length': rdpre.dlg.ui.lengthLineEdit.text,
                   'description': rdpre.dlg.ui.lorDescPlainTextEdit.toPlainText,
                   'mcl': rdpre.dlg.ui.mclLineEdit.text,
                   'desc_3': rdpre.dlg.ui.numberLineEdit.text,
                   'desc_2': rdpre.dlg.ui.offsetComboBox.currentText,
                   'rd_pol_id': rdpre.dlg.ui.rdpolyLineEdit.text,
                   'speed': rdpre.dlg.ui.speedLineEdit.text,
                   'usrn': rdpre.dlg.ui.usrnLineEdit.text}

        expected = {'combined_ref': 'F-5470/60/SSTRIP/S/1',
                    'element': 'Service Strip',
                    'hierarchy': 'Service Strip',
                    'desc_3': '1',
                    'desc_2': 'South',
                    'lane_number': '',
                    'length': '',
                    'description': 'Test MCL One',
                    'mcl': '11111',
                    'rd_pol_id': '27100',
                    'speed': '30',
                    'usrn': '14305470'}

        # Act
        rdpre.select_record("27100")

        # Print model data for debugging
        print("\nData in RdPoly model:")
        idx = rdpre.rdpoly_model.index
        rdpoly_model_data = []
        for col in range(rdpre.rdpoly_model.columnCount() - 1):
            rdpoly_model_data.append(rdpre.rdpoly_model.data(idx(0, col)))
        pprint.pprint(rdpoly_model_data)

        print("\nData in MCL model:")
        idx = rdpre.mcl_model.index
        mcl_model_data = []
        for col in range(rdpre.mcl_model.columnCount() - 1):
            mcl_model_data.append(rdpre.mcl_model.data(idx(0, col)))
        pprint.pprint(mcl_model_data)

        print("\nData in form")
        for getter in getters:
            print("{}: {}".format(getter, getters[getter]()))

        # Assert
        self.assertEqual(rdpre.rdpoly_model.data(idx(0, ramp_eds.RD_POL_ID)), int('27100'))
        for key in getters.keys():
            self.assertEqual(getters[key](), expected[key],
                             "Bad form display for {}. Expected {}, got {}".format(
                                 key, expected[key], getters[key]()))

    def test_save_updates_database(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=RampSelectorTool)
        rdpre = ramp_eds.RdpolyRecordEditor(self.db, mock_selection_tool, self.iface)
        rdpre.dlg.show = MagicMock()
        getters = {'combined_ref': rdpre.dlg.ui.combinedRefLineEdit.text,
                   'element': rdpre.dlg.ui.elementComboBox.currentText,
                   'hierarchy': rdpre.dlg.ui.hierarchyComboBox.currentText,
                   'lane_number': rdpre.dlg.ui.laneNumberLineEdit.text,
                   'length': rdpre.dlg.ui.lengthLineEdit.text,
                   'description': rdpre.dlg.ui.lorDescPlainTextEdit.toPlainText,
                   'mcl': rdpre.dlg.ui.mclLineEdit.text,
                   'desc_3': rdpre.dlg.ui.numberLineEdit.text,
                   'desc_2': rdpre.dlg.ui.offsetComboBox.currentText,
                   'rd_pol_id': rdpre.dlg.ui.rdpolyLineEdit.text,
                   'speed': rdpre.dlg.ui.speedLineEdit.text,
                   'usrn': rdpre.dlg.ui.usrnLineEdit.text}

        expected = [21473L, 11L, 27100L, u'CGWAY', u'LR', QPyNullVariant(int),
                    QPyNullVariant(int), QPyNullVariant(int), u'N', 1L, 1L,
                    QPyNullVariant(int), u'U-631571/10', u'/CGWAY/1', u'/CGWAY/N/1',
                    QPyNullVariant(int), QPyNullVariant(int), 11111L]

        # Act
        rdpre.select_record("27100")
        # Simulate changes
        rdpre.dlg.ui.lengthLineEdit.setText('999')

        set_combobox_to_itemtext(rdpre.dlg.ui.elementComboBox, 'Carriageway')
        set_combobox_to_itemtext(rdpre.dlg.ui.hierarchyComboBox, 'Link Road')
        set_combobox_to_itemtext(rdpre.dlg.ui.offsetComboBox, 'North')

        # Press save
        save_button = rdpre.dlg.ui.buttonBox.button(QDialogButtonBox.Save)
        QTest.mouseClick(save_button, Qt.LeftButton)

        # Print model data for debugging
        print("\nData in RdPoly model:")
        idx = rdpre.rdpoly_model.index
        rdpoly_model_data = []
        for col in range(rdpre.rdpoly_model.columnCount() - 1):
            rdpoly_model_data.append(rdpre.rdpoly_model.data(idx(0, col)))
        pprint.pprint(rdpoly_model_data)

        print("\nData in MCL model:")
        idx = rdpre.mcl_model.index
        mcl_model_data = []
        for col in range(rdpre.mcl_model.columnCount() - 1):
            mcl_model_data.append(rdpre.mcl_model.data(idx(0, col)))
        pprint.pprint(mcl_model_data)

        print("\nData in form")
        for getter in getters:
            print("{}: {}".format(getter, getters[getter]()))

        # Assert
        self.assertEqual(rdpoly_model_data, expected)

    def test_cancel_leaves_database_unchanged(self):
        # Arrange
        mock_selection_tool = MagicMock(spec=RampSelectorTool)
        rdpre = ramp_eds.RdpolyRecordEditor(self.db, mock_selection_tool, self.iface)
        rdpre.dlg.show = MagicMock()
        getters = {'combined_ref': rdpre.dlg.ui.combinedRefLineEdit.text,
                   'element': rdpre.dlg.ui.elementComboBox.currentText,
                   'hierarchy': rdpre.dlg.ui.hierarchyComboBox.currentText,
                   'lane_number': rdpre.dlg.ui.laneNumberLineEdit.text,
                   'length': rdpre.dlg.ui.lengthLineEdit.text,
                   'description': rdpre.dlg.ui.lorDescPlainTextEdit.toPlainText,
                   'mcl': rdpre.dlg.ui.mclLineEdit.text,
                   'desc_3': rdpre.dlg.ui.numberLineEdit.text,
                   'desc_2': rdpre.dlg.ui.offsetComboBox.currentText,
                   'rd_pol_id': rdpre.dlg.ui.rdpolyLineEdit.text,
                   'speed': rdpre.dlg.ui.speedLineEdit.text,
                   'usrn': rdpre.dlg.ui.usrnLineEdit.text}

        expected = [21473L, 11L, 27100L, u'SSTRIP', u'SS', QPyNullVariant(int),
                    QPyNullVariant(int), QPyNullVariant(int), u'S', 1L, 1L,
                    QPyNullVariant(int), u'U-631571/10', u'/SSTRIP/1', u'/SSTRIP/S/1',
                    QPyNullVariant(int), QPyNullVariant(int), 11111L]

        # Act
        rdpre.select_record("27100")
        # Simulate changes
        rdpre.dlg.ui.lengthLineEdit.setText('999')

        set_combobox_to_itemtext(rdpre.dlg.ui.elementComboBox, 'Carriageway')
        set_combobox_to_itemtext(rdpre.dlg.ui.hierarchyComboBox, 'Link Road')
        set_combobox_to_itemtext(rdpre.dlg.ui.offsetComboBox, 'North')

        # Press save
        # Press save
        cancel_button = rdpre.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        QTest.mouseClick(cancel_button, Qt.LeftButton)

        # Print model data for debugging
        print("\nData in RdPoly model:")
        idx = rdpre.rdpoly_model.index
        rdpoly_model_data = []
        for col in range(rdpre.rdpoly_model.columnCount() - 1):
            rdpoly_model_data.append(rdpre.rdpoly_model.data(idx(0, col)))
        pprint.pprint(rdpoly_model_data)

        print("\nData in MCL model:")
        idx = rdpre.mcl_model.index
        mcl_model_data = []
        for col in range(rdpre.mcl_model.columnCount() - 1):
            mcl_model_data.append(rdpre.mcl_model.data(idx(0, col)))
        pprint.pprint(mcl_model_data)

        print("\nData in form")
        for getter in getters:
            print("{}: {}".format(getter, getters[getter]()))

        # Assert
        self.assertEqual(rdpoly_model_data, expected)


def set_combobox_to_itemtext(combobox, itemtext):
    i = combobox.findText(itemtext)
    combobox.setCurrentIndex(i)


def get_table(table, db):
    """
    Get the contents of a database table as a list of tuples.
    :param table: table name
    :param db: QSqlDatabase
    :return: list of tuples
    """
    sql = "SELECT * FROM {};".format(table)
    query = QSqlQuery(sql, db)
    data = []
    while query.next():
        record = query.record()
        # Skip last record that contains geometry
        row = [record.value(i) for i in range(record.count() - 1)]
        data.append(tuple(row))
    return data

if __name__ == '__main__':
    unittest.main()
