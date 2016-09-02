# -*- coding: utf-8 -*-

import qgis.core  # required to get QPyNullVariant to work

from PyQt4.QtSql import (
    QSqlQuery,
    QSqlTableModel)
from PyQt4.QtGui import (
    QDataWidgetMapper,
    QDialogButtonBox,
    QItemDelegate,
    QRegExpValidator,
    QTextCursor)
from PyQt4.QtCore import Qt, QRegExp, QPyNullVariant
from Roadnet.roadnet_dialog import (RampMclEditorDlg, RampRdpolyEditorDlg)
import Roadnet.ramp.length_of_roads as lor
from Roadnet.ramp.selector_tools import EditLinkedPolysTool
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.generic_functions import ipdb_breakpoint
from Roadnet import config

# Create 'enum' like aliases for column names
# mcl
(PK_UID, ESU, SYMBOL, USRN, REC_TYPE, DESC_TEXT, LOCALITY,
 TOWN, ENTRY_DATE, TYP_3_USRN, TYP_3_DESC, TYP_4_USRN, TYP_4_DESC,
 LOR_REF_1, LOR_REF_2, LOR_DESC, LANE_NUMBER, SPEED_LIMIT,
 RURAL_URBAN_ID, SECTION_TYPE, ADOPTION_STATUS, MCL_REF, STREET_CLASS,
 IN_PILOT, CARRIAGEWAY) = range(25)
# rdpoly
(RD_POL_ID, ELEMENT, HIERARCHY, OFFSET, DESC_3, REF_3, LABEL, LABEL1) = (
    2, 3, 4, 8, 9, 10, 13, 14)

# Define valid entries for dropdowns
STREET_CLASS_VALUES = ['A', 'B', 'C', 'U', 'AT', 'M']
LANE_NUMBER_VALUES = ["{}".format(x) for x in [1, 2, 3, 4, 5, 6]]
CARRIAGEWAY_VALUES = ["Single", "Dual"]
RURAL_URBAN_VALUES = ['Rural', 'Urban']
SPEED_LIMIT_VALUES = ["20PT/30", "20PT/40", "20PT/50", "20PT/60", "20",
                      "30", "40", "50", "60", "70"]
SECTION_TYPE_VALUES = ["Carriageway", "Footpath"]
HIERARCHY_VALUES = ['Local Access Footway', 'Local Access Road',
                    'Link Footway', 'Link Road', 'Main Distributor', 'Motorway',
                    'Primary Walking Route', 'Prestige Walking Zone',
                    'Secondary Distributor', 'Strategic Route', 'Service Strip',
                    'Secondary Walking Route']
ELEMENT_VALUES = ['Adopted Carpark', 'Parking', 'Carriageway',
                  'Central Reserve', 'Footpath', 'Footway',
                  'Landscaping (Hard)', 'Landscaping (Soft)', 'Service Strip',
                  'Verge', 'Cycleway / Path']
OFFSET_VALUES = ['North', 'South', 'East', 'West']


