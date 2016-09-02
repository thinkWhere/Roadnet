# -*- coding: utf-8 -*-
import datetime
import operator

from PyQt4.QtCore import Qt, QDate, QObject, pyqtSignal
from PyQt4.QtGui import QMessageBox, QColor, QListWidgetItem, QLineEdit, QDoubleValidator
from PyQt4.QtSql import QSqlQuery
from qgis.core import QgsMapLayerRegistry, QgsPoint, QgsFeatureRequest
from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker

from mod_validation import ValidateDescription, ValidateStreetType
from ..generic_functions import ZoomSelectCanvas, MapLookupValues, SwitchStreetBrowserMode, ipdb_breakpoint
from ..roadnet_dialog import SaveRecordDlg, EditCoordsDlg, EditEsuLinkDlg
from .. import config

__author__ = 'matthew.walsh'


class EditRecord:
    """
    Makes changes to forms for editing/adding records, also deals with committing edits to the db
    """

    def __init__(self, iface, street_browser, model, mapper, db, params):
        self.street_browser = street_browser
        self.iface = iface
        self.model = model
        self.mapper = mapper
        self.db = db
        self.params = params
        self.canvas_functs = ZoomSelectCanvas(self.iface, self.street_browser, self.db)
        self.edit_signals = EditSignals()
        self.esu_layer = None

        self.update_dict = {4: (self.street_browser.ui.recordTypeComboBox, self.street_browser.ui.typeLineEdit),
                            20: (self.street_browser.ui.localityComboBox, self.street_browser.ui.localityLineEdit),
                            22: (self.street_browser.ui.townComboBox, self.street_browser.ui.townLineEdit),
                            21: (self.street_browser.ui.countyComboBox, self.street_browser.ui.countyLineEdit),
                            9: (self.street_browser.ui.authorityComboBox, self.street_browser.ui.authorityLineEdit),
                            17: (self.street_browser.ui.stateComboBox, self.street_browser.ui.stateLineEdit),
                            19: (self.street_browser.ui.classComboBox, self.street_browser.ui.classLineEdit),
                            8: (self.street_browser.ui.startDateDateEdit, self.street_browser.ui.startDateLineEdit),
                            7: (self.street_browser.ui.updateDateLineEdit, self.street_browser.ui.updateDateLineEdit),
                            2: (self.street_browser.ui.versionLineEdit, self.street_browser.ui.versionLineEdit),
                            5: (self.street_browser.ui.descriptionTextEdit, self.street_browser.ui.descriptionTextEdit),
                            6: (self.street_browser.ui.entryDateLineEdit, self.street_browser.ui.entryDateLineEdit)}

        self.query_lst = {
            "SELECT name, town_ref FROM tlkpTOWN": self.street_browser.ui.townComboBox,
            "SELECT state_desc, state_ref FROM tlkpSTREET_STATE": self.street_browser.ui.stateComboBox,
            "SELECT description, street_ref FROM tlkpSTREET_REF_TYPE": self.street_browser.ui.recordTypeComboBox,
            "SELECT name, loc_ref FROM tlkpLOCALITY": self.street_browser.ui.localityComboBox,
            "SELECT name, county_ref from tlkpCOUNTY": self.street_browser.ui.countyComboBox,
            "SELECT description, auth_code FROM tlkpAUTHORITY": self.street_browser.ui.authorityComboBox,
            "SELECT street_classification, class_ref from tlkpSTREET_CLASS": self.street_browser.ui.classComboBox}

        # Populate comboboxes
        self.populate_combos()

        # Create save dlg instance and connect buttons
        self.save_dlg = SaveRecordDlg()
        self.save_dlg.ui.savePushButton.clicked.connect(self.validate_and_save)
        self.save_dlg.ui.revertPushButton.clicked.connect(self.cancel_modifications)
        self.save_dlg.ui.cancelPushButton.clicked.connect(lambda: self.save_dlg.close())

        # Connect desc lineedit text changed event
        self.street_browser.ui.descriptionTextEdit.textChanged.connect(self.desc_text_changed)

        self.modify = SwitchStreetBrowserMode(self.street_browser)

        self.desc_original = ""
        self.insert_pre_update = ""

        self.cur_model = None
        self.edit_esu = None
        self.coords = None

        # SQL insert statement to copy a record
        self.record_copy_sql = ""

    def desc_text_changed(self):
        """
        Change the desc field label colour if validation passes/fails
        """
        desc_textedit = self.street_browser.ui.descriptionTextEdit
        desc_len = len(desc_textedit.toPlainText())
        if desc_len > 0:
            self.street_browser.ui.descriptionLabel.setStyleSheet("color : black")
        else:
            self.street_browser.ui.descriptionLabel.setStyleSheet("color : red")

    def modify_record(self):
        """
        Setup or complete a modification to a record. The button text determines action.
        """
        modify_text = str(self.street_browser.ui.modifyPushButton.text())
        if modify_text.lower() == "modify":
            if config.DEBUG_MODE:
                print('DEBUG MODE: Modify pressed')
            # Begin edit + connect esu button
            self.street_browser.ui.editEsuPushButton.clicked.connect(self.edit_esu_link)
            self.street_browser.ui.editCoordsPushButton.clicked.connect(self.edit_start_end_coords)
            self.street_browser_modify()
            if not self.esu_layer:
                # Set the ESU layer to read only during modification of the record
                self.esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
            if config.DEBUG_MODE:
                print("DEBUG_MODE: Setting ESU layer to read only for modify.")
            self.esu_layer.setReadOnly(True)
        else:
            if config.DEBUG_MODE:
                print('DEBUG_MODE: Complete pressed')
            self.save_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            if config.DEBUG_MODE:
                print("DEBUG_MODE: Setting ESU layer to writable after modify.")
            self.esu_layer.setReadOnly(False)
            self.save_dlg.exec_()

    def street_browser_modify(self):
        """
        Makes the street browser form editable
        """
        map_lookup = MapLookupValues(self.model)
        # Save snapshot of model to detect edits later on
        self.cur_model = map_lookup.all_mapped_fields(self.mapper.currentIndex(), 2, 1)
        # Make a copy of the record to be inserted if changes are made
        self.generate_sql_for_record_copy()
        # make the sb gui editable
        self.street_browser.ui.modifyPushButton.setText("Complete")
        self.modify.edit()
        # Save text for a revert
        self.desc_original = str(self.street_browser.ui.descriptionTextEdit.toPlainText())
        # Set index of combobox
        self.set_combo_index()
        self.set_dateedit_value()
        self.set_by_to_username()
        # Zoom to record
        self.canvas_functs.zoom_to_record(close=False, zoom_to=True, select=True)

    def street_browser_read_only(self):
        """
        Switch the sb gui to read only mode.
        """
        self.street_browser.ui.modifyPushButton.setText("Modify")
        self.modify.read_only()

    def is_coords_dirty(self, cur_model, updated_model):
        """
         Check which edit closure behaviour should be used depending on which fields have been modified
        :rtype : bool bool
        :param cur_model: Model before editing
        :param updated_model: Model after editing
        :return: dirty_coords=updated coordinates, dirty_other=Other mods to from
        """
        coords_idx = [11, 12, 13, 14]
        # Version and updatedate to be ignored as they are always auto updated
        dirty_coords = False
        dirty_other = False
        # Compare org model against current
        for field in cur_model:
            cur_index = field.index
            for field_n in updated_model:
                if cur_index == field_n.index:
                    if str(field.display_data) != str(field_n.display_data) or field.lookup_data != field_n.lookup_data:
                        if cur_index in coords_idx:
                            dirty_coords = True
                        else:
                            dirty_other = True
        # Check for new esu links
        if self.edit_esu:
            esu_lst = self.edit_esu.get_final_selection()
            org, final = esu_lst[0], esu_lst[1]
            if set(org) != set(final):
                dirty_other = True
        return dirty_coords, dirty_other

    def generate_sql_for_record_copy(self):
        """
        Generate sql to copy of the record from before it was modified (changing currency_flag to 1)
        """
        usrn = self.street_browser.ui.usrnLineEdit.text()
        self.record_copy_sql = """INSERT INTO tblSTREET (usrn, version_no, currency_flag, street_ref_type, description, entry_date,
        update_date, start_date, authority, closure_date, start_xref, start_yref, end_xref, end_yref, tolerance,
        street_sub_type, street_state, state_date, street_class, loc_ref, county_ref, town_ref, updated_by, closed_by,
        min_x, min_y, max_x, max_y, description_alt) SELECT usrn, version_no, 1, street_ref_type, description,
        entry_date, update_date, start_date, authority, closure_date, start_xref, start_yref, end_xref, end_yref,
        tolerance, street_sub_type, street_state, state_date, street_class, loc_ref, county_ref, town_ref, updated_by,
        closed_by, min_x, min_y, max_x, max_y, description_alt FROM tblSTREET  WHERE usrn = %s and
        currency_flag = 0;""" % usrn

    def set_combo_index(self):
        """
        Set the combo index to match the current value.
        """
        for idx, qitem in self.update_dict.iteritems():
            try:
                combo = qitem[0]
                line_edit = qitem[1]
                current_txt = line_edit.text()
                idx = combo.findText(current_txt)
                combo.setCurrentIndex(idx)
            except AttributeError:
                # skip dateedits, etc
                pass

    def set_dateedit_value(self):
        """
        Set the dateedit value from the lineedit date.
        """
        date_text = self.street_browser.ui.startDateLineEdit.text()
        date = datetime.datetime.strptime(date_text, "%d/%m/%Y")
        date_obj = QDate(date.year, date.month, date.day)
        self.street_browser.ui.startDateDateEdit.setDate(date_obj)

    def set_by_to_username(self):
        """
        Replace edited 'by' value with current username.
        :returns void:
        """
        username = self.params['UserName']
        self.street_browser.ui.byLineEdit.setText(username)

    def cancel_modifications(self):
        """
        Revert changes made + close.
        """
        self.disconnect_esu_and_coords()
        self.street_browser_read_only()
        self.model.revertAll()
        self.mapper.revert()
        usrn = str(self.street_browser.ui.usrnLineEdit.text())
        self.edit_signals.currentIndexSet.emit(usrn)
        self.edit_esu = None
        self.save_dlg.close()

    def validate_and_save(self):
        usrn = self.street_browser.ui.usrnLineEdit.text()
        mandatory = self.modify.mandatory_field_check()
        unique_desc = ValidateDescription(self.street_browser, self.db).validate(usrn=usrn)
        distinct_sel = list()
        if self.edit_esu:
            final_sel = self.edit_esu.get_final_selection()[0]
            # Create a list of all esu's without duplicates for symbology updating
            original_sel = self.edit_esu.get_final_selection()[1]
            distinct_sel = final_sel + list(set(original_sel) - set(final_sel))
            esu_valid = ValidateStreetType(self.street_browser, self.db).validate(usrn, final_sel)
        else:
            esu_valid = ValidateStreetType(self.street_browser, self.db).validate(usrn)
        if mandatory and unique_desc and esu_valid:
            self.save_modifications()
            current_index = self.mapper.currentIndex()
            self.mapper.setCurrentIndex(current_index)
            current_usrn = self.mapper.mappedWidgetAt(1).text()
            self.edit_signals.currentIndexSet.emit(current_usrn)
            # Update Esu Graphic symbology attribute for all linked Esu's
            if distinct_sel:
                # Pass the removed and added esu id's for symbology updating
                UpdateEsuSymbology(self.db, self.esu_layer).update(usrn, esu_list=distinct_sel)
            else:
                UpdateEsuSymbology(self.db, self.esu_layer).update(usrn)
        else:
            # close save dlg and give warning
            self.save_dlg.close()
            self.failed_validation_msg(mandatory, unique_desc, esu_valid)

    def save_modifications(self):
        """
        Insert unmodified copy of the record, then save changes and deal with currency flag.
        """
        unmod_query = QSqlQuery(self.db)
        unmod_query.exec_(self.record_copy_sql)
        # Save changes from dropdowns by directly editing model
        current = self.mapper.currentIndex()
        for idx, qitem in self.update_dict.iteritems():
            combo = qitem[0]
            try:
                data = combo.itemData(combo.currentIndex())
            except AttributeError:
                if idx == 5:
                    # Desc text
                    data = qitem[1].toPlainText()
                elif idx == 2:
                    # Version num
                    data = qitem[1].text()
                else:
                    # Otherwise its a date
                    data_raw = combo.text()
                    date_obj = datetime.datetime.strptime(data_raw, "%d/%m/%Y")
                    data = str(date_obj.strftime("%Y%m%d"))
            # Add modified data to the model
            if not self.model.setData(self.model.createIndex(current, idx), data):
                msg = "Error updating database model\n"
                msg += "Row: {}, Column: {}, Data: {}\n".format(current, idx, data)
                msg += self.model.lastError().text()
                raise BaseException(msg)
        # Compare model row before and after edit session
        map_lookup = MapLookupValues(self.model)
        updated_model = map_lookup.all_mapped_fields(current, 2, 1)
        dirty = self.is_coords_dirty(self.cur_model, updated_model)
        self.cur_model = None
        coord_dirt = dirty[0]
        other_dirt = dirty[1]
        if not coord_dirt and not other_dirt:
            # No edits so revert
            self.cancel_modifications()
        elif coord_dirt and not other_dirt:
            # Only coords edited, so no need to to duplicate record, ver no, etc
            self.model.submitAll()
            self.cancel_modifications()
        # Some data in the model has changed so submit and increment version number + updatedate
        else:
            # Auto set current date (update date)
            data = str(datetime.datetime.now().strftime("%Y%m%d"))
            self.model.setData(self.model.createIndex(current, 7), data)
            # Change updated by
            self.model.setData(self.model.createIndex(current, 23), self.params['UserName'])
            # Increment version number
            cur_ver = int(self.street_browser.ui.versionLineEdit.text())
            ver_plus_one = cur_ver + 1
            self.model.setData(self.model.createIndex(current, 2), str(ver_plus_one))
            # Save esu links
            self.update_esu_link(cur_ver, ver_plus_one)
            # Commit to db
            self.model.submitAll()
        # Select all rows in the model again (else filtering fails)
        self.post_model_submit(current)

    def failed_validation_msg(self, mandatory, desc, esu_valid):
        # TODO: Attach esu's to error message (see bad_esu = [] in validate_mandatory)
        """
        Display appropriate error message for failed validation
        :param mandatory: All mand fields complete (bool)
        :param desc: Unique desc (bool)
        :param esu_valid: esu links valid (bool)
        """
        err = "Unable to save record:"
        errors = []
        if not mandatory:
            errors.append("All mandatory fields must be complete")
        if not desc:
            errors.append("Description already exists within this town/locality")
        if not esu_valid:
            errors.append("Invalid ESU links")
        for error in errors:
            err = err + "\n" + str(error)
        edit_fail_msg_box = QMessageBox(QMessageBox.Warning, " ", err, QMessageBox.Ok, None)
        edit_fail_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        edit_fail_msg_box.exec_()

    def post_model_submit(self, cur_idx):
        """
        Various actions after a model submit
        :param cur_idx: Mapper index
        """
        while self.model.canFetchMore():
            self.model.fetchMore()
        # Refresh mapper
        self.mapper.setCurrentIndex(cur_idx)
        self.edit_esu = None
        # Revert to read only
        self.street_browser_read_only()
        self.save_dlg.close()
        self.disconnect_esu_and_coords()

    def disconnect_esu_and_coords(self):
        """
        Disconnect esu pushbutton and coords push button, re-connected with diff params for add record.
        """
        try:
            self.street_browser.ui.editEsuPushButton.clicked.disconnect()
            self.street_browser.ui.editCoordsPushButton.clicked.disconnect()
        except TypeError:
            pass

    def edit_esu_link(self):
        """
        Add and/or remove esu links for a street
        """
        layer = 'ESU Graphic'
        display_attr = 'esu_id'
        usrn = str(self.street_browser.ui.usrnLineEdit.text())
        button = self.street_browser.ui.editEsuPushButton
        if self.edit_esu:
            previous_unsaved = self.edit_esu.get_final_selection()[0]
            self.edit_esu = EditEsuLink(self.iface, button, self.db, street_browser=self.street_browser, usrn=usrn,
                                        unsaved=previous_unsaved, layer_name=layer, dis_attr=display_attr)
        else:
            self.edit_esu = EditEsuLink(self.iface, button, self.db, street_browser=self.street_browser, usrn=usrn,
                                        layer_name=layer, dis_attr=display_attr)
        self.edit_esu.show()

    def edit_start_end_coords(self):
        """
        Instance of coord edit class
        """
        coord_le = {"start_xref": self.street_browser.ui.startXLineEdit,
                    "start_yref": self.street_browser.ui.startYLineEdit,
                    "end_xref": self.street_browser.ui.endXLineEdit,
                    "end_yref": self.street_browser.ui.endYLineEdit}
        button = self.street_browser.ui.editCoordsPushButton
        usrn = self.street_browser.ui.usrnLineEdit.text()
        self.coords = EditStartEndCoords(self.iface, coord_le, self.model, self.mapper, button, usrn=usrn)
        self.coords.show()

    def update_esu_link(self, old_usrn_ver, new_usrn_ver):
        """
        Updates existing esu links on edit and deal with adding/remove links via editing
        :param old_usrn_ver: Old usrn version no
        :param new_usrn_ver: New usrn version no
        """
        usrn = str(self.street_browser.ui.usrnLineEdit.text())
        if self.edit_esu:
            # get new set of esu links
            esus = self.edit_esu.get_final_selection()
            final = esus[0]
        else:
            # No esu edits made so query for existing esu links
            final = self.canvas_functs.query_esu(usrn)
        date = str(datetime.datetime.now().strftime("%Y%m%d"))
        try:
            for esu in final:
                query_str = "SELECT version_no FROM tblESU WHERE esu_id = %s AND currency_flag = 0;" % esu
                query = QSqlQuery(query_str, self.db)
                seek = query.seek(0)
                if seek:
                    esu_ver = query.value(0)
                else:
                    esu_ver = str(1)
                # Create new links
                insert_sql = "INSERT INTO lnkESU_STREET (esu_id, usrn, esu_version_no, usrn_version_no, currency_flag," \
                             " entry_date, update_date) VALUES (%s, %s, %s, %s, 0, %s, %s)" \
                             % (esu, usrn, esu_ver, new_usrn_ver, date, date)
                insert = QSqlQuery(insert_sql, self.db)
            # Close existing links
            update_sql = "UPDATE lnkESU_STREET SET currency_flag=1, closure_date=%s WHERE usrn = %s " \
                         "AND usrn_version_no = %s" % (date, usrn, old_usrn_ver)
            update = QSqlQuery(update_sql, self.db)
        except TypeError:
            # No esu's attached to record
            pass

    def populate_combos(self):
        """
        Populate all comboboxes from db lookup tables. Combos sorted alphabetically with a 0 (default None) value at
        the top.
        """
        for query_str, combo in self.query_lst.iteritems():
            query = QSqlQuery(query_str)
            all_items = {}
            while query.next():
                text = str(query.value(0))
                value = str(query.value(1))
                all_items[text] = value
            if '0' in all_items.values():
                sorted_items = sorted(all_items.iteritems(), key=operator.itemgetter(0), reverse=True)
            else:
                # The only lookup without a 0 as 'None' item is the street ref type, also this is sorted on the type
                sorted_items = sorted(all_items.iteritems(), key=operator.itemgetter(1), reverse=True)
            default_none = None

            for item in sorted_items:
                text = item[0]
                data = item[1]
                if int(data) != 0:
                    combo.insertItem(0, text, userData=data)
                else:
                    default_none = item
            if default_none:
                combo.insertItem(0, default_none[0], userData=default_none[1])
            combo.setCurrentIndex(0)


