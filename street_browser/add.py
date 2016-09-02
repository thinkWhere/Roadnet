# -*- coding: utf-8 -*-
import datetime

from PyQt4.QtSql import QSqlQuery, QSqlQueryModel
from PyQt4.QtGui import QMessageBox, QLineEdit, QComboBox
from PyQt4.QtCore import Qt, QDate

from qgis.core import QgsMapLayerRegistry

from ..generic_functions import SwitchStreetBrowserMode, ZoomSelectCanvas, ipdb_breakpoint
from ..roadnet_dialog import SaveRecordDlg
from edit import EditEsuLink, EditStartEndCoords, UpdateEsuSymbology
from mod_validation import ValidateDescription, ValidateStreetType

__author__ = 'matthew.walsh'


class AddRecord:
    """
    Add a new street record to the model
    """
    def __init__(self, iface, street_browser, model, mapper, db, params):
        self.street_browser = street_browser
        self.iface = iface
        self.model = model
        self.mapper = mapper
        self.db = db
        self.username = params['UserName']
        self.modify = SwitchStreetBrowserMode(self.street_browser)
        self.save_dlg = SaveRecordDlg()
        self.save_dlg.ui.savePushButton.clicked.connect(self.save_new_record)
        self.save_dlg.ui.revertPushButton.clicked.connect(self.cancel_new_record)
        self.save_dlg.ui.cancelPushButton.clicked.connect(lambda: self.save_dlg.close())
        self.esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]

        self.lineedits = {1: self.street_browser.ui.usrnLineEdit,
                          8: self.street_browser.ui.startDateDateEdit,
                          7: self.street_browser.ui.updateDateLineEdit,
                          2: self.street_browser.ui.versionLineEdit,
                          6: self.street_browser.ui.entryDateLineEdit,
                          18: self.street_browser.ui.stateDateLineEdit,
                          11: self.street_browser.ui.startXLineEdit,
                          12: self.street_browser.ui.startYLineEdit,
                          13: self.street_browser.ui.endXLineEdit,
                          14: self.street_browser.ui.endYLineEdit,
                          15: self.street_browser.ui.tolLineEdit}

        self.combos = {4: self.street_browser.ui.recordTypeComboBox,
                       20: self.street_browser.ui.localityComboBox,
                       22: self.street_browser.ui.townComboBox,
                       21: self.street_browser.ui.countyComboBox,
                       9: self.street_browser.ui.authorityComboBox,
                       17: self.street_browser.ui.stateComboBox,
                       19: self.street_browser.ui.classComboBox}

        self.start_idx = None
        self.start_desc = None
        self.start_tol = None

        self.edit_esu = None
        self.new_usrn_no = None
        self.esu_version = ZoomSelectCanvas(self.iface, self.street_browser, self.db)

    def add(self):
        """
        Main method to decide whether to setup for adding or complete/commit record
        """
        add_text = str(self.street_browser.ui.addPushButton.text())
        # Setup blank form
        if add_text.lower() == "add":
            self.street_browser.ui.editEsuPushButton.clicked.connect(self.create_esu_link)
            self.street_browser.ui.editCoordsPushButton.clicked.connect(self.create_start_end_coords)
            self.setup_sb_add()
        # Completion event
        else:
            self.save_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            self.save_dlg.exec_()

    def current_desc_tol_idx(self):
        """
        Grab the current record index and desc
        """
        self.start_idx = self.mapper.currentIndex()
        self.start_desc = self.street_browser.ui.descriptionTextEdit.toPlainText()
        self.start_tol = self.street_browser.ui.tolLineEdit.text()

    def setup_sb_add(self):
        """
        Setup the street browser for adding a new record
        """
        # Grab current idx's desc, tol
        self.current_desc_tol_idx()
        n_usrn = self.new_usrn()
        self.street_browser.ui.addPushButton.setText("Complete")
        self.street_browser.ui.descriptionLabel.setStyleSheet("color : red")
        self.modify.edit()
        # Clear lineedits
        all_lineedits = self.street_browser.findChildren(QLineEdit)
        for lineedit in all_lineedits:
            lineedit.setText("")
        self.clear_xref_and_esu_tables()
        self.set_combo_index()
        self.set_current_dates()
        self.street_browser.ui.tolLineEdit.setStyleSheet("background-color: white")
        self.street_browser.ui.tolLineEdit.setReadOnly(False)
        self.street_browser.ui.tolLineEdit.setText("10")
        self.street_browser.ui.descriptionTextEdit.setText("")
        # Set new usrn + version 1
        self.street_browser.ui.byLineEdit.setText(self.username)
        self.street_browser.ui.usrnLineEdit.setText(str(n_usrn))
        self.street_browser.ui.versionLineEdit.setText("1")
        # Set the ESU layer to read only
        self.esu_layer.setReadOnly(True)

    def revert_sb_add(self):
        """
        Revert street browser back to read-only mode
        """
        self.edit_esu = None
        self.modify.read_only()
        self.street_browser.ui.tolLineEdit.setReadOnly(True)
        self.street_browser.ui.tolLineEdit.setStyleSheet("background-color: rgb(213,234,234)")
        self.street_browser.ui.addPushButton.setText("Add")
        self.esu_layer.setReadOnly(False)

    def clear_xref_and_esu_tables(self):
        """
        Blank model clears the xref table
        """
        # Set xref to empty model
        empty_model = QSqlQueryModel()
        self.street_browser.ui.crossReferenceTableView.setModel(empty_model)
        # Clear list widget
        self.street_browser.ui.linkEsuListWidget.clear()

    def set_combo_index(self):
        """
        Set the index of the comboboxes
        """
        all_combos = self.street_browser.findChildren(QComboBox)
        for combo in all_combos:
            combo.setCurrentIndex(0)

    def set_current_dates(self):
        """
        Set date lineedits/date picker to current date
        """
        now_date = datetime.datetime.now()
        now_formatted = now_date.strftime("%d/%m/%Y")
        self.street_browser.ui.updateDateLineEdit.setText(now_formatted)
        self.street_browser.ui.entryDateLineEdit.setText(now_formatted)
        self.street_browser.ui.stateDateLineEdit.setText(now_formatted)
        date_obj = QDate(now_date.year, now_date.month, now_date.day)
        self.street_browser.ui.startDateDateEdit.setDate(date_obj)

    def cancel_new_record(self):
        """
        Revert street browser to read only
        """
        self.revert_sb_add()
        self.mapper.setCurrentIndex(self.mapper.currentIndex())
        self.disconnect_esu_and_coords()
        self.save_dlg.close()

    def new_usrn(self):
        """
        Returns a new usrn (max usrn + 1)
        :rtype : int
        :return: USRN
        """
        query = QSqlQuery("SELECT MAX(usrn) from tblSTREET", self.db)
        query.seek(0)
        try:
            usrn = int(query.value(0)) + 1
        except TypeError:
            # Throws if there are no USRNs yet.  Example for demo db inserted here
            # This must be set manually for a new local authority
            usrn = 12700001
        self.new_usrn_no = usrn
        return usrn

    def failed_validation_msg(self, mandatory, desc, esu_valid):
        # TODO: Attach esu's to error message (see bad_esu = [] in validate_mandatory)
        """
        Display appropriate error message for failed validation
        :param mandatory: mand check bool
        :param desc: desc present bool
        :param esu_valid: valid esu links bool
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
        val_fail_msg_box = QMessageBox(QMessageBox.Warning, " ", err, QMessageBox.Ok, None)
        val_fail_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        val_fail_msg_box.exec_()

    def save_new_record(self):
        """
        Insert new record if all validation is passed
        """
        self._strip_whitespace_from_description()
        usrn = self.street_browser.ui.usrnLineEdit.text()
        mandatory = self.modify.mandatory_field_check()

        if self._record_is_type_3_or_4():
            unique_desc = True
        else:
            unique_desc = ValidateDescription(self.street_browser, self.db).validate()
        if self.edit_esu:
            final_sel = self.edit_esu.get_final_selection()[0]
            esu_valid = ValidateStreetType(self.street_browser, self.db).validate(usrn, final_sel)
        else:
            esu_valid = True

        if mandatory and unique_desc and esu_valid:
            self.insert_record()
            self.revert_sb_add()
            self.disconnect_esu_and_coords()
            # Update Esu Graphic symbology attribute for all linked Esu's
            self.esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
            UpdateEsuSymbology(self.db, self.esu_layer).update(usrn)
        else:
            self.failed_validation_msg(mandatory, unique_desc, esu_valid)

        self.save_dlg.close()

    def _strip_whitespace_from_description(self):
        """
        Strip whitespace from the text in the description field
        """
        description = str(self.street_browser.ui.descriptionTextEdit.toPlainText())
        description = description.strip()
        self.street_browser.ui.descriptionTextEdit.setPlainText(description)

    def _record_is_type_3_or_4(self):
        """
        Check the combo box to see if record is Type 3 or 3
        :return boolean:
        """
        record_type_combo = self.street_browser.ui.recordTypeComboBox
        record_type = int(record_type_combo.itemData(record_type_combo.currentIndex()))
        if record_type in (3, 4):
            return True
        else:
            return False

    def disconnect_esu_and_coords(self):
        try:
            self.street_browser.ui.editEsuPushButton.clicked.disconnect()
            self.street_browser.ui.editCoordsPushButton.clicked.disconnect()
        except TypeError:
            pass

    def insert_record(self):
        """
        Insert a record/row into the model + commit
        """
        record = self.model.record()
        record.setValue(1, str(self.street_browser.ui.usrnLineEdit.text()))  # usrn
        record.setValue(3, str(0))  # currency_flag 0
        record.setValue(5, str(self.street_browser.ui.descriptionTextEdit.toPlainText()))
        record.setValue(23, self.username)
        # Set values from lineedits
        date_cols = [6, 7, 8, 18]
        for idx, lineedit in self.lineedits.iteritems():
            txt = str(lineedit.text())
            if txt:
                # re-format dates for db
                if idx in date_cols:
                    txt = self.database_dates(txt)
                record.setValue(idx, txt)
        # Set values from comboboxes
        for idx, combo in self.combos.iteritems():
            combo_idx = combo.currentIndex()
            # if combo_idx != 0:
            record.setValue(idx, str(combo.itemData(combo_idx)))
        # Append record after last current record
        self.model.insertRecord(-1, record)
        # Commit to db + insert any esu links
        self.model.submitAll()
        self.commit_esu_link()
        self.repopulate_model()

    def repopulate_model(self):
        """
        Repopulate the model to show the new model
        """
        while self.model.canFetchMore():
            self.model.fetchMore()
        # jump to new record (appended to end)
        self.mapper.toLast()

    def database_dates(self, date):
        """
        Format dates from lineedits for database (yyyymmdd)
        :param date: Date string
        :return: formattted date string
        """
        date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
        db_date = str(date_obj.strftime("%Y%m%d"))
        return db_date

    def create_esu_link(self):
        """
        Add esu links to a street
        """
        button = self.street_browser.ui.editEsuPushButton
        layer = 'ESU Graphic'
        display_attr = 'esu_id'
        if self.edit_esu:
            previous_unsaved = self.edit_esu.get_final_selection()[0]

            self.edit_esu = EditEsuLink(self.iface, button, self.db, street_browser=self.street_browser,
                                        layer_name=layer, dis_attr=display_attr, unsaved=previous_unsaved)
        else:
            self.edit_esu = EditEsuLink(self.iface, button, self.db, street_browser=self.street_browser,
                                        layer_name=layer, dis_attr=display_attr)
        self.edit_esu.show()

    def commit_esu_link(self):
        """
        Updates existing esu links on edit and deal with adding/remove links via editing
        """
        usrn = str(self.new_usrn_no)
        if self.edit_esu:
            # get new set of esu links
            esus = self.edit_esu.get_final_selection()
            final = esus[0]
        else:
            # No esu edits made so query for existing esu links
            final = self.esu_version.query_esu(usrn)
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
                             " entry_date, update_date) VALUES (%s, %s, %s, 1, 0, %s, %s)" \
                             % (esu, usrn, esu_ver, date, date)
                new_lnk_query = QSqlQuery(insert_sql, self.db)
        except TypeError:
            # No esu's attached to record
            pass

    def create_start_end_coords(self):
        """
        Create instance of cooord edit class
        """
        coord_le = {"start_xref": self.street_browser.ui.startXLineEdit,
                    "start_yref": self.street_browser.ui.startYLineEdit,
                    "end_xref": self.street_browser.ui.endXLineEdit,
                    "end_yref": self.street_browser.ui.endYLineEdit}
        button = self.street_browser.ui.editCoordsPushButton
        usrn = self.street_browser.ui.usrnLineEdit.text()
        coords = EditStartEndCoords(self.iface, coord_le, self.model, self.mapper, button, usrn=usrn, edit=False)
        coords.show()