class MclRecordEditor(object):
    """
    Handles forms and database connections for editing RAMP features.
    """
    edit_linked_polys_tool = None
    original_linked_polys = None
    mcl_ref = None
    dlg = None
    model = None
    mapper = None

    def __init__(self, db, selector_tool, iface):
        self.db = db
        self.selector_tool = selector_tool
        self.iface = iface
        self.prepare_dialog()
        self.connect_signals()

    def prepare_dialog(self):
        """
        Prepare MCL edit dialog including setting comobox entries and
        validation.
        :return: RampMclEditorDlg
        """
        self.dlg = RampMclEditorDlg()
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg.move(5, 5)
        self.set_combobox_items()
        self.set_dialog_validators()

    def set_combobox_items(self):
        """
        Populate the items in the comboboxes.
        """
        self.dlg.ui.streetClassComboBox.addItems([''] + STREET_CLASS_VALUES)
        self.dlg.ui.laneNumberComboBox.addItems([''] + LANE_NUMBER_VALUES)
        self.dlg.ui.carriagewayComboBox.addItems([''] + CARRIAGEWAY_VALUES)
        self.dlg.ui.ruralUrbanComboBox.addItems([''] + RURAL_URBAN_VALUES)
        self.dlg.ui.speedLimitComboBox.addItems([''] + SPEED_LIMIT_VALUES)
        self.dlg.ui.sectionTypeComboBox.addItems([''] + SECTION_TYPE_VALUES)

    def set_dialog_validators(self):
        """
        Add validators to the free-text fields of the dialog.
        """
        # These widgets are 'free-text'
        self.dlg.ui.usrnLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"\d{0,8}")))
        self.dlg.ui.ref1LineEdit.setValidator(
            QRegExpValidator(QRegExp(r"[ABCUFTMZ]{1,2}-?\d{0,}")))
        self.dlg.ui.ref2LineEdit.setValidator(
            QRegExpValidator(QRegExp(r"\d{0,}")))

        # There isn't length validation for plain text edit, so implement our own
        self.dlg.ui.sectionDescriptionPlainTextEdit.textChanged.connect(
            self.trim_section_description)

    def trim_section_description(self):
        """
        Trim text in street section description to within 150 characters.
        """
        editor = self.dlg.ui.sectionDescriptionPlainTextEdit
        text = editor.toPlainText()
        if len(text) > 150:
            text = text[:150]
            editor.setPlainText(text)
            editor.moveCursor(QTextCursor.End)

    def connect_signals(self):
        """
        Connect GUI signals and slots.  Extends parent class function
        """
        # GUI controls
        self.selector_tool.selected_id.connect(self.select_record)
        save_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Save)
        cancel_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        save_button.clicked.connect(self.save_record)
        cancel_button.clicked.connect(self.close_tool)
        self.dlg.rejected.connect(self.close_tool)
        self.dlg.ui.editLinksPushButton.clicked.connect(
            self.launch_edit_linked_polys_tool)

        # Auto updates on combined ref line edit
        self.dlg.ui.ref1LineEdit.textChanged.connect(self.update_combined_ref)
        self.dlg.ui.ref2LineEdit.textChanged.connect(self.update_combined_ref)

    def select_record(self, mcl_ref):
        """
        Update the GUI to populate with data from the chosen record.  Show if
        not already visible.
        :param mcl_ref: int, emitted by selector_tool
        """
        self.mcl_ref = mcl_ref
        self.setup_model_and_mapper(mcl_ref)
        self.populate_length_lineedit(mcl_ref)
        self.original_linked_polys = self.get_linked_polys_in_db(mcl_ref)
        self.set_linked_poly_box_items(self.original_linked_polys)

        if not self.dlg.isVisible():
            self.dlg.show()

    def launch_edit_linked_polys_tool(self):
        """
        Create new instance of edit linked polys tool for current record
        """
        linked_polys = self.get_items_from_linked_poly_box()
        self.edit_linked_polys_tool = EditLinkedPolysTool(linked_polys,
                                                          self.iface,
                                                          self.dlg)
        self.edit_linked_polys_tool.linked_polys_updated.connect(
            self.set_linked_poly_box_items)
        self.edit_linked_polys_tool.launch()

    def close_tool(self):
        """
        Close the dialog, reverting unsaved changes.
        """
        self.mapper.revert()
        self.dlg.hide()

    def save_record(self):
        """
        Save changes to the record, then close dialog.
        """
        self.mapper.submit()
        self.update_db_linked_polys()
        self.iface.mapCanvas().refresh()
        self.dlg.hide()

    def setup_model_and_mapper(self, mcl_ref):
        """
        Load the table data for selected record into a model and map to widgets.
        """
        # Set up model
        self.model = QSqlTableModel(db=self.db)
        self.model.setTable('mcl')
        self.model.setFilter("mcl_ref = {}".format(int(mcl_ref)))
        self.model.select()
        if self.model.rowCount() != 1:
            msg = "MCL query for mcl_ref = {} returned {} rows".format(
                mcl_ref, self.model.rowCount())
            raise rn_except.MclFormBadMclRefError(msg)

        # Set up mapper
        self.mapper = QDataWidgetMapper()
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.dlg.ui.mclLineEdit, MCL_REF)
        self.mapper.addMapping(self.dlg.ui.usrnLineEdit, USRN)
        self.mapper.addMapping(self.dlg.ui.streetClassComboBox, STREET_CLASS)
        self.mapper.addMapping(self.dlg.ui.ref1LineEdit, LOR_REF_1)
        self.mapper.addMapping(self.dlg.ui.ref2LineEdit, LOR_REF_2)
        self.mapper.addMapping(self.dlg.ui.laneNumberComboBox, LANE_NUMBER)
        self.mapper.addMapping(self.dlg.ui.carriagewayComboBox, CARRIAGEWAY)
        self.mapper.addMapping(self.dlg.ui.ruralUrbanComboBox, RURAL_URBAN_ID)
        self.mapper.addMapping(self.dlg.ui.speedLimitComboBox, SPEED_LIMIT)
        self.mapper.addMapping(self.dlg.ui.sectionTypeComboBox, SECTION_TYPE)
        self.mapper.addMapping(self.dlg.ui.sectionDescriptionPlainTextEdit, LOR_DESC)
        self.mapper.setItemDelegate(MclEditorDelegate(self.dlg))
        self.mapper.toFirst()

    def update_combined_ref(self):
        """
        Update combinedRefLineEdit with value derived from other fields.
        """
        ref1 = self.dlg.ui.ref1LineEdit.text()
        ref2 = self.dlg.ui.ref2LineEdit.text()
        new_text = "{}/{}".format(ref1, ref2)

        self.dlg.ui.combinedRefLineEdit.setText(new_text)

    def populate_length_lineedit(self, mcl_ref):
        """
        Calculate the length of the MCL and populate lineedit with data.
        :param mcl_ref: int, id of the MCL to calculate
        """
        # Don't do calculation if spatialite version is too low. (libgeos bug)
        if lor.get_spatialite_version_as_int(self.db) < 430:
            length_text = "Spatialite < 4.3.0"
            self.dlg.ui.lengthLineEdit.setText(length_text)
            return

        # Run query
        sql = """
            SELECT GLength(geometry) AS length FROM mcl
            WHERE mcl_ref = {}
            ;""".format(mcl_ref)
        query = QSqlQuery(sql, self.db)

        # Raise exception if query fails
        if not query.first():
            msg = ("Could not calculate MCL length.  Query:\n{}\n"
                   "Database returned:\n{}".format(sql,
                                                   query.lastError().text()))
            raise rn_except.MclFormLengthCalculationError(msg)

        # Update field
        length = query.record().value('length')
        length_text = "{:.2f}".format(length)
        self.dlg.ui.lengthLineEdit.setText(length_text)

    def update_db_linked_polys(self):
        """
        Update the database with changes to linked polygons.
        """
        linked_polys = self.get_items_from_linked_poly_box()

        # Clear links for polygons that have been removed
        for polygon in self.original_linked_polys:
            if polygon not in linked_polys:
                self.clear_rdpoly_mcl_fields(polygon)

        # Create links for polygons that have been added.
        for polygon in linked_polys:
            if polygon not in self.original_linked_polys:
                self.clear_rdpoly_mcl_fields(polygon)
                self.set_rdpoly_mcl_links_in_db(polygon, self.mcl_ref)

    def get_items_from_linked_poly_box(self):
        """
        Get the values from the Linked Polygons box
        :return: list of strings
        """
        poly_box = self.dlg.ui.linkedPolygonsListWidget
        items = []
        for i in range(poly_box.count()):
            items.append(poly_box.item(i).data(Qt.DisplayRole))
        return items

    def set_linked_poly_box_items(self, items):
        """
        Populate the Linked Polygons box with items
        :param items: list of strings
        """
        # Cannot link already linked polygon
        try:
            self.validate_polygon_links(items)
        except rn_except.RampRdPolyAlreadyLinkedPopupError:
            # Don't update if polygons already have links to other MCLs
            return

        poly_box = self.dlg.ui.linkedPolygonsListWidget
        poly_box.clear()
        poly_box.addItems(items)

    def validate_polygon_links(self, linked_polys):
        """
        Raise exception if any polygons have link to other MCLs.
        """
        already_linked = []
        for rd_pol_id in linked_polys:
            linked_mcl_cref = self.get_mcl_cref(rd_pol_id)

            if linked_mcl_cref == str(self.mcl_ref):
                # OK if linked to current MCL
                continue
            elif linked_mcl_cref in ('', 'NULL', 'Null'):
                # Null is OK
                continue
            else:
                # Otherwise already linked to other polygon
                already_linked.append(rd_pol_id)

        if already_linked:
            msg = "Cannot update links.  The following polygons are already linked"
            msg += " to other MCLs.\n\n"
            msg += ", ".join(already_linked)
            raise rn_except.RampRdPolyAlreadyLinkedPopupError(msg)

    def get_mcl_cref(self, rd_pol_id):
        """
        Get the MCL ref attached to given polygon
        :param rd_pol_id:
        :return: str, mcl_cref
        """
        sql = """
            SELECT mcl_cref FROM rdpoly
            WHERE rd_pol_id = '{}'
            ;""".format(rd_pol_id)
        query = QSqlQuery(sql, self.db)

        if not query.isActive():
            msg = "Invalid rd_pol_id:"
            msg += "\n\nSQL command:\n\n{}".format(sql)
            msg += "\n\nDatabase reply:\n\n{}".format(query.lastError().text())
            raise rn_except.RampRdPolyUpdateFailedPopupError(msg)

        query.first()
        mcl_ref = str(query.record().value('mcl_cref'))

        return mcl_ref

    def get_linked_polys_in_db(self, mcl_ref):
        """
        Get the polygons that have current mcl_ref
        :param mcl_ref: str with reference
        :return: list of strings
        """
        sql = """
            SELECT rd_pol_id FROM rdpoly
            WHERE mcl_cref = {}
            ;""".format(mcl_ref)
        query = QSqlQuery(sql, self.db)

        linked_polys = []
        while query.next():
            record = query.record()
            rd_pol_id = str(record.value('rd_pol_id'))
            linked_polys.append(rd_pol_id)

        return linked_polys

    def set_rdpoly_mcl_links_in_db(self, rd_pol_id, mcl_ref):
        """
        Update the fields of the rdpoly table with values for the given
        mcl_ref from the mcl table.
        :param rd_pol_id: str, rd_pol_id to update
        :param mcl_ref: str, mcl_ref to supply values
        """
        if config.DEBUG_MODE:
            print("DEBUG_MODE: Updating rdpoly {} with data from mcl {}".format(rd_pol_id, mcl_ref))

        # Get update values
        mcl_attrs = self.get_mcl_attrs_for_rdpoly(mcl_ref)
        mcl_attrs['mcl_ref'] = mcl_ref
        mcl_attrs['rd_pol_id'] = rd_pol_id

        # Update database
        sql = """
            UPDATE rdpoly SET part_label = "{part_label}",
                 mcl_cref = {mcl_cref}
            WHERE rd_pol_id = {rd_pol_id}
            ;""".format(**mcl_attrs)
        if config.DEBUG_MODE:
            print(sql)
        query = QSqlQuery(sql, self.db)

        if not query.isActive():
            msg = "Failed to update rdpoly with mcl data."
            msg += "\n\nSQL command:\n\n{}".format(sql)
            msg += "\n\nDatabase reply:\n\n{}".format(query.lastError().text())
            raise rn_except.RampRdPolyUpdateFailedPopupError(msg)

    def clear_rdpoly_mcl_fields(self, rd_pol_id):
        """
        Clear values in rdpoly that were derived from linked MCL.  Used when
        MCL is unlinked.
        :param rd_pol_id: str, rd_pol_id
        """
        sql = """
            UPDATE rdpoly SET
                element = NULL, hierarchy = NULL,
                ref_1 = NULL, ref_2 = NULL, ref_3 = NULL,
                desc_1 = NULL, desc_2 = NULL, desc_3 = NULL,
                part_label = NULL, label = NULL, label1 = NULL,
                feature_length = NULL, r_usrn = NULL, mcl_cref = NULL
            WHERE rd_pol_id = {}
            ;""".format(rd_pol_id)
        if config.DEBUG_MODE:
            print(sql)
        query = QSqlQuery(sql, self.db)

        if not query.isActive():
            msg = "Problem updating rdpoly with mcl data."
            msg += "\n\nSQL command:\n\n{}".format(sql)
            msg += "\n\nDatabase reply:\n\n{}".format(query.lastError().text())
            raise rn_except. RampRdPolyUpdateFailedPopupError(msg)

    def get_mcl_attrs_for_rdpoly(self, mcl_ref):
        """
        Get values from database and prepare attributes to insert into rdpoly
        table.
        :param mcl_ref: str, mcl_ref
        :return: dict, mcl_attributes
        """
        sql = """
            SELECT lor_ref_1 || "/" || lor_ref_2 AS part_label
            FROM mcl WHERE mcl_ref={};""".format(mcl_ref)
        query = QSqlQuery(sql, self.db)

        if not query.isActive():
            msg = "Failed to get MCL attributes."
            msg += "\n\nSQL command:\n\n{}".format(sql)
            msg += "\n\nDatabase reply:\n\n{}".format(query.lastError().text())
            raise rn_except. RampRdPolyUpdateFailedPopupError(msg)

        query.first()
        part_label = query.record().value("part_label")
        mcl_attrs = {'mcl_cref': mcl_ref, 'part_label': part_label}

        return mcl_attrs