class EditSignals(QObject):
    """class holding signals for the edit class"""
    currentIndexSet = pyqtSignal(str)


class EditStartEndCoords(object):
    """Class for editing start/end coordinates"""

    class ButtonEnum:

        start, end = range(2)

    def __init__(self, iface, coord_le, model, mapper, button, usrn=None, edit=True):

        self.iface = iface
        self.st_x_le = coord_le["start_xref"]
        self.st_y_le = coord_le["start_yref"]
        self.end_x_le = coord_le["end_xref"]
        self.end_y_le = coord_le["end_yref"]
        # self.street_browser = street_browser
        self.model = model
        self.mapper = mapper
        # Determines if coords are being edited or added
        self.edit = edit
        self.usrn = usrn
        # Button to be disabled/enabled
        self.button = button
        # Create dialog
        self.coords_dlg = EditCoordsDlg()
        # sets coords limits in all line edits for validation
        self.coords_line_edit_list = None
        self.set_coords_limits()
        self.coords_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        # Connect buttons
        self.connect_buttons()
        self.selected_button = None
        self.tool_clickPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.vm_start = None
        self.vm_end = None
        self.modified_coordinates = False
        # self.saved = False

    def connect_buttons(self):
        """
        Connect buttons.
        """
        self.coords_dlg.ui.cancelPushButton.clicked.connect(self.close_dlg)
        self.coords_dlg.ui.okPushButton.clicked.connect(self.close_save_dlg)
        self.coords_dlg.ui.startPushButton.pressed.connect(lambda: self.edit_coords(self.ButtonEnum.start))
        self.coords_dlg.ui.endPushButton.pressed.connect(lambda: self.edit_coords(self.ButtonEnum.end))

    def show(self):
        """
        Show the dialog, populate if there are existing values.
        """
        self.setup_vm()
        x_start = self.st_x_le.text()
        y_start = self.st_y_le.text()
        # Test for existing coords (none if add)
        if len(str(x_start)) > 0 and len(str(y_start)) > 0:
            self.populate_from_sb()
        # Update label
        if self.usrn:
            self.coords_dlg.ui.usrnLabel.setText("USRN: " + str(self.usrn))
        else:
            self.coords_dlg.ui.usrnLabel.setVisible(False)
        self.button.setEnabled(False)
        self.coords_dlg.exec_()

    def close_dlg(self):
        """
        Cancel/cleanup
        """
        self.coords_dlg.close()
        self.button.setEnabled(True)
        self.remove_markers()
        self.iface.actionSelect().trigger()

    def close_save_dlg(self):
        """
        Set sb cooord line edits, remove markers + close dlg
        """
        # first checks if coordinates are valid
        if self.validate_coords():
            if self.edit:
                # Editing existing record so update model directly
                self.model.setData(self.model.createIndex(self.mapper.currentIndex(), 11),
                                   self.coords_dlg.ui.startXLineEdit.text())
                self.model.setData(self.model.createIndex(self.mapper.currentIndex(), 12),
                                   self.coords_dlg.ui.startYLineEdit.text())
                self.model.setData(self.model.createIndex(self.mapper.currentIndex(), 13),
                                   self.coords_dlg.ui.endXLineEdit.text())
                self.model.setData(self.model.createIndex(self.mapper.currentIndex(), 14),
                                   self.coords_dlg.ui.endYLineEdit.text())
            else:
                # New record so just update the lineedits on the street browser
                self.st_x_le.setText(self.coords_dlg.ui.startXLineEdit.text())
                self.st_y_le.setText(self.coords_dlg.ui.startYLineEdit.text())
                self.end_x_le.setText(self.coords_dlg.ui.endXLineEdit.text())
                self.end_y_le.setText(self.coords_dlg.ui.endYLineEdit.text())
            self.button.setEnabled(True)
            self.remove_markers()
            self.coords_dlg.close()
            self.iface.actionSelect().trigger()
        else:
            return

    def edit_coords(self, button):
        """
        Start/stop editing point.
        :param button: button enum
        """
        self.disconnect_click_point()
        start_button = self.coords_dlg.ui.startPushButton
        end_button = self.coords_dlg.ui.endPushButton
        if button == self.ButtonEnum.start:
            if not start_button.isChecked():
                self.capture_point(button)
            end_button.setChecked(False)
        if button == self.ButtonEnum.end:
            if not end_button.isChecked():
                self.capture_point(button)
            start_button.setChecked(False)

    def capture_point(self, button):
        """
        connect canvasClicked event
        :param button: Button enum
        """
        self.selected_button = button
        self.tool_clickPoint.canvasClicked.connect(self.canvas_clicked)
        self.iface.mapCanvas().setMapTool(self.tool_clickPoint)

    def disconnect_click_point(self):
        """
        Disconnect canvasClicked signal.
        """
        try:
            self.tool_clickPoint.canvasClicked.disconnect()
        except TypeError:
            pass

    def canvas_clicked(self, point=None, button=None):
        """
        Set lineedit to clicked coords + vertex marker
        :param point: x, y
        :param button: Button enum
        """
        x, y = point[0], point[1]
        self.modified_coordinates = True
        if self.selected_button == self.ButtonEnum.start:
            self.coords_dlg.ui.startXLineEdit.setText(str(round(x, 2)))
            self.coords_dlg.ui.startYLineEdit.setText(str(round(y, 2)))
            self.place_marker(self.vm_start, point)
        if self.selected_button == self.ButtonEnum.end:
            self.coords_dlg.ui.endXLineEdit.setText(str(round(x, 2)))
            self.coords_dlg.ui.endYLineEdit.setText(str(round(y, 2)))
            self.place_marker(self.vm_end, point)

    def place_marker(self, marker, point):
        """
        Place a vertex marker on the canvas at a given x/y
        :param marker: Vertex marker
        :param point: x, y
        """
        x, y = point[0], point[1]
        try:
            marker.setCenter(QgsPoint(float(x), float(y)))
            self.iface.mapCanvas().refresh()
        except ValueError:
            pass

    def remove_markers(self):
        """
        Remove marker from canvas.
        """
        self.iface.mapCanvas().scene().removeItem(self.vm_start)
        self.iface.mapCanvas().scene().removeItem(self.vm_end)

    def populate_from_sb(self):
        """
        Populate initial cooords to editor.
        """
        start_x = self.st_x_le.text()
        start_y = self.st_y_le.text()
        end_x = self.end_x_le.text()
        end_y = self.end_y_le.text()
        self.coords_dlg.ui.startXLineEdit.setText(start_x)
        self.coords_dlg.ui.startYLineEdit.setText(start_y)
        self.coords_dlg.ui.endXLineEdit.setText(end_x)
        self.coords_dlg.ui.endYLineEdit.setText(end_y)
        self.place_marker(self.vm_start, (start_x, start_y))
        self.place_marker(self.vm_end, (end_x, end_y))

    def setup_vm(self):
        """
        Setup/style the vertex marker.
        """
        self.vm_start = QgsVertexMarker(self.iface.mapCanvas())
        self.vm_start.setColor(QColor('blue'))
        self.vm_start.setIconSize(16)
        self.vm_start.setPenWidth(4)
        self.vm_end = QgsVertexMarker(self.iface.mapCanvas())
        self.vm_end.setColor(QColor('red'))
        self.vm_end.setIconSize(16)
        self.vm_end.setPenWidth(4)

    def set_coords_limits(self):
        """
        sets min and max X and Y coords for user input validation
        :return: void
        """
        self.coords_line_edit_list = self.coords_dlg.findChildren(QLineEdit)
        x_coords_validator = QDoubleValidator(-100000.00, 600000.00, 2, None)
        y_coords_validator = QDoubleValidator(100000.00, 1300000.00, 2, None)
        for coords_line_edit in self.coords_line_edit_list:
            if "X" in coords_line_edit.objectName():
                coords_line_edit.setValidator(x_coords_validator)
            else:
                coords_line_edit.setValidator(y_coords_validator)

    def validate_coords(self):
        """
        function that validates the coordinates into the ESU coords text boxes
        :return: [bool] True if all coords are valid, False if at least one coord is invalid
        """
        coords_line_edit_names = {
            'startXLineEdit': 'Start X',
            'startYLineEdit': 'Start Y',
            'endXLineEdit': 'End X',
            'endYLineEdit': 'End Y'
            }
        for coords_line_edit in self.coords_line_edit_list:
            state = coords_line_edit.validator().validate(coords_line_edit.text(), 0)
            if int(state[0]) is not 2:
                coords_invalid_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                                     "{} is out of range for this coordinate system".
                                                     format(coords_line_edit_names[coords_line_edit.objectName()]),
                                                     QMessageBox.Ok, None)
                coords_invalid_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                coords_invalid_msg_box.exec_()
                return False
        return True


