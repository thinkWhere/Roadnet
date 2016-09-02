# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox
from PyQt4.QtSql import QSqlRelation, QSqlQuery

from Roadnet.roadnet_dialog import SrwrSpecialDesDlg
from Roadnet.generic_functions import ipdb_breakpoint
from srwr import WidgetInfoObject, WidgetTypeEnum, SrwrViewRecord
from srwr_maintenance import MaintenanceTable, SrwrAddMaintenanceRecord, SrwrModifyMaintenanceRecord, SrwrDeleteMaintenanceRecord


class SpecialDesignationTable(MaintenanceTable):
    """
    Inherits MaintenanceTable class. Makes changes for displaying records from the special designation table.
    """
    table = "tblSPEC_DES"
    hide_cols = [0, 3, 4, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20]
    whole_rd_col = 12
    currency_flag_col = 3
    usrn_col = 4
    start_end_coords_cols = [8, 9, 10, 11]

    def __init__(self, street_browser, usrn, db, tv, iface, params):
        """
        :param street_browser: street browser dialog
        :param usrn: usrn
        :param db: database connection
        :param tv: table view
        :param iface: qgis iface hook
        """
        super(SpecialDesignationTable, self).__init__(street_browser, usrn, db, tv, iface, params)

        self.dlg = SrwrSpecialDesDlg()

    def relate_lookup_tables(self, model):
        """
        Relate the lookup tables to the model data
        :param model: QSqlRelationalTableModel
        """
        model.setHeaderData(1, Qt.Horizontal, "ID")
        model.setRelation(12, QSqlRelation("tlkpWHOLE_ROAD", "whole_road", "description"))
        model.setHeaderData(12, Qt.Horizontal, "Whole Road")
        model.setRelation(13, QSqlRelation("tlkpORG", "swa_org_ref", "description"))
        model.setRelation(6, QSqlRelation("tlkpSPEC_DES", "designation_code", "designation_text"))
        model.setHeaderData(6, Qt.Horizontal, "Designation")
        model.setHeaderData(7, Qt.Horizontal, "Location")
        model.setHeaderData(2, Qt.Horizontal, "Version")
        model.setHeaderData(5, Qt.Horizontal, "Ref No")

    def view_or_modify(self, add=False, modify=False, delete=False, view=False):
        """
        Launch the Add, modify or view form.
        :param add: bool option
        :param modify: bool option
        :param delete: bool option
        :param view: bool option
        """
        # Current record in model to pass to form
        idx = self.table_view.selectionModel().currentIndex()

        # Create fresh instance of dialog
        self.dlg = SrwrSpecialDesDlg()

        widget_info = [WidgetInfoObject(self.dlg.ui.specDesIdLineEdit, WidgetTypeEnum.lineedit, 1, id_col=True),
                       WidgetInfoObject(self.dlg.ui.versionLineEdit, WidgetTypeEnum.lineedit, 2),
                       WidgetInfoObject(self.dlg.ui.refLineEdit, WidgetTypeEnum.lineedit, 5),
                       WidgetInfoObject(self.dlg.ui.locationTextEdit, WidgetTypeEnum.textedit, 7, white=True),
                       WidgetInfoObject(self.dlg.ui.descTextEdit, WidgetTypeEnum.textedit, 15, white=True),
                       WidgetInfoObject(self.dlg.ui.swaLineEdit, WidgetTypeEnum.lineedit, 13),
                       WidgetInfoObject(self.dlg.ui.designationLineEdit, WidgetTypeEnum.lineedit, 6),
                       WidgetInfoObject(self.dlg.ui.designationDateLineEdit, WidgetTypeEnum.lineedit, 14,
                                        date_col=True),
                       WidgetInfoObject(self.dlg.ui.entryDateLineEdit, WidgetTypeEnum.lineedit, 16, date_col=True),
                       WidgetInfoObject(self.dlg.ui.byLineEdit, WidgetTypeEnum.lineedit, 17),
                       WidgetInfoObject(self.dlg.ui.notesTextEdit, WidgetTypeEnum.textedit, 20, white=True),
                       WidgetInfoObject(self.dlg.ui.startXLineEdit, WidgetTypeEnum.lineedit, 8),
                       WidgetInfoObject(self.dlg.ui.startYLineEdit, WidgetTypeEnum.lineedit, 9),
                       WidgetInfoObject(self.dlg.ui.endXLineEdit, WidgetTypeEnum.lineedit, 10),
                       WidgetInfoObject(self.dlg.ui.endYLineEdit, WidgetTypeEnum.lineedit, 11),
                       WidgetInfoObject(self.dlg.ui.swaComboBox, WidgetTypeEnum.combo, 13, mapped=False),
                       WidgetInfoObject(self.dlg.ui.designationComboBox, WidgetTypeEnum.combo, 6, mapped=False),
                       WidgetInfoObject(self.dlg.ui.designationDateDateEdit, WidgetTypeEnum.dateedit, 14, mapped=False)]

        query_lst = {
            "SELECT description, swa_org_ref FROM tlkpORG": self.dlg.ui.swaComboBox,
            "SELECT designation_text, designation_code FROM tlkpSPEC_DES": self.dlg.ui.designationComboBox
            }

        if add:
            self.add_i = SrwrAddSpecialDesRecord(self.model, self.iface, self.db, self.street_browser, self.dlg,
                                                 self.whole_rd_col, self.currency_flag_col, self.usrn_col, widget_info,
                                                 query_lst, self.params)
            self.add_i.view(idx, self.usrn)
            self.disable_sb_modifications()
            self.dlg.ui.swaLabel.setStyleSheet("color : black")
        elif modify:
            # Hide links button as there are no poly links
            self.dlg.ui.editLinkPushButton.hide()
            self.add_i = SrwrModifySpecialDesRecord(self.model, self.iface, self.db, self.street_browser, self.dlg,
                                                    self.whole_rd_col, self.currency_flag_col, self.usrn_col,
                                                    widget_info, query_lst, self.params)
            self.add_i.view(idx, self.usrn)
            self.disable_sb_modifications()
            self.dlg.ui.swaLabel.setStyleSheet("color : black")
        elif delete:
            self.delete_i = SrwrDeleteSpecialDesRecord(self.street_browser, self.db, self.model, self.usrn,
                                                       self.table_view)
            self.delete_i.delete()
            self.signals.current_usrn_links.emit(self.usrn)
        elif view:
            self.view_i = SrwrViewRecord(self.model, self.iface, self.dlg, self.whole_rd_col, widget_info, self.params)
            self.view_i.view(idx, self.usrn)
        else:
            pass


