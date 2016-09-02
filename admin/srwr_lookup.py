# -*- coding: utf-8 -*-
import re

from PyQt4.QtSql import QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt4.QtGui import QMessageBox
from PyQt4.Qt import Qt
from Roadnet.generic_functions import ipdb_breakpoint
from Roadnet import config

__author__ = 'Alessandro Cristofori'


class SrwrLookup:

    def __init__(self, iface, db, srwr_lu_dia):
        self.iface = iface
        self.db = db
        self.srwr_lu_dia = srwr_lu_dia
        self.connect_buttons()
        self.items_model = None
        self.data_model = None
        self.queries = {
            0: """SELECT designation_code,
                  (designation_code || ' : ' || designation_text) AS 'display'
                  FROM tlkpSPEC_DES
                  ORDER BY designation_code""",
            1: """SELECT reinstatement_code,
                  (reinstatement_code || ' : ' || description) AS 'display'
                  FROM tlkpREINS_CAT
                  ORDER BY reinstatement_code""",
            2: """SELECT road_status_ref,
                  (road_status_ref || ' : ' || Description) AS 'display'
                  FROM tlkpROAD_STATUS
                  ORDER BY road_status_ref"""}
        self.tables = {
            0: "tlkpSPEC_DES",
            1: "tlkpREINS_CAT",
            2: "tlkpROAD_STATUS"}
        self.columns = {0: "designation_code",
                        1: "reinstatement_code",
                        2: "road_status_ref"}
        self.amend_queries = {
            0: """UPDATE tlkpSPEC_DES SET designation_text = '{0}'
                  WHERE designation_code = {1} """,
            1: """UPDATE tlkpREINS_CAT SET description = '{0}'
                  WHERE reinstatement_code = {1} """,
            2: """UPDATE tlkpROAD_STATUS SET Description = '{0}'
                  WHERE road_status_ref = {1}"""}
        self.changes_made = False
        # Setup initial view
        self.srwr_lu_dia.ui.desRadioButton.setChecked(True)
        self.populate_list(0)

    def connect_buttons(self):
        """
        events handler for buttons in the form
        :return: object
        """
        self.srwr_lu_dia.ui.addButton.clicked.connect(self.add_lookup)
        self.srwr_lu_dia.ui.removeButton.clicked.connect(self.remove_lookup)
        self.srwr_lu_dia.ui.amendButton.clicked.connect(self.amend_lookup)
        self.srwr_lu_dia.ui.closeButton.clicked.connect(self.close_browser)
        self.srwr_lu_dia.ui.desRadioButton.pressed.connect(lambda: self.populate_list(0))
        self.srwr_lu_dia.ui.reinsRadioButton.pressed.connect(lambda: self.populate_list(1))
        self.srwr_lu_dia.ui.statRadioButton.pressed.connect(lambda: self.populate_list(2))
        self.srwr_lu_dia.ui.itemsListView.pressed.connect(lambda: self.selection_handler())

    def close_browser(self):
        # close the dialog window
        if self.changes_made:
            changes_made_msg_box = QMessageBox(
                QMessageBox.Information, " ",
                "SRWR lookup tables updated.\n\n"
                "Restart roadNet to populate menus with new values.",
                QMessageBox.Ok,
                None)
            changes_made_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                                Qt.WindowTitleHint)
            changes_made_msg_box.exec_()
        self.srwr_lu_dia.close()

    def populate_list(self, table_id):
        """
        populate the list view on initialisation and when radio buttons are toggled,
        this view is just for show because QSqlQueryModel class does not handle editing
        but data need to be displayed as concatenated strings, this is not allowed in a
        QSqlTableModel class
        :param table_id: the id passed from the radio button
        :return: void
        """
        self.srwr_lu_dia.ui.typeDescLineEdit.clear()
        self.items_model = QSqlQueryModel()
        self.items_model.setQuery(self.queries[table_id], self.db)
        while self.items_model.canFetchMore():
            self.items_model.fetchMore()
        self.srwr_lu_dia.ui.typeNoSpinBox.setValue(0)
        self.srwr_lu_dia.ui.itemsListView.setModel(self.items_model)
        self.srwr_lu_dia.ui.itemsListView.setModelColumn(1)
        self.create_data_model(table_id)

    def create_data_model(self, table_id):
        """
        create an object from the QSqlTableModel class used to data modifications
        to send to the database
        :param table_id: the id passed from the radio button
        :return: void
        """
        self.data_model = QSqlTableModel(db=self.db)
        self.data_model.setTable(self.tables[table_id])
        self.data_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.data_model.setSort(2, Qt.AscendingOrder)
        self.data_model.select()
        while self.data_model.canFetchMore():
            self.data_model.fetchMore()

    def add_lookup(self):
        """
        get the max value each table model and increment of 1
        add a record to the database when the add button is pressed
        with the incremented value
        :return: void
        """
        ui = self.srwr_lu_dia.ui
        if ui.desRadioButton.isChecked():
            table_id = 0
            table = self.tables[table_id]
            ref_col = self.columns[0]
        elif ui.reinsRadioButton.isChecked():
            table_id = 1
            table = self.tables[table_id]
            ref_col = self.columns[1]
        elif ui.statRadioButton.isChecked():
            table_id = 2
            table = self.tables[table_id]
            ref_col = self.columns[2]

        # format text and numbers
        add_desc = str(ui.typeDescLineEdit.text()).strip()
        add_desc.replace("'", "''")
        add_code = ui.typeNoSpinBox.value()
        if add_desc == "" or add_code is None:
            desc_error_msg_box = QMessageBox(QMessageBox.Warning,
                                             " ",
                                             "You must enter the code AND description",
                                             QMessageBox.Ok,
                                             None)
            desc_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                              Qt.WindowTitleHint)
            desc_error_msg_box.exec_()
            return

        # avoid duplicate insertion on double click on 'Add' button
        sel_model = ui.itemsListView.selectionModel()
        if sel_model.selectedIndexes():
            # extracts just the id from the string
            sel_items = sel_model.selectedIndexes()[0]
            item_data = str(sel_items.data())
            p = re.compile("([0-9]{1,3})(?=\s:)")
            src = p.search(item_data)
            item_id = int(src.group(1))
            if item_id == add_code:
                dups_error_msg_box = QMessageBox(QMessageBox.Warning,
                                                 " ",
                                                 "Cannot add duplicate values",
                                                 QMessageBox.Ok,
                                                 None)
                dups_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                                  Qt.WindowTitleHint)
                dups_error_msg_box.exec_()
                return

        # Avoid duplicate insertion by checking database
        sql_find_duplicates = """SELECT {0} FROM {1}
                                 WHERE {0} IS '{2}'""".format(ref_col,
                                                              table,
                                                              add_code)
        if config.DEBUG_MODE:
            print('DEBUG_MODE: find_duplicates: {}'.format(
                sql_find_duplicates))
        query = QSqlQuery(sql_find_duplicates, self.db)
        if query.first():  # False unless value already found in table
            dup_values_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                             "Cannot add duplicate values",
                                             QMessageBox.Ok, None)
            dup_values_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                              Qt.WindowTitleHint)
            dup_values_msg_box.exec_()
            return

        # create the record to insert
        data_model_idx = self.data_model.createIndex(self.data_model.rowCount() - 1, 0)
        insert_record = self.data_model.record(self.items_model.rowCount())
        insert_record.setValue(1, add_code)
        insert_record.setValue(2, add_desc)
        insert_record.setValue(3, str(""))
        insert_record.setValue(4, str(""))
        self.data_model.insertRecord(self.items_model.rowCount(), insert_record)
        if self.data_model.submitAll():
            # clear the line input and selects the newly created value on the list
            ui.typeDescLineEdit.clear()
            ui.typeNoSpinBox.setValue(1)
            self.populate_list(table_id)
            index = ui.itemsListView.model().createIndex(self.items_model.rowCount() - 1, 1)
            ui.itemsListView.setCurrentIndex(index)
            self.changes_made = True
        else:
            db_error_msg_box = QMessageBox(QMessageBox.Warning,
                                           " ",
                                           "Error: {}".format(
                                               self.data_model.lastError().text()),
                                           QMessageBox.Ok,
                                           None)
            db_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            db_error_msg_box.exec_()
            return

    def selection_handler(self, table_id=None):
        """
        Populate the typeNoSpinBox and typeDescLineEdit with data from the 
        selected row in the list.  The data are extracted from the string
        value itself, without reference to the original model.
        :return void:
        """
        # print all selected list items to the text box
        sel_model = self.srwr_lu_dia.ui.itemsListView.selectionModel()
        sel_items = sel_model.selectedIndexes()[0]
        item_data = str(sel_items.data())
        # split text from the code number
        p = re.compile("\:(.*)")
        src = p.search(item_data)
        item_text = str(src.group(1)[1:])
        p = re.compile("([0-9]{1,3})(?=\s:)")
        src = p.search(item_data)
        item_id = int(src.group(1))
        self.srwr_lu_dia.ui.typeNoSpinBox.setValue(item_id)
        self.srwr_lu_dia.ui.typeDescLineEdit.setText(item_text)

    def remove_lookup(self):
        """
        this function deletes selected items from the list view and db, only if
        the lookups are not used, in this case it prevents the removal displaying
        the list of the streets that use the lookup
        :return: void
        """
        ui = self.srwr_lu_dia.ui
        if ui.desRadioButton.isChecked():
            table_id = 0
            table = self.tables[table_id]
            ref_col = self.columns[0]
            sql_usrns = "SELECT usrn FROM tblSPEC_DES WHERE " \
                         "(designation_code = {0} AND currency_flag=0);" \
                         .format(str(ui.typeNoSpinBox.value()))
        elif ui.reinsRadioButton.isChecked():
            table_id = 1
            table = self.tables[table_id]
            ref_col = self.columns[1]
            sql_usrns = "SELECT usrn FROM tblREINS_CAT WHERE " \
                         "(reinstatement_code = {0} AND currency_flag=0);" \
                         .format(str(ui.typeNoSpinBox.value()))
        elif ui.statRadioButton.isChecked():
            table_id = 2
            table = self.tables[table_id]
            ref_col = self.columns[2]
            sql_usrns = "SELECT usrn FROM tblMaint WHERE " \
                         "(road_status_ref = {0} AND currency_flag=0);" \
                         .format(str(ui.typeNoSpinBox.value()))

        data_model = self.data_model
        item_text = ui.typeDescLineEdit.text()
        item_ref = ui.typeNoSpinBox.value()
        selection_model = ui.itemsListView.selectionModel()
        try:
            item_to_remove = selection_model.selectedIndexes()[0]
        except IndexError:  # Throws if nothing selected
            return

        # prevent deleting the default lookup just for designation and road status
        if table_id == 0 or table_id == 2:
            if item_text == "-none-" or item_ref == 0:
                # not_remove_message = self.srwr_lu_dia.ui.removeButton
                remove_error_msg_box = QMessageBox(QMessageBox.Warning,
                                                   " ",
                                                   "This item cannot be removed",
                                                   QMessageBox.Ok,
                                                   None)
                remove_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                                    Qt.WindowTitleHint)
                remove_error_msg_box.exec_()
                return

        # Check for USRNs that use this item
        query = QSqlQuery(sql_usrns, self.db)
        usrns = []
        while query.next():
            usrns.append(str(query.value(0)))
        if len(usrns) > 0:
            # Create a message
            message = ("This item cannot be deleted because is used by the "
                       "following streets: \n")
            usrns_string = ', '.join(usrns[:20])
            if len(usrns) > 20:
                usrns_string += ' and more...'
            long_message = message + usrns_string
            # Display warning message in box, then exit
            item_not_deletable_msg_box = QMessageBox(QMessageBox.Warning,
                                                    " ",
                                                    long_message,
                                                    QMessageBox.Ok,
                                                    None)
            item_not_deletable_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                                      Qt.WindowTitleHint)
            item_not_deletable_msg_box.exec_()
            return

        # Remove selected row and clear the line edit
        sql_remove_item = """DELETE FROM {}
                             WHERE {} IS {};""".format(table, ref_col,
                                                       item_ref)
        if config.DEBUG_MODE:
            print('DEBUG_MODE: remove_item: {}'.format(
                sql_remove_item))
        query = QSqlQuery(sql_remove_item, self.db)  # Query is excuted here
        ui.typeDescLineEdit.clear()

        # Check the delete was successful
        if query.numRowsAffected > 0:
            # Repopulate table and select previous item in list
            self.populate_list(table_id)
            if item_to_remove.row() == 0:
                index = ui.itemsListView.model().createIndex(0, 1)
            else:
                index = ui.itemsListView.model().createIndex(
                    item_to_remove.row() - 1, 1)
            ui.itemsListView.setCurrentIndex(index)
            self.selection_handler(table_id)
            self.changes_made = True
        else:
            db_error_msg_box = QMessageBox(QMessageBox.Warning,
                                           " ",
                                           "Error: {}".format(
                                               data_model.lastError.text(),
                                           QMessageBox.Ok,
                                           None))
            db_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint |
                                            Qt.WindowTitleHint)
            db_error_msg_box.exec_()
        return
    
    def amend_lookup(self):
        """
        change the value of existing lookup items, this time are used db queries
        :return: void
        """
        table_id = None
        if self.srwr_lu_dia.ui.typeDescLineEdit.text() == "":
            return
        item_id = self.srwr_lu_dia.ui.typeNoSpinBox.value()
        selection_model = self.srwr_lu_dia.ui.itemsListView.selectionModel()
        selection_indexes = selection_model.selectedIndexes()
        # if nothing is selects exit the function
        if not selection_indexes:
            return
        selection_index = selection_indexes[0]
        if selection_index.data() == "0 : -none-":
            # if the selected value is -none- fire an alert
            not_edit_msg_box = QMessageBox(QMessageBox.Warning,
                                           " ",
                                           "This item cannot be edited",
                                           QMessageBox.Ok,
                                           None)
            not_edit_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            not_edit_msg_box.exec_()
            return
        # changes the values directly onto the db
        des_radio_btn = self.srwr_lu_dia.ui.desRadioButton
        reins_radio_btn = self.srwr_lu_dia.ui.reinsRadioButton
        stat_radio_btn = self.srwr_lu_dia.ui.statRadioButton
        amend_query = QSqlQuery(self.db)
        if des_radio_btn.isChecked():
            table_id = 0
            format_query = self.amend_queries[0].format(self.srwr_lu_dia.ui.typeDescLineEdit.text(), item_id)
            if not amend_query.exec_(format_query):
                db_error_msg_box = QMessageBox(QMessageBox.Warning,
                                               " ",
                                               "Error: {}".format(
                                                   amend_query.lastError().text()),
                                               QMessageBox.Ok,
                                               None)
                db_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                db_error_msg_box.exec_()
        if reins_radio_btn.isChecked():
            table_id = 1
            format_query = self.amend_queries[1].format(self.srwr_lu_dia.ui.typeDescLineEdit.text(), item_id)
            if not amend_query.exec_(format_query):
                db_error_msg_box = QMessageBox(QMessageBox.Warning,
                                               " ",
                                               "Error: {}".format(
                                                   amend_query.lastError().text()),
                                               QMessageBox.Ok,
                                               None)
                db_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                db_error_msg_box.exec_()
        if stat_radio_btn.isChecked():
            table_id = 2
            format_query = self.amend_queries[2].format(self.srwr_lu_dia.ui.typeDescLineEdit.text(), item_id)
            if not amend_query.exec_(format_query):
                db_error_msg_box = QMessageBox(QMessageBox.Warning,
                                               " ",
                                               "Error: {}".format(
                                                   amend_query.lastError().text()),
                                               QMessageBox.Ok,
                                               None)
                db_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                db_error_msg_box.exec_()
        # closes the query and repopulate the list
        self.changes_made = True
        amend_query.clear()
        self.populate_list(table_id)
