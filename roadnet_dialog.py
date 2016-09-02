# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RoadnetDialog
                                 A QGIS plugin
 Roadnet is a plugin used for maintaining a local street gazetteer.
                             -------------------
        begin                : 2014-12-09
        git sha              : $Format:%H$
        copyright            : (C) 2014 by thinkWhere
        email                : support@thinkwhere.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtGui, QtCore


from Roadnet.gui.rn_street_browser_ui import Ui_streetBrowserDialog
from Roadnet.gui.rn_filter_street_record_ui import Ui_filterStreetRecordDialog
from Roadnet.gui.rn_quick_find_ui import Ui_quickFindDialog
from Roadnet.gui.rn_save_record_ui import Ui_AddRecordDialog
from Roadnet.gui.rn_edit_coords_ui import Ui_editCoordsDialog
from Roadnet.gui.rn_edit_esu_link_ui import Ui_editEsuLinkDialog
from Roadnet.gui.rn_export_lsg_ui import Ui_exportLsgDialog
from Roadnet.gui.rn_export_swrf_ui import Ui_exportSWRF
from Roadnet.gui.rn_export_lor_ui import Ui_exportLorDialog
from Roadnet.gui.rn_street_selector_ui import Ui_streetSelectorDialog
from Roadnet.gui.rn_export_sf_ui import Ui_selectedFeatures
from Roadnet.gui.rn_export_lsg_shp_ui import Ui_exportLsgShpDialog
from Roadnet.gui.rn_export_poly_shp_ui import Ui_exportPolyShpDialog
from Roadnet.gui.rn_export_complete_ui import Ui_exportComplete
from Roadnet.gui.rn_admin_street_reports_ui import Ui_streetreports
from Roadnet.gui.rn_admin_street_reports_alert_ui import Ui_strtAdminAlert
from Roadnet.gui.rn_admin_metadata_ui import Ui_metadataDialog
from Roadnet.gui.rn_export_exporting import Ui_exporteExporting
from Roadnet.gui.rn_admin_lsg_lookup_ui import Ui_lsgLookupDialog
from Roadnet.gui.rn_admin_srwr_lookup_ui import Ui_srwrLookupDialog
from Roadnet.gui.rn_admin_validation_ui import Ui_validationDialog
from Roadnet.gui.rn_srwr_maint_ui import Ui_srwrMaintDialog
from Roadnet.gui.rn_srwr_spec_des_ui import Ui_srwrSpecDesDialog
from Roadnet.gui.rn_srwr_reins_cat_ui import Ui_srwrReinsCatDialog
from Roadnet.gui.rn_admin_validation_summary import Ui_validationSummaryDialog
from Roadnet.gui.rn_login_ui import Ui_loginDialog
from Roadnet.gui.rn_db_path_ui import Ui_newDbPathDialog
from Roadnet.gui.rn_password_ui import Ui_chPasswordDlg
from Roadnet.gui.rn_about_ui import Ui_aboutDialog
from Roadnet.gui.rn_settings_ui import Ui_settingsDialog
from Roadnet.gui.rn_symbology_ui import Ui_symbologyDialog
from Roadnet.ramp.gui.ramp_length_of_roads_ui import Ui_RampLengthOfRoadsDialog
from Roadnet.ramp.gui.ramp_mcl_editor_ui import Ui_MclEditorDialog
from Roadnet.ramp.gui.ramp_rdpoly_editor_ui import Ui_RdpolyEditorDialog
from Roadnet.ramp.gui.ramp_edit_linked_polys_ui import Ui_editLinkedPolysDialog
from Roadnet.ramp.gui.ramp_mcl_auto_numbering_ui import Ui_mclAutoNumberingDialog