class EditEsuLink(object):
    """
    Class for editing of Esu/Street links
    """

    def __init__(self, iface, button, db, **kwargs):

        self.iface = iface
        self.db = db
        self.button = button
        # No street browser instance then it must be SRWR polygon link
        self.street_browser = None
        # No usrn param provided = not a modification of an existing record
        self.usrn = None
        self.unsaved = None
        self.layer_name = None
        self.dis_attr = None

        self.sort_kwargs(kwargs)

        # Create esu dialog
        self.esu_dlg = EditEsuLinkDlg()
        self.esu_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        # Create instance of generic zoom/select functs
        self.gn_fnc = ZoomSelectCanvas(self.iface, self.street_browser, self.db)
        self.connect_buttons()
        self.layer = QgsMapLayerRegistry.instance().mapLayersByName(self.layer_name)[0]
        set_layer = self.iface.setActiveLayer(self.layer)
        # List widget
        self.list_widget = self.esu_dlg.ui.esuLinkListWidget
        self.list_widget.clear()
        self.selected_dict = {}
        self.final_selection = []
        self.original_selection = []

    def sort_kwargs(self, kwargs):
        """
        Set class variables to kwarg params
        :param kwargs: key word arguments
        """
        if "street_browser" in kwargs:
            self.street_browser = kwargs["street_browser"]
        if "usrn" in kwargs:
            self.usrn = kwargs["usrn"]
        if "unsaved" in kwargs:
            self.unsaved = kwargs["unsaved"]
        if "layer_name":
            self.layer_name = kwargs["layer_name"]
        if "dis_attr" in kwargs:
            self.dis_attr = kwargs["dis_attr"]

    def show(self):
        """
        Populate + show
        """
        self.populate_listwidget()
        self.button.setEnabled(False)
        self.esu_dlg.exec_()

    def connect_selection_change(self):
        """
        Connect selection update
        """
        self.layer.selectionChanged.connect(self.esu_selection_changed)

    def connect_buttons(self):
        """
        Connect buttons
        """
        self.esu_dlg.ui.okPushButton.clicked.connect(self.close_save_dlg)
        self.esu_dlg.ui.cancelPushButton.clicked.connect(self.close_dlg)

    def close_save_dlg(self):
        """
        Disconnect, save + close if valid
        """
        try:
            self.layer.selectionChanged.disconnect(self.esu_selection_changed)
        except TypeError:
            pass
        for esu in self.selected_dict:
            self.final_selection.append(esu)
        self.button.setEnabled(True)
        self.esu_dlg.close()

    def close_dlg(self):
        """
        disconnect + close
        """
        try:
            self.layer.selectionChanged.disconnect(self.esu_selection_changed)
        except TypeError:
            pass
        # Set the final selection to the same as the original for a cancel operation
        self.final_selection = self.original_selection
        self.button.setEnabled(True)
        self.esu_dlg.close()

    def esu_selection_changed(self, selected, deselected, clear_and_sel):
        """
        Slot for selection changed event to add/remove esu's
        :param selected: selected items fids
        :param deselected: Items just deselected fids
        """
        prov = self.layer.dataProvider()
        for fid in selected:
            esu_id = None
            feat = self.layer.getFeatures(
                QgsFeatureRequest().setFilterFid(fid)).next()
            esu_id = int(feat.attribute(self.dis_attr))

            if esu_id not in self.selected_dict:
                self.selected_dict[esu_id] = QListWidgetItem(str(esu_id),
                                                             self.list_widget)

        for fid in deselected:
            esu_id = None
            feat = self.layer.getFeatures(
                QgsFeatureRequest().setFilterFid(fid)).next()
            esu_id = int(feat.attribute(self.dis_attr))

            try:
                item = self.selected_dict[esu_id]
                idx = self.list_widget.indexFromItem(item)
                self.list_widget.takeItem(idx.row())
                self.selected_dict.pop(esu_id)
            except KeyError:
                # add record has nothing previously selected
                pass

    def populate_listwidget(self):
        """
        Deals with initial population and slot connection. Re-populate list with previously selected but unsaved esu's.
        i.e. with same modification
        """
        if self.unsaved:
            for esu in self.unsaved:
                self.selected_dict[int(esu)] = QListWidgetItem(str(esu), self.list_widget)
            self.original_selection = self.unsaved
        elif self.usrn:
            self.gn_fnc.zoom_to_record(usrn=self.usrn, select=True)
            esu_list = self.gn_fnc.query_esu(self.usrn)
            try:
                for esu in esu_list:
                    self.selected_dict[int(esu)] = QListWidgetItem(str(esu), self.list_widget)
                # Create list of original esu's (edit testing comparison)
                self.original_selection = esu_list
            except TypeError:
                # no esu links
                pass
        else:
            # Connect selection changed signal
            self.connect_selection_change()
            return
        # Connect selection changed signal
        self.connect_selection_change()
        # Zoom canvas to esu's
        self.zoom_to_esus()

    def zoom_to_esus(self):
        """
        Zoom the map canvas to the original selection of ESU's
        :return:
        """
        field = 'esu_id'
        layer_name = 'ESU Graphic'
        feats = self.gn_fnc.get_features_from_field_value(self.original_selection, field, layer_name)
        self.gn_fnc.select_features(feats, self.layer_name)

    def get_final_selection(self):
        """
        return final and original feature selection
        :rtype: list list
        :return: Final ESU selection and the original selection (for comparison purposes)
        """
        return self.final_selection, self.original_selection