class MclEditorDelegate(QItemDelegate):
    """
    Changes the way that database model data are presented in GUI and returned
    to the database.  Includes mappings for 'keys' where database values don't
    match combobox displays.
    """
    rural_urban_codes = {'R': 'Rural',
                         'U': 'Urban'}
    section_type_codes = {'CW': 'Carriageway',
                          'FT': 'Footpath'}

    def setEditorData(self, editor, index):
        """
        Changes how model data are displayed in widget.
        :param editor: QWidget used for editing
        :param index: QModelIndex, index for model
        """
        if index.column() in (STREET_CLASS, LANE_NUMBER, CARRIAGEWAY,
                              SPEED_LIMIT):
            text = str(index.model().data(index, Qt.DisplayRole))
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        elif index.column() == RURAL_URBAN_ID:
            set_combobox_to_model_value(editor, index,
                                        self.rural_urban_codes)
        elif index.column() == SECTION_TYPE:
            set_combobox_to_model_value(editor, index,
                                        self.section_type_codes)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """
        Changes how model data is populated from displayed values.
        :param editor: QWidget, custom editor widget
        :param model: QAbstractItemModel, model
        :param index: QModelIndex, model index
        """
        if index.column() in (STREET_CLASS, LANE_NUMBER, CARRIAGEWAY,
                              SPEED_LIMIT):
            model.setData(index, editor.currentText())

        elif index.column() == RURAL_URBAN_ID:
            set_model_value_from_combobox(editor, model, index,
                                          self.rural_urban_codes)
        elif index.column() == SECTION_TYPE:
            set_model_value_from_combobox(editor, model, index,
                                          self.section_type_codes)
        else:
            QItemDelegate.setModelData(self, editor, model, index)