class SrwrAddSpecialDesRecord(SrwrAddMaintenanceRecord):
    """
    Inherits from the SrwrAddMaintenanceRecord maintenance class. Overrides the methods which are specific to the
    maintenance records.
    """
    def __init__(self, model, iface, db, street_browser, dlg, whole_rd_col, currency_flag_col, usrn_col, widget_info,
                 query_lst, params):

        super(SrwrAddSpecialDesRecord, self).__init__(model, iface, db, street_browser, dlg, whole_rd_col,
                                                      currency_flag_col, usrn_col, widget_info, query_lst, params)
        self.valid_designation_rules = self.validation_sql()
        self.fields_to_validate = []

    def connect_widgets_validation(self):
        """
        Connect designation drop down changes to update the date field label and mandatory labels.
        """
        self.view_dlg.ui.designationComboBox.currentIndexChanged.connect(self.set_date_label)
        self.view_dlg.ui.designationComboBox.currentIndexChanged.connect(self.change_mandatory_labels)
        self.view_dlg.ui.designationComboBox.currentIndexChanged.connect(self.designation_mandatory_label)
        self.view_dlg.ui.locationTextEdit.textChanged.connect(self.location_text_changed)
        self.view_dlg.ui.wholeRoadCheckBox.stateChanged.connect(self.whole_rd_state)

    def disconnect_validation(self):
        """
        Disconnect all existing validation signals
        """
        try:
            self.view_dlg.ui.designationDateDateEdit.dateChanged.disconnect()
        except TypeError:
            pass
        try:
            self.view_dlg.ui.swaComboBox.currentIndexChanged.disconnect()
        except TypeError:
            pass
        try:
            self.view_dlg.ui.descTextEdit.textChanged.disconnect()
        except TypeError:
            pass

    def change_mandatory_labels(self, idx):
        """
        Resets the fields which are mandatory depending on the designation code
        :param idx: new combobox index
        """
        # Disconnect previous validation
        self.disconnect_validation()
        self.fields_to_validate = []
        # All labels black (default)
        self.view_dlg.ui.designationDateLabel.setStyleSheet("color : black")
        self.view_dlg.ui.swaLabel.setStyleSheet("color : black")
        self.view_dlg.ui.descriptionlabel.setStyleSheet("color : black")
        try:
            desig_code = self.view_dlg.ui.designationComboBox.itemData(idx)
            designation = self.valid_designation_rules[int(desig_code)]
            mand_fields = designation[0]
            # Split on comma
            mand_fields_c = [x.strip().lower() for x in mand_fields.split(',')]
            # Connect new mandatory field checks and force update for current values
            if 'date' in mand_fields_c:
                self.view_dlg.ui.designationDateDateEdit.dateChanged.connect(self.date_changed)
                self.date_changed(self.view_dlg.ui.designationDateDateEdit.date())
                self.fields_to_validate.append('date')
            if 'swa_org_ref' in mand_fields_c:
                self.view_dlg.ui.swaComboBox.currentIndexChanged.connect(self.swa_idx_changed)
                self.swa_idx_changed(self.view_dlg.ui.swaComboBox.currentIndex())
                self.fields_to_validate.append('swa_org_ref')
            if 'description' in mand_fields_c:
                self.view_dlg.ui.descTextEdit.textChanged.connect(self.desc_text_changed)
                self.desc_text_changed()
                self.fields_to_validate.append('description')
        except (KeyError, TypeError):
            pass

    def designation_mandatory_label(self, idx):
        """
        Set the designation label colour depending upon whether a value has been selected. idx 0 = blank
        :param idx: combo box index
        """
        if idx == 0:
            self.view_dlg.ui.designationLabel.setStyleSheet("color : red")
        else:
            self.view_dlg.ui.designationLabel.setStyleSheet("color : black")

    def date_changed(self, date):
        """
        Change the label colour to black if the date is not the default (01/01/2000)
        :param date: QDate from datepicker
        """
        if date.getDate() != (2000, 01, 01):
            self.view_dlg.ui.designationDateLabel.setStyleSheet("color : black")
        else:
            self.view_dlg.ui.designationDateLabel.setStyleSheet("color : red")

    def desc_text_changed(self):
        """
        Change the description field label colour if validation passes/fails
        """
        desc_len = len(self.view_dlg.ui.descTextEdit.toPlainText())
        if desc_len > 0:
            self.view_dlg.ui.descriptionlabel.setStyleSheet("color : black")
        else:
            self.view_dlg.ui.descriptionlabel.setStyleSheet("color : red")

    def view(self, idx, usrn):
        """
        Extends the default view behaviour for editing and custom behaviour for special designation tabs
        :param idx: model index
        :param usrn: usrn of current record
        """
        self.style_lineedits()
        self.enable_btns()
        self.switch_stacked()
        self.set_username()
        self.populate_combos()
        self.set_mandatory_fields()
        self.view_dlg.ui.editLinkPushButton.hide()
        ref_query = 'SELECT MAX(reference_no) FROM tblSPEC_DES WHERE usrn = '
        id_query = 'SELECT MAX(spec_des_id) FROM tblSPEC_DES'
        self.generate_ids(id_query, ref_query, self.db)
        self.entry_date_default()
        self.usrn = usrn
        self.view_dlg.show()

    def set_date_label(self, idx):
        """
        Set the date field label based on the designation type selected.
        :param idx: new combo index
        """
        try:
            desig_code = self.view_dlg.ui.designationComboBox.itemData(idx)
            designation = self.valid_designation_rules[int(desig_code)]
            date_text = designation[1]
            if date_text:
                self.view_dlg.ui.designationDateLabel.setText(date_text)
            else:
                self.view_dlg.ui.designationDateLabel.setText("Date Designated")
        except (KeyError, TypeError):
            # Add record defaults to 0/empty
            pass

    def save_record_changes(self):
        """
        Validate the changes, update rd poly links and create a new record in the model
        """
        self.save_dlg.close()
        maint_id = self.id_lineedit.text()
        self.revert_sb_modify_buttons()
        all_valid, err_kwargs = self.dynamic_validation()
        if all_valid:
            self.view_dlg.close()
            self.create_rd_poly_links(maint_id)
            # Create new record
            self.update_model()
            # Commit to db + insert any esu links
            self.model.submitAll()
            # Select the new record in the tableview
            last_row = int(self.model.rowCount())
            self.street_browser.ui.specDesTableView.selectRow(last_row - 1)
        else:
            self.validation_failed_messages(**err_kwargs)

    def dynamic_validation(self):
        """
        Different fields are validated depending upon the designation type for the record.
        """
        all_valid = True
        kwargs = {}
        if 'swa_org_ref' in self.fields_to_validate:
            valid_swa = self.validate_swa_mandatory()
            kwargs['swa'] = valid_swa
            if not valid_swa:
                all_valid = False
        if 'description' in self.fields_to_validate:
            valid_des = self.validate_desc()
            kwargs['desc'] = valid_des
            if not valid_des:
                all_valid = False
        if 'date' in self.fields_to_validate:
            valid_date = self.validate_designation_date()
            kwargs['des_date'] = valid_date
            if not valid_date:
                all_valid = False
        # Always validate location
        valid_loc = self.validate_location_mandatory()
        kwargs['location'] = valid_loc
        # Always validate Designation
        valid_desigation = self.validate_designation_mandatory()
        kwargs['designation'] = valid_desigation
        if not valid_loc or not valid_desigation:
            all_valid = False
        return all_valid, kwargs

    def validation_sql(self):
        """
        Builds a dict of the validation rules and what the date label should be, depending on the designation.
        :return: dict [designation code] = (mandatory field, date field name)
        """
        sql = "SELECT designation_code, date_text, mandatory_fields FROM tlkpSPEC_DES;"
        rules = {}
        query = QSqlQuery(sql, self.db)
        while query.next():
            code = int(query.value(0))
            date_text = query.value(1)
            mand_fields = query.value(2)
            rules[code] = (mand_fields, date_text)
        return rules

    def validate_designation_mandatory(self):
        """
        Check the designation has been set.
        :return: bool True if valid
        """
        cur_idx = self.view_dlg.ui.designationComboBox.currentIndex()
        text = self.view_dlg.ui.designationComboBox.itemText(cur_idx)
        if text:
            return True
        else:
            return False

    def validate_desc(self):
        """
        Check the description field has values
        """
        desc_len = len(self.view_dlg.ui.descTextEdit.toPlainText())
        if desc_len > 0:
            return True
        else:
            return False

    def validate_designation_date(self):
        """
        Checks the special designation date has been chosen
        """
        date_f = self.display_date_to_db(self.view_dlg.ui.designationDateDateEdit.text())
        if date_f == '20000101':
            return False
        else:
            return True