class StreetBrowserDlg(QtGui.QDialog, Ui_streetBrowserDialog):
    """
    Main street browsers dialog widget.
    """
    def __init__(self, params):
        """
        :param params: Params dictionary
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_streetBrowserDialog()
        self.ui.setupUi(self)
        self.params = params
        self.srwr = None
        self.street_browser = None
        self.signals = StreetBrowserSignals()

    def closeEvent(self, event):
        """
        Only close the street browser if it is not in modify/add record state. This stops the user from closing the
        dialog from the Windows preview thumbnail.
        :param event: QEvent
        """
        # checks if the sb is in editing mode
        if self.ui.addPushButton.text() == 'Complete' or self.ui.modifyPushButton.text() == 'Complete':
            event.ignore()
        else:
            event.accept()
            self.signals.closed_sb.emit()

    def changeEvent(self, event):
        """
        Detects a maximise event from the street browser dialog and shows
        by deafult the SRWR group box
        :param event: QEvent the event fired up by the user
        :return: void
        """
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMaximized:
                self.ui.srwrRecordsGroupBox.setVisible(True)
                self.ui.srwrPushButton.setText("Hide SRWR Details")
        QtGui.QWidget.changeEvent(self, event)


class StreetBrowserSignals(QtCore.QObject):
    """class holding signals for the street browser window"""
    closed_sb = QtCore.pyqtSignal()


class FilterStreetRecordsDlg(QtGui.QDialog, Ui_filterStreetRecordDialog):
    # Filter street record dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_filterStreetRecordDialog()
        self.ui.setupUi(self)


class QuickFindDlg(QtGui.QDialog, Ui_quickFindDialog):
    # Quick find record dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_quickFindDialog()
        self.ui.setupUi(self)


class SaveRecordDlg(QtGui.QDialog, Ui_AddRecordDialog):
    # Confirm save record dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AddRecordDialog()
        self.ui.setupUi(self)


class EditCoordsDlg(QtGui.QDialog, Ui_editCoordsDialog):
    # Edit start/end coords dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_editCoordsDialog()
        self.ui.setupUi(self)


class EditEsuLinkDlg(QtGui.QDialog, Ui_editEsuLinkDialog):
    # Edit ESU/Street links dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_editEsuLinkDialog()
        self.ui.setupUi(self)


class ExportLsgDlg(QtGui.QDialog, Ui_exportLsgDialog):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportLsgDialog()
        self.ui.setupUi(self)


class ExportsSwrfDlg(QtGui.QDialog, Ui_exportLsgDialog):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportSWRF()
        self.ui.setupUi(self)


class ExportsLorDlg(QtGui.QDialog, Ui_exportLsgDialog):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportLorDialog()
        self.ui.setupUi(self)


class ExportLsgShapefileDlg(QtGui.QDialog, Ui_exportLsgShpDialog):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportLsgShpDialog()
        self.ui.setupUi(self)


class ExportPolyDlg(QtGui.QDialog, Ui_exportPolyShpDialog):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportPolyShpDialog()
        self.ui.setupUi(self)


class ExportSelectedFeatures(QtGui.QDialog, Ui_selectedFeatures):
    # Export LSG dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_selectedFeatures()
        self.ui.setupUi(self)


class ExportCompleteDia(QtGui.QDialog, Ui_exportComplete):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exportComplete()
        self.ui.setupUi(self)


class ExportExporting(QtGui.QDialog, Ui_exporteExporting):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_exporteExporting()
        self.ui.setupUi(self)


class StreetSelectorDlg(QtGui.QDialog, Ui_streetSelectorDialog):
    # Street Selector Dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_streetSelectorDialog()
        self.ui.setupUi(self)


class StreetReportsAlert(QtGui.QDialog, Ui_strtAdminAlert):
    # Street Selector Dialog
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_strtAdminAlert()
        self.ui.setupUi(self)


class StreetReportsDlg(QtGui.QDialog, Ui_streetreports):
    # Street Reports Dialog Admin
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_streetreports()
        self.ui.setupUi(self)


class AdminMetadataDlg(QtGui.QDialog, Ui_metadataDialog):
    # Street Reports Dialog Admin
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_metadataDialog()
        self.ui.setupUi(self)


class LsgLookupDlg(QtGui.QDialog, Ui_lsgLookupDialog):
    # LSG lookup dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_lsgLookupDialog()
        self.ui.setupUi(self)


class SrwrLookupDlg(QtGui.QDialog, Ui_srwrLookupDialog):
    # SRWR lookup dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_srwrLookupDialog()
        self.ui.setupUi(self)


class ValidationDlg(QtGui.QDialog, Ui_validationDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_validationDialog()
        self.ui.setupUi(self)


class SrwrMaintDlg(QtGui.QDialog, Ui_srwrMaintDialog):
    # SRWR maintenance dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_srwrMaintDialog()
        self.ui.setupUi(self)


class SrwrSpecialDesDlg(QtGui.QDialog, Ui_srwrSpecDesDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_srwrSpecDesDialog()
        self.ui.setupUi(self)


class SrwrReinsCatDlg(QtGui.QDialog, Ui_srwrReinsCatDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_srwrReinsCatDialog()
        self.ui.setupUi(self)


class ValidationSummaryDock(QtGui.QDialog, Ui_validationSummaryDialog):
    # validation to screen summary window
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_validationSummaryDialog()
        self.ui.setupUi(self)


class LoginDlg(QtGui.QDialog, Ui_loginDialog):
    # login dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_loginDialog()
        self.ui.setupUi(self)


class DbPathDlg(QtGui.QDialog, Ui_newDbPathDialog):
    # change db path dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_newDbPathDialog()
        self.ui.setupUi(self)


class ChPwdDlg(QtGui.QDialog, Ui_chPasswordDlg):
    # change password dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_chPasswordDlg()
        self.ui.setupUi(self)


class AboutDlg(QtGui.QDialog, Ui_aboutDialog):
    # about dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self)


class SettingsDlg(QtGui.QDialog, Ui_settingsDialog):
    # Settings dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)


class RampLengthOfRoadsDlg(QtGui.QDialog, Ui_RampLengthOfRoadsDialog):
    # Ramp length of roads
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_RampLengthOfRoadsDialog()
        self.ui.setupUi(self)


class RampMclEditorDlg(QtGui.QDialog, Ui_MclEditorDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_MclEditorDialog()
        self.ui.setupUi(self)


class RampRdpolyEditorDlg(QtGui.QDialog, Ui_RdpolyEditorDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_RdpolyEditorDialog()
        self.ui.setupUi(self)


class RampEditLinkedPolysDlg(QtGui.QDialog, Ui_editLinkedPolysDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_editLinkedPolysDialog()
        self.ui.setupUi(self)


class RampMclAutoNumberingDlg(QtGui.QDialog, Ui_mclAutoNumberingDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_mclAutoNumberingDialog()
        self.ui.setupUi(self)


class SymbologyDlg(QtGui.QDialog, Ui_symbologyDialog):
    # Symbology dialog window
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_symbologyDialog()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        """
        Only close the symbology update dialog if the task is not running.
        :param event: QEvent
        """
        # The run button is disabled during the running of the threaded process
        if self.ui.runPushButton.isEnabled():
            event.accept()
        else:
            event.ignore()
