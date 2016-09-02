# -*- coding: utf-8 -*-
import os
from PyQt4.QtGui import (
        QFileDialog,
        QMessageBox,
        QCheckBox,
        QProgressDialog,
        QIcon,
        QPixmap)
from Roadnet.exports.export_validation_threaded import (
        CheckAsdCoords,
        CheckMaintReins,
        CheckStartEnd,
        CheckTinyEsus,
        DupEsuRef,
        DupStreetDesc,
        EndReport,
        InitGlobals,
        InvalidCrossReferences,
        MaintNoPoly,
        NoLinkEsuStreets,
        PolyNoMaint,
        StartReport,
        StreetsNoEsuDesc,
        Type3Desc)
from Roadnet.exports.export_validation_report import ExportValidationReport
from Roadnet.admin.validation_summary import ValidationSummary
from PyQt4.QtCore import Qt, QRegExp, QThreadPool, pyqtSlot
from PyQt4.QtSql import QSqlQuery
from Roadnet.roadnet_dialog import ValidationSummaryDock
from Roadnet import database


__author__ = 'Alessandro Cristofori'


class Validation:
    def __init__(self, iface, db, validation_dia, plugin_dir, params):
        self.iface = iface
        self.db = db
        self.params = params
        self.validation_dia = validation_dia
        self.app_root = plugin_dir
        self.open_image = QPixmap(os.path.join(self.app_root,
                                               "image",
                                               "folder_open_icon.png"))
        self.validation_dia.ui.openPushButton.setIcon(QIcon(self.open_image))
        self.validation_dia.ui.openPushButton.setToolTip("Select File")
        self.export_globals = None
        self.validation_dk = None
        self.report_to_dialog = None
        self.re = QRegExp("CheckBox")
        self.check_boxes_names = []
        self.long_task = QThreadPool(None).globalInstance()
        self.summary_tables = {}
        self.model_navigation()
        self.form_load()
        self.file_dialog = QFileDialog()
        self.summary_functions = {}
        self.report_file_path = None
        self.home_dir = os.path.expanduser('~')
        self.org_name = database.get_from_gaz_metadata(db, "owner")
        self.report = ExportValidationReport("roadNet Validation Report",
                                             self.org_name,
                                             self.db, self.iface, None)
        self.list_check_boxes = []
        self.progress_win = QProgressDialog("", None, 0, 100, self.validation_dia)
        self.progress_win.setFixedSize(380, 100)
        self.progress_win.setModal(True)
        self.progress_win.setWindowTitle("Export Validation Report")

        self.summary_runnables = {'dupStreetCheckBox': [lambda: DupStreetDesc(), 0],
                                  'notStreetEsuCheckBox': [lambda: StreetsNoEsuDesc(), 1],
                                  'notType3CheckBox': [lambda: Type3Desc(False), 2],
                                  'incFootPathCheckBox': [lambda: Type3Desc(True), 2],
                                  'dupEsuRefCheckBox': [lambda: DupEsuRef(True), 3],
                                  'notEsuStreetCheckBox': [lambda: NoLinkEsuStreets(), 4],
                                  'invCrossRefCheckBox': [lambda: InvalidCrossReferences()],
                                  'startEndCheckBox': [lambda: CheckStartEnd(), 8],
                                  'tinyEsuCheckBox': [lambda: CheckTinyEsus("esu", 1)],
                                  'notMaintReinsCheckBox': [lambda: CheckMaintReins()],
                                  'asdStartEndCheckBox': [lambda: CheckAsdCoords()],
                                  'notMaintPolysCheckBox': [lambda: MaintNoPoly(), 16],
                                  'notPolysMaintCheckBox': [lambda: PolyNoMaint()],
                                  'tinyPolysCheckBox': [lambda: CheckTinyEsus("rd_poly", 1)]}

    def init_functions(self, ref_class, tolerance):
        """
        initialise a dictionary which keys are names of check boxes
        and values are all functions that create the respective table on the screen report
        functions are lambda because they will be called upon report creation and
        int references to a dictionary in the validation_summary
        class to the associated table widget to populate
        :param ref_class: class, the class holding the relative function
        :return: void
        """

        self.summary_functions = {'dupStreetCheckBox': [lambda: ref_class.dup_street_desc(), 0],
                                  'notStreetEsuCheckBox': [lambda: ref_class.street_not_esu_desc(), 1],
                                  'notType3CheckBox': [lambda: ref_class.no_type3_desc(include_footpath=False), 2],
                                  'incFootPathCheckBox': [lambda: ref_class.no_type3_desc(include_footpath=True), 2],
                                  'dupEsuRefCheckBox': [lambda: ref_class.dup_esu_ref(), 3],
                                  'notEsuStreetCheckBox': [lambda: ref_class.no_link_esu_streets(), 4],
                                  'invCrossRefCheckBox': [lambda: ref_class.invalid_cross_references()],
                                  'startEndCheckBox': [lambda: ref_class.check_start_end(tolerance), 8],
                                  'tinyEsuCheckBox': [lambda: ref_class.check_tiny_esus("esu", 1)],
                                  'notMaintReinsCheckBox': [lambda: ref_class.check_maint_reinst()],
                                  'asdStartEndCheckBox': [lambda: ref_class.check_asd_coords()],
                                  'notMaintPolysCheckBox': [lambda: ref_class.maint_no_poly(), 16],
                                  'notPolysMaintCheckBox': [lambda: ref_class.poly_no_maint()],
                                  'tinyPolysCheckBox': [lambda: ref_class.check_tiny_esus("rd_poly", 1)]}

    def model_navigation(self):
        """
        events handler for buttons in the form
        :return: object
        """
        buttons = self.validation_dia.ui.okCancelButtons.buttons()
        buttons[0].clicked.connect(self.get_data)
        buttons[1].clicked.connect(self.close_browser)
        self.validation_dia.ui.openPushButton.clicked.connect(self.select_file)
        self.validation_dia.ui.screenRadioButton.toggled.connect(lambda: self.selection_handler(0))
        self.validation_dia.ui.fileRadioButton.toggled.connect(lambda: self.selection_handler(1))
        self.validation_dia.ui.notType3CheckBox.toggled.connect(self.check_no_type_click)
        self.validation_dia.ui.startEndCheckBox.toggled.connect(self.check_coords_click)
        self.validation_dia.ui.selectAllButton.clicked.connect(self.select_all)
        self.validation_dia.ui.clearAllButton.clicked.connect(self.clear_all)

    def form_load(self):
        # set the initial status of the form
        self.validation_dia.ui.screenRadioButton.setChecked(True)
        self.validation_dia.ui.filePathLineEdit.setEnabled(False)
        self.check_coords_click()
        self.check_no_type_click()
        self.validation_dia.ui.dupStreetCheckBox.setChecked(True)
        self.validation_dia.ui.notStreetEsuCheckBox.setChecked(True)
        self.validation_dia.ui.notType3CheckBox.setChecked(True)
        self.validation_dia.ui.dupEsuRefCheckBox.setChecked(True)
        self.validation_dia.ui.notEsuStreetCheckBox.setChecked(True)
        self.validation_dia.ui.invCrossRefCheckBox.setChecked(True)
        self.validation_dia.ui.startEndCheckBox.setChecked(False)
        self.validation_dia.ui.tinyEsuCheckBox.setChecked(True)
        if self.params['RNsrwr'].lower() == 'true':
            self.validation_dia.ui.notMaintReinsCheckBox.setChecked(True)
            self.validation_dia.ui.asdStartEndCheckBox.setChecked(True)
        if self.params['RNsrwr'].lower() == 'false':
            self.validation_dia.ui.notMaintReinsCheckBox.setChecked(False)
            self.validation_dia.ui.asdStartEndCheckBox.setChecked(False)
            self.validation_dia.ui.notMaintReinsCheckBox.setEnabled(False)
            self.validation_dia.ui.asdStartEndCheckBox.setEnabled(False)
        if self.params['RNPolyEdit'].lower() == 'true':
            self.validation_dia.ui.notMaintPolysCheckBox.setChecked(True)
            self.validation_dia.ui.notPolysMaintCheckBox.setChecked(True)
            self.validation_dia.ui.tinyPolysCheckBox.setChecked(True)
        if self.params['RNPolyEdit'].lower() == 'false':
            self.validation_dia.ui.notMaintPolysCheckBox.setChecked(False)
            self.validation_dia.ui.notPolysMaintCheckBox.setChecked(False)
            self.validation_dia.ui.tinyPolysCheckBox.setChecked(False)
            self.validation_dia.ui.notMaintPolysCheckBox.setEnabled(False)
            self.validation_dia.ui.notPolysMaintCheckBox.setEnabled(False)
            self.validation_dia.ui.tinyPolysCheckBox.setEnabled(False)

    def close_browser(self):
        # close the dialog
        self.validation_dia.close()

    def get_data(self):
        """
        produce the report according to the options specified by the user
        :return: validation report either on screen or as text file
        """
        if self.validation_dia.ui.fileRadioButton.isChecked():
            # alert the user if no path is specified
            if self.validation_dia.ui.filePathLineEdit.text() == "":
                no_path_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                              "You must specify a path and filename for the report",
                                              QMessageBox.Ok, None)
                no_path_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                no_path_msg_box.exec_()
                return
            # format the path and runs the export
            val_file_path = self.validation_dia.ui.filePathLineEdit.text()
            # checks if the export directory exists and it is valid
            if not os.path.isdir(os.path.dirname(val_file_path)):
                path_invalid_msg_box = QMessageBox(QMessageBox.Warning, " ", "A valid directory must be selected",
                                                   QMessageBox.Ok, None)
                path_invalid_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                path_invalid_msg_box.exec_()
            else:
                self.report_to_file(val_file_path)
            # text file report = false, create a screen report, instantiate the report creator class
        if not self.validation_dia.ui.fileRadioButton.isChecked():
            self.report_to_screen()

    def select_file(self):
        """
        open the dialog window to select the file and print the path on the main line edit
        :return: void
        """
        self.file_dialog.setDirectory(self.home_dir)
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)
        filters = "Text files (*.txt)"
        self.file_dialog.setNameFilter(filters)
        save_file_name = self.file_dialog.getSaveFileName(self.file_dialog, "Export Validation Report",
                                                          self.home_dir,
                                                          filter="Text files (*.txt)")
        if save_file_name != "":
            self.validation_dia.ui.filePathLineEdit.setText(("{}.txt".format(save_file_name)))
        if save_file_name.endswith(".txt"):
            self.validation_dia.ui.filePathLineEdit.setText(save_file_name)

    def selection_handler(self, button_id):
        """
        change the status of the line edit according to the radio button selection
        :return:
        """
        # if screen report is selected disable line edit for the file path
        if button_id == 0:
            self.validation_dia.ui.filePathLineEdit.setEnabled(False)
            self.validation_dia.ui.openPushButton.setEnabled(False)
            self.check_boxes_names = []

        else:
            self.validation_dia.ui.filePathLineEdit.setEnabled(True)
            self.validation_dia.ui.openPushButton.setEnabled(True)
            self.check_boxes_names = []

    def check_coords_click(self):
        # show/hide tolerance metres spin box
        if self.validation_dia.ui.startEndCheckBox.isChecked():
            self.validation_dia.ui.metresSpinBox.setVisible(True)
            self.validation_dia.ui.toleranceLabel.setVisible(True)
        else:
            self.validation_dia.ui.metresSpinBox.setVisible(False)
            self.validation_dia.ui.toleranceLabel.setVisible(False)

    def check_no_type_click(self):
        # enable/disable footpath check box
        if self.validation_dia.ui.notType3CheckBox.isChecked():
            self.validation_dia.ui.incFootPathCheckBox.setEnabled(True)
        else:
            self.validation_dia.ui.notType3CheckBox.setChecked(False)
            self.validation_dia.ui.incFootPathCheckBox.setEnabled(False)

    def select_all(self):
        # reset the form to default status, select all
        self.form_load()

    def clear_all(self):
        # uncheck all checkboxes
        self.validation_dia.ui.dupStreetCheckBox.setChecked(False)
        self.validation_dia.ui.notStreetEsuCheckBox.setChecked(False)
        self.validation_dia.ui.notType3CheckBox.setChecked(False)
        self.validation_dia.ui.incFootPathCheckBox.setChecked(False)
        self.validation_dia.ui.incFootPathCheckBox.setEnabled(False)
        self.validation_dia.ui.dupEsuRefCheckBox.setChecked(False)
        self.validation_dia.ui.notEsuStreetCheckBox.setChecked(False)
        self.validation_dia.ui.invCrossRefCheckBox.setChecked(False)
        self.validation_dia.ui.startEndCheckBox.setChecked(False)
        self.validation_dia.ui.tinyEsuCheckBox.setChecked(False)
        self.validation_dia.ui.notMaintReinsCheckBox.setChecked(False)
        self.validation_dia.ui.asdStartEndCheckBox.setChecked(False)
        self.validation_dia.ui.notMaintPolysCheckBox.setChecked(False)
        self.validation_dia.ui.notPolysMaintCheckBox.setChecked(False)
        self.validation_dia.ui.tinyPolysCheckBox.setChecked(False)

    def report_to_file(self, val_file_path):
        """
        creates a text file report
        :return: void
        """
        # assign to the report class the file path property
        self.report_file_path = val_file_path
        # start writing
        # get all checked check-boxes
        if len(self.list_check_boxes) > 0:
            self.list_check_boxes = []
        self.list_check_boxes = self.validation_dia.findChildren(QCheckBox, self.re)
        if len(self.check_boxes_names) > 0:
            self.check_boxes_names = []
        for check_box in self.list_check_boxes:
            if check_box.isChecked():
                self.check_boxes_names.append(str(check_box.objectName()))
        if len(self.check_boxes_names) < 1:
            no_val_check_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                               "At least one validation option must be selected", QMessageBox.Ok, None)
            no_val_check_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_val_check_msg_box.exec_()
            return
        tolerance = self.validation_dia.ui.metresSpinBox.value()
        if self.validation_dia.ui.startEndCheckBox.isChecked() and (tolerance is None or tolerance == 0):
            no_tol_msg_box_file = QMessageBox(QMessageBox.Warning, " ", "You must specify a tolerance",
                                              QMessageBox.Ok, None)
            no_tol_msg_box_file.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_tol_msg_box_file.exec_()
            return
        self.progress_win.setWindowTitle("Export Validation Report")
        self.progress_win.show()
        if self.validation_dia.ui.notType3CheckBox.isChecked():
            if 'incFootPathCheckBox' in self.check_boxes_names:
                # locate the include footpath option and run just the appropriate function
                self.check_boxes_names.remove('notType3CheckBox')
        self.export_globals = InitGlobals(self.db, self.params, tolerance)
        self.long_task.setMaxThreadCount(1)
        start_report = StartReport(val_file_path, self.org_name)
        start_report.signals.result.connect(self.log_progress)
        end_report = EndReport()
        end_report.signals.result.connect(self.log_progress)
        end_report.signals.report_finished.connect(self.show_finished)
        self.long_task.start(start_report)
        for check_box_name in self.check_boxes_names:
            run_class = self.summary_runnables[check_box_name]
            runnable = run_class[0]()
            runnable.signals.result.connect(self.log_progress)
            self.long_task.start(runnable)
        self.long_task.start(end_report)

        self.list_check_boxes = []
        self.check_boxes_names = []

    @pyqtSlot()
    def show_finished(self):
        self.long_task.waitForDone()
        show_finished_msg_box = QMessageBox(QMessageBox.Information, " ",
                                            "Report successfully exported at \n {0}"
                                            .format(str(self.report_file_path))
                                            .replace("\\\\", "\\"), QMessageBox.Ok, None)
        show_finished_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        show_finished_msg_box.exec_()

    @pyqtSlot(str, int)
    def log_progress(self, task, value):
        self.progress_win.setLabelText(task)
        self.progress_win.setValue(value)

    def report_to_screen(self):
        tolerance = self.validation_dia.ui.metresSpinBox.value()
        if self.validation_dia.ui.startEndCheckBox.isChecked() and (tolerance is None or tolerance == 0):
            no_tol_msg_box_screen = QMessageBox(QMessageBox.Warning, " ", "You must specify a tolerance",
                                                QMessageBox.Ok, None)
            no_tol_msg_box_screen.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_tol_msg_box_screen.exec_()
            return
        report_to_screen = self.report
        report_to_screen.validation_dia = self.validation_dia
        # in case the user selects a screen report immediately after the generation of
        # a file report create a new instance of the report class and None the file path
        # instantiate the report window, the parent is the main validation report dialog
        if self.validation_dk is None:
            self.validation_dk = ValidationSummaryDock(self.validation_dia)
            self.validation_dk.setWindowTitle("Validation Report Summary")
            self.validation_dk.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
            rn_icon = QIcon()
            rn_icon.addPixmap(QPixmap(os.path.join(self.app_root,
                                                         "image",
                                                         "rn_logo_v2.png")))
            self.validation_dk.setWindowIcon(rn_icon)
        # instantiate the class handler (functions to create and format the screen report)
        # include the window in the instantiation
        report_to_dialog = ValidationSummary(self.validation_dk, self.iface, self.db, tolerance)
        # creates a list of the checked checkboxes to create the tables
        self.list_check_boxes = self.validation_dia.findChildren(QCheckBox, self.re)
        for check_box in self.list_check_boxes:
            if check_box.isChecked():
                self.check_boxes_names.append(str(check_box.objectName()))
        # check if at least one checkbox is checked before running the report
        if len(self.check_boxes_names) < 1:
            no_val_check_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                               "At least one validation option must be selected", QMessageBox.Ok, None)
            no_val_check_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_val_check_msg_box.exec_()
            return
        # initialises the functions
        self.init_functions(report_to_screen, tolerance)
        # runs the functions, each function passes a list and a table reference
        # to the handler class methods that create, populate and finally show the window
        if self.validation_dia.ui.notType3CheckBox.isChecked():
            if 'incFootPathCheckBox' in self.check_boxes_names:
                # locate the include footpath option and run just the appropriate function
                self.check_boxes_names.remove('notType3CheckBox')
                report_to_dialog.include_footpath = True
        self.report.start_report()
        for check_box_name in self.check_boxes_names:
            function = self.summary_functions[check_box_name][0]
            # handles multiple results for a unique check box (cross references)
            if check_box_name == 'invCrossRefCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 5)
                report_to_dialog.set_table(function_list[1], 6)
                report_to_dialog.set_table(function_list[2], 7)
            # handles multiple results for a unique check box (tiny/empty ESUs Polys)
            elif check_box_name == 'tinyEsuCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 9)
                report_to_dialog.set_table(function_list[1], 10)
            elif check_box_name == 'tinyPolysCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 19)
                report_to_dialog.set_table(function_list[1], 20)
            # handles multiple results for a unique check box (maint/reins asd streets)
            elif check_box_name == 'notMaintReinsCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 11)
                report_to_dialog.set_table(function_list[1], 12)
            # handles multiple results for a unique check box (maint/reins asd coords)
            elif check_box_name == 'asdStartEndCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 13)
                report_to_dialog.set_table(function_list[1], 14)
                report_to_dialog.set_table(function_list[2], 15)
            # handles multiple results for a unique check box (polygons with no link, multi maintenance assignation)
            elif check_box_name == 'notPolysMaintCheckBox':
                function_list = function()
                report_to_dialog.set_table(function_list[0], 17)
                report_to_dialog.set_table(function_list[1], 18)
            # all other normal cases
            else:
                table_id = self.summary_functions[check_box_name][1]
                report_to_dialog.set_table(function(), table_id)
        self.report.end_report(self.validation_dia)
        self.report = ExportValidationReport("roadNet Validation Report",
                                             self.org_name,
                                             self.db, self.iface, None)
        report_to_dialog.show_validation_widget()