class SrwrModifySpecialDesRecord(SrwrModifyMaintenanceRecord, SrwrAddSpecialDesRecord):
    """
    Uses methods from both SrwrModifyMaintenanceRecord and SrwrAddSpecialDesRecord to produce a class which allows for
    modifying special designation records.
    """
    def __init__(self, model, iface, db, street_browser, dlg, whole_rd_col, currency_flag_col, usrn_col, widget_info,
                 query_lst, params):
        """
        :param model: model
        :param iface: qgis iface hook
        :param db: database connection
        :param street_browser: street browser dialog
        :param dlg: modify dialog
        :param whole_rd_col: int whole road column
        :param currency_flag_col: int currency flag column
        :param usrn_col: int usrn column
        :param widget_info: list of WidgetInfoObjects
        :param query_lst: list of custom spec des queries
        """
        super(SrwrModifySpecialDesRecord, self).__init__(model, iface, db, street_browser, dlg, whole_rd_col,
                                                         currency_flag_col, usrn_col, widget_info, query_lst, params)

    def view(self, idx, usrn):
        """
        Overrides base method to deal with a modification.
        :param idx: current record model index
        :param usrn: USRN of modified record link
        """
        row = idx.row()
        self.pre_edit_row = row

        self.style_lineedits()
        self.enable_btns()
        self.switch_stacked()
        self.populate_combos()
        self.set_mandatory_fields()

        self.mapper.setCurrentIndex(row)
        self.set_initial_values()
        self.entry_date_default()
        self.whole_road_checkbox(row)
        self.update_version_number()
        # After initial setup take a snapshot of values
        self.before_mod_values = self.snapshot_record_values()
        self.usrn = usrn
        self.view_dlg.show()

    def save_record_changes(self):
        """
        Validate the changes with validation specific to special designations
        """
        self.save_dlg.close()
        self.revert_sb_modify_buttons()
        validation = self.dynamic_validation()
        all_valid = validation[0]
        err_kwargs = validation[1]
        if all_valid:
            self.view_dlg.close()
            dirty = self.is_record_dirty()
            if dirty:
                # Create new record
                self.update_model()
                # Commit to db + insert any esu links
                self.model.submitAll()
            # Reselect the same row
            self.street_browser.ui.specDesTableView.selectRow(self.pre_edit_row)
        else:
            self.validation_failed_messages(**err_kwargs)

    def is_record_dirty(self):
        """
        Check if any edits have been made by comparing snapshot of data from before edit session started
        :rtype : bool
        :return : True if record is dirty
        """
        new_values = self.snapshot_record_values()
        for idx, org_value in self.before_mod_values.iteritems():
            if org_value != new_values[idx]:
                return True
        adopt_new = self.view_dlg.ui.designationDateDateEdit.text()
        adopt_old = self.view_dlg.ui.designationDateLineEdit.text()
        if adopt_new != adopt_old:
            # Default date in datepicker would equal empty string in lineedit
            if adopt_new != "01/01/2000":
                return True
        return False


