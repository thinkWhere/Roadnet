# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox
from PyQt4.QtSql import QSqlRelation, QSqlQuery

from Roadnet.roadnet_dialog import SrwrReinsCatDlg
from srwr import WidgetInfoObject, WidgetTypeEnum, SrwrViewRecord
from srwr_maintenance import (
    SrwrAddMaintenanceRecord,
    SrwrModifyMaintenanceRecord,
    SrwrDeleteMaintenanceRecord)
from srwr_special_designation import SpecialDesignationTable

import datetime

class ReinstatementCategoriesTable(SpecialDesignationTable):
    """
    Inherits MaintenanceTable class. Makes changes for displaying records from the special designation table.
    """
    table = "tblREINS_CAT"
    hide_cols = [0, 3, 4, 8, 9, 10, 11, 13, 14, 15, 16, 17]
    whole_rd_col = 12
    currency_flag_col = 3
    usrn_col = 4
    start_end_coords_cols = [8, 9, 10, 11]

    def __init__(self, street_browser, usrn, db, tv, iface, params):
        super(ReinstatementCategoriesTable, self).__init__(street_browser, usrn, db, tv, iface, params)

    def relate_lookup_tables(self, model):
        """
        Relate the lookup tables to the model data
        :param model: QSqlRelationalTableModel
        """
        model.setHeaderData(1, Qt.Horizontal, "ID")
        model.setRelation(6, QSqlRelation("tlkpREINS_CAT", "reinstatement_code", "description"))
        model.setHeaderData(6, Qt.Horizontal, "Category")
        model.setRelation(12, QSqlRelation("tlkpWHOLE_ROAD", "whole_road", "description"))
        model.setHeaderData(12, Qt.Horizontal, "Whole Road")
        model.setHeaderData(2, Qt.Horizontal, "Version")
        model.setHeaderData(5, Qt.Horizontal, "Ref No")
        model.setHeaderData(7, Qt.Horizontal, "Location")

    def view_or_modify(self, add=False, modify=False, delete=False, view=False):
        """
        Launch the Add, modify or view form
        :param add: bool option
        :param modify: bool option
        :param delete: bool option
        :param view: bool option
        """
        # Current record in model to pass to form
        idx = self.table_view.selectionModel().currentIndex()

        # Create fresh instance of dialog
        self.dlg = SrwrReinsCatDlg()
        self.dlg.ui.editLinkPushButton.hide()
        self.dlg.ui.swaLabel.setStyleSheet("color : black")

        widget_info = [WidgetInfoObject(self.dlg.ui.reinsCatIdLineEdit, WidgetTypeEnum.lineedit, 1, id_col=True),
                       WidgetInfoObject(self.dlg.ui.versionLineEdit, WidgetTypeEnum.lineedit, 2),
                       WidgetInfoObject(self.dlg.ui.refLineEdit, WidgetTypeEnum.lineedit, 5),
                       WidgetInfoObject(self.dlg.ui.categoryLineEdit, WidgetTypeEnum.lineedit, 6),
                       WidgetInfoObject(self.dlg.ui.locationTextEdit, WidgetTypeEnum.textedit, 7, white=True),
                       WidgetInfoObject(self.dlg.ui.entryDateLineEdit, WidgetTypeEnum.lineedit, 13, date_col=True),
                       WidgetInfoObject(self.dlg.ui.byLineEdit, WidgetTypeEnum.lineedit, 15),
                       WidgetInfoObject(self.dlg.ui.notesTextEdit, WidgetTypeEnum.textedit, 17, white=True),
                       WidgetInfoObject(self.dlg.ui.startXLineEdit, WidgetTypeEnum.lineedit, 8),
                       WidgetInfoObject(self.dlg.ui.startYLineEdit, WidgetTypeEnum.lineedit, 9),
                       WidgetInfoObject(self.dlg.ui.endXLineEdit, WidgetTypeEnum.lineedit, 10),
                       WidgetInfoObject(self.dlg.ui.endYLineEdit, WidgetTypeEnum.lineedit, 11),
                       WidgetInfoObject(self.dlg.ui.categoryComboBox, WidgetTypeEnum.combo, 6)]

        query_lst = {
            "SELECT description, reinstatement_code FROM tlkpREINS_CAT": self.dlg.ui.categoryComboBox
            }

        if add:
            self.add_i = SrwrAddReinstatementCatRecord(self.model, self.iface, self.db, self.street_browser, self.dlg,
                                                       self.whole_rd_col, self.currency_flag_col, self.usrn_col,
                                                       widget_info, query_lst, self.params)
            self.add_i.view(idx, self.usrn)
            self.disable_sb_modifications()
            self.dlg.ui.swaLabel.setStyleSheet("color : black")
        elif modify:
            # Hide links button as there are no poly links
            self.add_i = SrwrModifyReinstatementCatRecord(self.model, self.iface, self.db, self.street_browser,
                                                          self.dlg, self.whole_rd_col, self.currency_flag_col,
                                                          self.usrn_col, widget_info, query_lst, self.params)
            self.add_i.view(idx, self.usrn)
            self.disable_sb_modifications()
            self.dlg.ui.swaLabel.setStyleSheet("color : black")
        elif delete:
            self.delete_i = SrwrDeleteReinstatementCatRecord(self.street_browser, self.db, self.model, self.usrn,
                                                             self.table_view)
            self.delete_i.delete()
            self.signals.current_usrn_links.emit(self.usrn)
        elif view:
            self.view_i = SrwrViewRecord(self.model, self.iface, self.dlg, self.whole_rd_col, widget_info, self.params)
            self.view_i.view(idx, self.usrn)
        else:
            pass