class RdpolyRecordEditor(object):
    """
    Handles forms and database connections for editing RAMP features.
    """
    dlg = None
    rdpoly_model = None
    rdpoly_mapper = None
    mcl_model = None
    mcl_mapper = None

    def __init__(self, db, selector_tool, iface):
        self.db = db
        self.selector_tool = selector_tool
        self.iface = iface
        self.prepare_dialog()
        self.connect_signals()

    def prepare_dialog(self):
        """
        Prepare MCL edit dialog including setting comobox entries and
        validation.
        :return: RampMclEditorDlg
        """
        self.dlg = RampRdpolyEditorDlg()
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg.move(5, 5)
        self.set_combobox_items()
        self.set_dialog_validators()

    def set_combobox_items(self):
        """
        Populate the items in the comboboxes.
        """
        self.dlg.ui.elementComboBox.addItems([''] + ELEMENT_VALUES)
        self.dlg.ui.hierarchyComboBox.addItems([''] + HIERARCHY_VALUES)
        self.dlg.ui.offsetComboBox.addItems([''] + OFFSET_VALUES)

    def set_dialog_validators(self):
        """
        Add validators to the free-text fields of the dialog.
        """
        self.dlg.ui.numberLineEdit.setValidator(
            QRegExpValidator(QRegExp(r"\d{0,3}")))

    def connect_signals(self):
        """
        Connect GUI signals and slots.  Extends parent class function
        """
        # GUI controls
        self.selector_tool.selected_id.connect(self.select_record)
        save_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Save)
        cancel_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        save_button.clicked.connect(self.save_record)
        cancel_button.clicked.connect(self.close_tool)
        # reject() is called if user presses escape
        self.dlg.rejected.connect(self.close_tool)

        # Auto updates on combined ref line edit
        self.dlg.ui.numberLineEdit.textChanged.connect(self.update_combined_ref)
        self.dlg.ui.elementComboBox.currentIndexChanged.connect(
            self.update_combined_ref)
        self.dlg.ui.elementComboBox.currentIndexChanged.connect(
            self.set_length_readonly_state)
        self.dlg.ui.hierarchyComboBox.currentIndexChanged.connect(
            self.update_combined_ref)
        self.dlg.ui.offsetComboBox.currentIndexChanged.connect(
            self.update_combined_ref)

    def select_record(self, rd_pol_id):
        """
        Update the GUI to populate with data from the chosen record.  Show if
        not already visible.
        :param rd_pol_id: int, emitted by selector_tool
        """
        try:
            self.setup_models_and_mappers(rd_pol_id)
        except rn_except.RampNoLinkedPolyPopupError:
            return

        self.set_length_readonly_state()

        if not self.dlg.isVisible():
            # Emit the index changed symbol so update_combined_ref() is triggered,
            # ensuring combined ref box is populated on initial load
            self.dlg.ui.elementComboBox.currentIndexChanged.emit(
                self.dlg.ui.elementComboBox.currentIndex())
            self.dlg.show()

    def close_tool(self):
        """
        Close the dialog, reverting unsaved changes.
        """
        self.mcl_mapper.revert()
        self.rdpoly_mapper.revert()
        self.dlg.hide()

    def save_record(self):
        """
        Save changes to the record, then close dialog.
        """
        self.mcl_mapper.submit()
        self.rdpoly_mapper.submit()
        self.update_label_fields()
        self.update_ref_3()
        self.iface.mapCanvas().refresh()
        self.dlg.hide()

    def setup_models_and_mappers(self, rd_pol_id):
        """
        Load the table data for selected record into a model and map to widgets.
        """
        self.setup_rdpoly_model_and_mapper(rd_pol_id)
        mcl_ref = self.get_mcl_ref_from_rd_pol_id(rd_pol_id)
        self.setup_mcl_model_and_mapper(mcl_ref)

    def get_mcl_ref_from_rd_pol_id(self, rd_pol_id):
        """
        Query database to get mcl_ref associated with given polygon
        :param rd_pol_id: str, id number
        :return mcl_ref: str, id number
        """
        sql = """
            SELECT mcl_cref FROM rdpoly
            WHERE rd_pol_id = {}""".format(rd_pol_id)
        query = QSqlQuery(sql, self.db)

        if not query.first():
            msg = "No MCLs are linked to polygon {}".format(rd_pol_id)
            raise rn_except.RampNoLinkedPolyPopupError(msg)

        mcl_ref = query.record().value('mcl_cref')
        if isinstance(mcl_ref, QPyNullVariant):
            msg = "No MCLs are linked to polygon {}".format(rd_pol_id)
            raise rn_except.RampNoLinkedPolyPopupError(msg)

        return str(mcl_ref)

    def set_length_readonly_state(self):
        """
        Make the length lineedit writeable for non-MCL fields
        """
        element_value = self.dlg.ui.elementComboBox.currentText()
        delegate = self.rdpoly_mapper.itemDelegate()
        element_key = get_key(delegate.element_codes, element_value)

        if element_key in ('CGWAY', 'FPATH'):
            self.dlg.ui.lengthLineEdit.setReadOnly(True)
            self.dlg.ui.lengthLineEdit.setStyleSheet("""
                border-width: 0.5px;
                border-style: solid;
                border-radius: 2px;
                border-color: rgb(100, 100, 100);
                background-color: rgb(213, 234, 234);""")
        else:
            self.dlg.ui.lengthLineEdit.setReadOnly(False)
            self.dlg.ui.lengthLineEdit.setStyleSheet("")

    def update_label_fields(self):
        """
        Update the label columns of the rdpoly table based on new values
        """
        element = self.rdpoly_data(ELEMENT)
        side = self.rdpoly_data(OFFSET)
        number = self.rdpoly_data(DESC_3)
        if isinstance(number, QPyNullVariant) or number in (0, ''):
            label = "/{}".format(element)
            label1 = "/{}/{}".format(element, side)
        else:
            label = "/{}/{}".format(element, number)
            label1 = "/{}/{}/{}".format(element, side, number)

        self.rdpoly_model.setData(self.rdpoly_model.index(0, LABEL), label)
        self.rdpoly_model.setData(self.rdpoly_model.index(0, LABEL1), label1)
        self.rdpoly_model.submit()

    def update_ref_3(self):
        """
        Update the ref_3 column of rdpoly with value from desc_3.
        """
        number = self.rdpoly_data(DESC_3)
        self.rdpoly_model.setData(self.rdpoly_model.index(0, REF_3), number)
        self.rdpoly_model.submit()

    def setup_rdpoly_model_and_mapper(self, rd_pol_id):
        """
        Load the data for the Polygon portion of the form
        :param rd_pol_id: str rd_pol_id
        :return:
        """
        # Set up model
        self.rdpoly_model = QSqlTableModel(db=self.db)
        self.rdpoly_model.setTable('rdpoly')
        self.rdpoly_model.setFilter("rd_pol_id = {}".format(int(rd_pol_id)))
        self.rdpoly_model.select()
        if self.rdpoly_model.rowCount() != 1:
            msg = "Table rdpoly query for rd_pol_id = {} returned {} rows".format(
                rd_pol_id, self.rdpoly_model.rowCount())
            raise rn_except.RdpolyFormBadRdpolyRefError(msg)

        # Set up rdpoly_mapper
        self.rdpoly_mapper = QDataWidgetMapper()
        self.rdpoly_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.rdpoly_mapper.setModel(self.rdpoly_model)
        self.rdpoly_mapper.addMapping(self.dlg.ui.rdpolyLineEdit, RD_POL_ID)
        self.rdpoly_mapper.addMapping(self.dlg.ui.numberLineEdit, DESC_3)
        self.rdpoly_mapper.addMapping(self.dlg.ui.elementComboBox, ELEMENT)
        self.rdpoly_mapper.addMapping(self.dlg.ui.hierarchyComboBox, HIERARCHY)
        self.rdpoly_mapper.addMapping(self.dlg.ui.offsetComboBox, OFFSET)
        self.rdpoly_mapper.setItemDelegate(RdpolyEditorDelegate(self.dlg))
        self.rdpoly_mapper.toFirst()

    def setup_mcl_model_and_mapper(self, mcl_ref):
        """
        Load the data for the MCL portion of the form
        :param mcl_ref: str mcl_ref
        :return:
        """
        # Set up model
        self.mcl_model = QSqlTableModel(db=self.db)
        self.mcl_model.setTable('mcl')
        self.mcl_model.setFilter("mcl_ref = {}".format(int(mcl_ref)))
        self.mcl_model.select()
        if self.mcl_model.rowCount() != 1:
            msg = "MCL query for mcl_ref = {} returned {} rows".format(
                mcl_ref, self.mcl_model.rowCount())
            raise rn_except.RdpolyFormBadMclRefError(msg)

        # Set up mcl_mapper
        self.mcl_mapper = QDataWidgetMapper()
        self.mcl_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mcl_mapper.setModel(self.mcl_model)
        self.mcl_mapper.addMapping(self.dlg.ui.mclLineEdit, MCL_REF)
        self.mcl_mapper.addMapping(self.dlg.ui.usrnLineEdit, USRN)
        self.mcl_mapper.addMapping(self.dlg.ui.lorDescPlainTextEdit, LOR_DESC)
        self.mcl_mapper.addMapping(self.dlg.ui.laneNumberLineEdit, LANE_NUMBER)
        self.mcl_mapper.addMapping(self.dlg.ui.speedLineEdit, SPEED_LIMIT)
        self.mcl_mapper.toFirst()

    def update_combined_ref(self):
        """
        Update combinedRefLineEdit with value derived from other fields.
        """
        if self.mcl_model is None:
            # This happens if signal calls function before model created
            return

        # Get strings from MCLs
        mcl_ref1 = self.mcl_data(LOR_REF_1)
        mcl_ref2 = self.mcl_data(LOR_REF_2)

        # Get strings from rdpoly
        delegate = self.rdpoly_mapper.itemDelegate()
        element_value = self.dlg.ui.elementComboBox.currentText()
        element_key = get_key(delegate.element_codes, element_value)
        offset_value = self.dlg.ui.offsetComboBox.currentText()
        offset_key = get_key(delegate.offset_codes, offset_value)
        number = self.dlg.ui.numberLineEdit.text()

        new_text = "{}/{}/{}/{}/{}".format(mcl_ref1, mcl_ref2, element_key,
                                           offset_key, number)
        self.dlg.ui.combinedRefLineEdit.setText(new_text)

    def rdpoly_data(self, column):
        return self.rdpoly_model.data(self.rdpoly_model.index(0, column))

    def mcl_data(self, column):
        return self.mcl_model.data(self.mcl_model.index(0, column))


