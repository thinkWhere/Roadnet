# -*- coding: utf-8 -*-
import datetime
import os

from PyQt4.QtGui import QFileDialog, QMessageBox, QPixmap, QIcon
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtCore import Qt
from export_street_report import StreetReportsExport

__author__ = 'matthew.bradley'


class ExportStreetReport:
    def __init__(self, iface, db, st_dia, params):
        self.iface = iface
        self.db = db
        self.street_dia = st_dia
        self.params = params
        self.export_path = None
        self.str_rb = None
        self.tbl_rb = None
        self.csv_chx = None
        self.report = None
        self.app_root = os.path.dirname(os.path.dirname(__file__))
        self.open_image = QPixmap(os.path.join(self.app_root,
                                               "image",
                                               "folder_open_icon.png"))
        self.home_dir = os.path.expanduser('~')
        self.street_dia.ui.fileOpenPushButton.setIcon(QIcon(self.open_image))
        self.street_dia.ui.fileOpenPushButton.setToolTip("Select File")
        self.model_navigation()

    def model_navigation(self):
        # handles events on widgets
        self.street_dia.ui.fileOpenPushButton.clicked.connect(self.select_file)

        self.street_dia.ui.cancelPushButton.clicked.connect(self.close_browser)
        self.street_dia.ui.okPushButton.clicked.connect(self.submit_export)
        self.street_dia.ui.changedStsRadioButton.pressed.connect(self.enable_streets)
        self.street_dia.ui.tblsRadioButton.pressed.connect(self.disable_streets)
        self.street_dia.ui.tblsComboBox.currentIndexChanged.connect(self.populate_list)

    def close_browser(self):
        # close the browser
        self.street_dia.close()

    def populate_list(self, current):
        """
        changes the content of the list widget according to the selected value
        in the combo box
        :param current: the current combo box index
        :return: void
        """
        # 0 = None,  1 = maintenance, 2 = reinstatement, 3 = special designation
        qry = {0: [],
               1: ['SELECT * from tlkpRoad_Status', 'Description', 'Road_Status_Ref'],
               2: ['SELECT * from tlkpREINS_CAT', 'Description', 'Reinstatement_Code'],
               3: ['SELECT designation_code,designation_text from tlkpSPEC_DES', 'Designation_Text', 'Designation_code']
               }
        # if the parameter is not null change the query accordingly
        if current != 0:
            query = QSqlQuery(self.db)
            query.exec_(qry.get(current)[0])
            rec = query.record()
            # aval are the names of the indexes columns
            aval = [rec.indexOf(qry.get(current)[1]), rec.indexOf(qry.get(current)[2])]
            self.street_dia.ui.listWidget.clear()
            while query.next():
                # adds values to widget list
                entry = str(query.value(aval[1])) + ": " + str(query.value(aval[0]))
                self.street_dia.ui.listWidget.addItem(entry)
            # Select the first item
            first_item = self.street_dia.ui.listWidget.item(0)
            first_item.setSelected(True)
        else:
            self.street_dia.ui.listWidget.clear()

    def select_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setDirectory(self.home_dir)
        self.street_dia.ui.fileLineEdit.setText(
            dialog.getSaveFileName(dialog, "Street Report", os.path.join(self.home_dir, "RNStreetReport")))

    def disable_streets(self):
        # disable the additional tables reporting option
        # and enable the diachronic reporting option
        self.street_dia.ui.dateEdit.setEnabled(False)
        self.street_dia.ui.tblsComboBox.setEnabled(True)
        self.street_dia.ui.listWidget.setEnabled(True)

    def enable_streets(self):
        # disable the diachronic reporting option
        # enable the additional tables reporting option
        self.street_dia.ui.listWidget.clear()
        self.street_dia.ui.tblsComboBox.setCurrentIndex(0)
        self.street_dia.ui.dateEdit.setEnabled(True)
        self.street_dia.ui.tblsComboBox.setEnabled(False)
        self.street_dia.ui.listWidget.setEnabled(False)

    def submit_export(self):
        """
        when the ok button is presses it runs the main export class,
        gets alla data from widgets and instantiate a StreetReportsExport class
        :return:
        """
        self.export_path = self.street_dia.ui.fileLineEdit.text()
        if self.export_path is None or self.export_path == "":
            no_export_path_msg_box = QMessageBox(QMessageBox.Warning, " ", "You must select an export file path",
                                                 QMessageBox.Ok, None)
            no_export_path_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_export_path_msg_box.exec_()
            return
        date = self.street_dia.ui.dateEdit.date().toPyDate()
        if date.year < 1997:
            wrong_date_msg_box = QMessageBox(QMessageBox.Warning, " ", "No records present before 01/01/1997",
                                             QMessageBox.Ok, None)
            wrong_date_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            wrong_date_msg_box.exec_()
            return
        if date > datetime.date.today():
            not_valid_date_msg_box = QMessageBox(QMessageBox.Warning, " ", "Change Date not valid",
                                                 QMessageBox.Ok, None)
            not_valid_date_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            not_valid_date_msg_box.exec_()
            return
        formatted_date = date.strftime("%Y%m%d")

        # dictionary containing another dictionary which keys are
        # the option of the report format (date or optional table)
        # and values are the values selected for each widget
        self.report = dict(streets=dict(radio=self.street_dia.ui.changedStsRadioButton.isChecked(),
                                        result=formatted_date),
                           tables=dict(radio=self.street_dia.ui.tblsRadioButton.isChecked(),
                                       result=self.street_dia.ui.listWidget.selectedItems(),
                                       combo=self.street_dia.ui.tblsComboBox.currentIndex(),
                                       type=self.street_dia.ui.tblsComboBox.currentText()),
                           )
        # optional CSV formatting option checkbox
        self.csv_chx = self.street_dia.ui.csvCheckBox.isChecked()
        # export class instantiation
        export = StreetReportsExport(self.iface, self.db, self.export_path,
                                     self.report, self.csv_chx,
                                     self.street_dia, self.params)
        # run the export
        export.run_export()