class SrwrDeleteSpecialDesRecord(SrwrDeleteMaintenanceRecord):
    """
    Delete a special designation record.
    """

    id_col = 1

    def __init__(self, street_browser, db, model, usrn, table_view):
        """
        :param street_browser: Street browser dialog
        :param db: Qt database connection
        :param model: srwr model
        :param usrn: current usrn
        """
        super(SrwrDeleteSpecialDesRecord, self).__init__(street_browser, db, model, usrn, table_view)

    def delete(self):
        """
        Main method for deleting a record. Closes the record in tblSPEC_DES.
        """
        row = self.table_view.currentIndex().row()
        maint_id = self.model.data(self.model.index(row, self.id_col), Qt.DisplayRole)
        confirm_delete_dlg = QMessageBox("", "Are you sure you want to delete record " + str(maint_id),
                                         QMessageBox.Question, QMessageBox.Yes, QMessageBox.No,
                                         QMessageBox.NoButton, None, Qt.Dialog)
        confirm_delete_result = confirm_delete_dlg.exec_()
        if confirm_delete_result == QMessageBox.Yes:
            self.close_record_db(maint_id, 'tblSPEC_DES', 'spec_des_id')
            self.refresh_model()
            self.table_view.selectRow(0)
        if confirm_delete_result == QMessageBox.No:
            pass