class SrwrAddReinstatementCatRecord(SrwrAddMaintenanceRecord):
    """
    Inherits from the SrwrAddMaintenanceRecord maintenance class. Overrides the methods which are specific to the
    maintenance records.
    """
    def __init__(self, model, iface, db, street_browser, dlg, whole_rd_col, currency_flag_col, usrn_col, widget_info,
                 query_lst, params):
        """
        :param model: Model
        :param iface: qgis iface hook
        :param db: database connection
        :param street_browser: street browser dlg instance
        :param dlg: modify dialog instance
        :param whole_rd_col: int whole road column
        :param currency_flag_col: int currency flag
        :param usrn_col: int usrn column
        :param widget_info: list of WidgetInfoObjects
        :param query_lst: list of queries for reinstatement cats
        """
        super(SrwrAddReinstatementCatRecord, self).__init__(model, iface, db, street_browser, dlg, whole_rd_col,
                                                            currency_flag_col, usrn_col, widget_info, query_lst, params)

        self.valid_cat_rules = None

    def view(self, idx, usrn):
        """
        Extends the default view behaviour for editing
        :param idx: model index
        :param usrn: current usrn
        """
        self.style_lineedits()
        self.enable_btns()
        self.switch_stacked()
        self.set_username()
        self.populate_combos()
        self.set_mandatory_fields()
        self.view_dlg.ui.editLinkPushButton.hide()
        ref_query = 'SELECT MAX(reference_no) FROM tblREINS_CAT WHERE usrn = '
        id_query = "SELECT MAX(reins_cat_id) FROM tblREINS_CAT"
        self.generate_ids(id_query, ref_query, self.db)
        self.entry_date_default()
        self.usrn = usrn
        self.view_dlg.show()

    def save_record_changes(self):
        """
        Validate the changes with validation specific to reinstatement categories
        """
        self.save_dlg.close()
        self.revert_sb_modify_buttons()
        # Check location text is present
        valid_loc = self.validate_location_mandatory()
        valid_cat = self.validate_category()
        if valid_loc and valid_cat:
            self.view_dlg.close()
            # Create new record
            self.update_model()
            # Commit to db + insert any esu links
            self.model.submitAll()
            # Select the new record in the tableview
            last_row = int(self.model.rowCount())
            self.street_browser.ui.reinstCatTableView.selectRow(last_row - 1)
        else:
            kwargs = {'location': valid_loc,
                      'category': valid_cat}
            self.validation_failed_messages(**kwargs)

    def category_idx_changed(self, idx):
        """
        Change the category label text if a category is selected
        :param idx: index of dropdown
        """
        # Change the label colour if required
        if idx != 0:
            self.view_dlg.ui.swaLabel.setStyleSheet("color : black")
        else:
            self.view_dlg.ui.swaLabel.setStyleSheet("color : red")

    def validate_category(self):
        """
        Checks that a record can only be saved if no other whole road records exist in the same category.
        :return: bool validation result
        """
        # Populate code dict
        if not self.valid_cat_rules:
            self.valid_cat_rules = self.category_validation_sql()
        # Get the current category code
        cur_idx = self.view_dlg.ui.categoryComboBox.currentIndex()
        code = int(self.view_dlg.ui.categoryComboBox.itemData(cur_idx))
        cur_category = int(self.valid_cat_rules[code])
        # Check that all other records are not whole road and the same category as new/modified record
        valid = True
        current_id = int(self.view_dlg.ui.reinsCatIdLineEdit.text())
        rc = self.model.rowCount()
        counter = 0
        while counter < rc:
            whole_rd = self.model.data(self.model.index(counter, self.whole_road_col), Qt.DisplayRole)
            id_ = int(self.model.data(self.model.index(counter, 1), Qt.DisplayRole))
            exist_code_txt = self.model.data(self.model.index(counter, 6), Qt.DisplayRole)
            code_idx = self.view_dlg.ui.categoryComboBox.findText(exist_code_txt)
            exist_code = self.view_dlg.ui.categoryComboBox.itemData(code_idx)
            exist_cat = int(self.valid_cat_rules[int(exist_code)])
            # Must be whole road, same category code and not the same record
            if (whole_rd.lower() == "yes") and (exist_cat == cur_category) and (current_id != id_):
                valid = False
                break
            counter += 1
        return valid

    def category_validation_sql(self):
        """
        Populate a dict with validation rules for different record categories
        :return: dict of cateogry rules
        """
        sql = "SELECT reinstatement_code, category FROM tlkpREINS_CAT;"
        rules = {}
        query = QSqlQuery(sql, self.db)
        while query.next():
            code = query.value(0)
            category = query.value(1)
            rules[code] = category
        return rules