class UpdateEsuSymbology(object):
    def __init__(self, db, esu_layer):
        self.db = db
        self.esu_layer = esu_layer

    def update(self, usrn, esu_list=None):
        """
        Main method to update symbology.
        :param usrn: usrn of current street being modified
        """
        if esu_list:
            # Its a delete/close update
            esu_ids = esu_list
        else:
            esu_ids = self.get_esu_selection(usrn)
        for esu in esu_ids:
            all_link_types = self.street_ref_types(esu)
            symbol_value = self.calculate_symbol_no(all_link_types)
            self.update_attributes(esu, symbol_value)
        self.esu_layer.removeSelection()

    def street_ref_types(self, esu_id):
        """
        Get the street type from the db
        :param esu_id: esu ID
        :return: List of all types associated with esu
        """
        sql = """
              SELECT tblSTREET.street_ref_type
                  FROM lnkESU_STREET INNER JOIN tblSTREET
                      ON lnkESU_STREET.usrn_version_no = tblSTREET.version_no
                         AND lnkESU_STREET.usrn = tblSTREET.usrn
              WHERE lnkESU_STREET.esu_id = {esu_id}
                  AND lnkESU_STREET.currency_flag = 0
                  AND tblSTREET.currency_flag = 0
              ;""".format(esu_id=esu_id)
        query = QSqlQuery(sql, self.db)
        all_type_links = []
        while query.next():
            type_ = int(query.value(0))
            all_type_links.append(type_)
        return all_type_links

    @staticmethod
    def calculate_symbol_no(types):
        """
        Symbology value is calculated by the sum of all the different type values.
        :param types: List of all street types esu is linked too
        :return: symbol int value
        """
        # Default 0 for unassigned
        symbol = 0
        if len(types) == 0:
            return symbol

        # Type greater than 4 is invalid
        max_type = sorted(types)[-1]
        if max_type > 4:
            symbol = 1
            return symbol

        # Multiple type 1, 2 or 3 records is invalid
        for type_number in [1, 2, 3]:
            if types.count(type_number) > 1:
                symbol = 1
                return symbol

        # Type 1 and 2 together is invalid
        if (1 in types) and (2 in types):
            symbol = 1
            return symbol

        # Type 3 or 4 without a type 1 or 2 is invalid
        has_1_or_2 = (1 in types) or (2 in types)
        has_3_or_4 = (3 in types) or (4 in types)
        if has_3_or_4 and not has_1_or_2:
            symbol = 1
            return symbol

        # Calculate symbol from remaining types
        if 1 in types:
            symbol += 10
        if 2 in types:
            symbol += 11
        if 3 in types:
            symbol += 2
        if 4 in types:
            symbol += 4

        return symbol

    def update_attributes(self, esu_id, symbol):
        """
        Update feature attributes
        :param esu_id: esu ID
        :param symbol: symbology number
        """
        sql = """UPDATE esu
                 SET symbol={symbol}
                 WHERE esu_id IS {esu_id}
                 ;""".format(symbol=symbol, esu_id=esu_id)
        if config.DEBUG_MODE:
            print("DEBUG_MODE: Updating ESU symbology for esu_id={}".format(esu_id))
        query = QSqlQuery(sql, self.db)

    def get_esu_selection(self, usrn):
        """
        Get the Esu selection from db
        :param usrn: modified record usrn
        :return: List of linked esu's
        """
        esu_selection = []
        sql = "select esu_id from lnkESU_STREET where usrn = %s and currency_flag = 0" % usrn
        query = QSqlQuery(sql, self.db)
        while query.next():
            esu_selection.append(query.value(0))
        return esu_selection