def get_key(dictionary, value):
    """
    Get the key corresponding to a dictionary value.
    :param dictionary: dict
    :param value: str, value text
    :return: str, key
    """
    if value == '':
        return ''

    for k, v in dictionary.iteritems():
        if v == value:
            return k


class RdpolyEditorDelegate(QItemDelegate):
    """
    Changes the way that database model data are presented in GUI and returned
    to the database.  Includes mappings for 'keys' where database values don't
    match combobox displays.
    """
    hierarchy_codes = {'LAF': 'Local Access Footway',
                       'LAR': 'Local Access Road',
                       'LF': 'Link Footway',
                       'LR': 'Link Road',
                       'MD': 'Main Distributor',
                       'MW': 'Motorway',
                       'PWR': 'Primary Walking Route',
                       'PWZ': 'Prestige Walking Zone',
                       'SD': 'Secondary Distributor',
                       'SR': 'Strategic Route',
                       'SS': 'Service Strip',
                       'SWR': 'Secondary Walking Route'}
    element_codes = {'ACARPK': 'Adopted Carpark',
                     'CARPK': 'Parking',
                     'CGWAY': 'Carriageway',
                     'CRESERVE': 'Central Reserve',
                     'FPATH': 'Footpath',
                     'FTWAY': 'Footway',
                     'LSHARD': 'Landscaping (Hard)',
                     'LSSOFT': 'Landscaping (Soft)',
                     'SSTRIP': 'Service Strip',
                     'VERGE': 'Verge',
                     'CYCLE': 'Cycleway / Path'}
    offset_codes = {'N': 'North',
                    'S': 'South',
                    'E': 'East',
                    'W': 'West'}

    def setEditorData(self, editor, index):
        """
        Changes how model data are displayed in widget.
        :param editor: QWidget used for editing
        :param index: QModelIndex, index for model
        """
        if index.column() == ELEMENT:
            set_combobox_to_model_value(editor, index,
                                        self.element_codes)
        elif index.column() == HIERARCHY:
            set_combobox_to_model_value(editor, index,
                                        self.hierarchy_codes)
        elif index.column() == OFFSET:
            set_combobox_to_model_value(editor, index,
                                        self.offset_codes)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """
        Changes how model data is populated from displayed values.
        :param editor: QWidget, custom editor widget
        :param model: QAbstractItemModel, model
        :param index: QModelIndex, model index
        """
        if index.column() == ELEMENT:
            set_model_value_from_combobox(editor, model, index,
                                          self.element_codes)
        elif index.column() == HIERARCHY:
            set_model_value_from_combobox(editor, model, index,
                                          self.hierarchy_codes)
        elif index.column() == OFFSET:
            set_model_value_from_combobox(editor, model, index,
                                          self.offset_codes)
        else:
            QItemDelegate.setModelData(self, editor, model, index)


def set_combobox_to_model_value(editor, index, code_map):
    """
    Set combobox editor value to match value in model
    :param editor:
    :param index:
    :param code_map:
    """
    try:
        model_text = str(index.model().data(index, Qt.DisplayRole))
        display_text = code_map[model_text]
        i = editor.findText(display_text)
        if i == -1:
            i = 0
        editor.setCurrentIndex(i)
    except KeyError:
        editor.setCurrentIndex(0)


def set_model_value_from_combobox(editor, model, index, code_map):
    """
    Set model data based on value in combobox
    :param editor:
    :param model:
    :param index:
    :param code_map:
    """
    display_text = editor.currentText()

    if display_text == '':
        model.setData(index, QPyNullVariant)
        return

    # Loop back through dictionary to find model key
    for k, v in code_map.iteritems():
        if v == display_text:
            model_text = k
            model.setData(index, model_text)