class SrwrModifyReinstatementCatRecord(SrwrModifyMaintenanceRecord, SrwrAddReinstatementCatRecord):
    """
    Uses methods from both SrwrModifyMaintenanceRecord and SrwrAddReinstatementCatRecord to produce a class which allows
    for modifying special designation records.
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
        :param query_lst: list of custom reinstatement queries
        """
        super(SrwrModifyReinstatementCatRecord, self).__init__(model, iface, db, street_browser, dlg, whole_rd_col,
                                                               currency_flag_col, usrn_col, widget_info, query_lst,
                                                               params)

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
        Validate the changes with methods specific to reinstatement categories
        """
        self.save_dlg.close()
        self.revert_sb_modify_buttons()
        valid_loc = self.validate_location_mandatory()
        valid_cat = self.validate_category()
        if valid_loc and valid_cat:
            self.view_dlg.close()
            dirty = self.is_record_dirty()
            if dirty:
                # Create new record
                self.update_model()
                # Commit to db + insert any esu links
                self.model.submitAll()
            # Reselect the same row
            self.street_browser.ui.reinstCatTableView.selectRow(self.pre_edit_row)
        else:
            kwargs = {'location': valid_loc,
                      'category': valid_cat}
            self.validation_failed_messages(**kwargs)

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
        return False


class SrwrDeleteReinstatementCatRecord(SrwrDeleteMaintenanceRecord):
    """
    Delete a reinstatement category record.
    """

    id_col = 1

    def __init__(self, street_browser, db, model, usrn, table_view):
        """
        :param street_browser: Street browser dialog
        :param db: Qt database connection
        :param model: srwr model
        :param usrn: current usrn
        """
        super(SrwrDeleteReinstatementCatRecord, self).__init__(street_browser, db, model, usrn, table_view)

    def delete(self):
        """
        Main method for deleting a record. Closes the record in tblREINS_CAT.
        """
        row = self.table_view.currentIndex().row()
        maint_id = self.model.data(self.model.index(row, self.id_col), Qt.DisplayRole)
        confirm_delete_dlg = QMessageBox("", "Are you sure you want to delete record " + str(maint_id),
                                         QMessageBox.Question, QMessageBox.Yes, QMessageBox.No,
                                         QMessageBox.NoButton, None, Qt.Dialog)
        confirm_delete_result = confirm_delete_dlg.exec_()
        if confirm_delete_result == QMessageBox.Yes:
            self.close_record_db(maint_id, 'tblREINS_CAT', 'reins_cat_id')
            self.refresh_model()
            self.table_view.selectRow(0)
        if confirm_delete_result == QMessageBox.No:
            pass
