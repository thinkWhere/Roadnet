# -*- coding: utf-8 -*-
import os

from PyQt4.QtGui import QFileDialog
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.roadnet_dialog import ExportCompleteDia
from Roadnet.ramp import wdm
from Roadnet import config


class WdmExportHandler(object):
    def __init__(self, db, params, iface):
        """
        Class for coordinating gui during exports to WDM
        :param db: Open QSqlDatabase object
        :param params: Dictionary of roadNet parameters
        :param iface: QGIS iface object
        """
        self.db = db
        self.params = params
        self.iface = iface
        self.output_dir = self.get_valid_output_dir()
        self.complete_dlg = ExportCompleteDia()
        self.complete_dlg.ui.cancelPushButton.clicked.connect(
            self.complete_dlg.close)

    def get_valid_output_dir(self):
        """
        Check validity of output directory stored in params. Get new directory
        if not valid.
        :return: String path to output directory
        """
        # Choose path to start in
        if os.path.isdir(self.params['RAMP_output_directory']):
            initial_dir = self.params['RAMP_output_directory']
        else:
            initial_dir = os.path.expanduser('~')

        # Create and tweak file dialog
        file_dialog = QFileDialog()
        title = "Select export directory (RAMPOUTPUT files will be overwritten)"

        # Show dialog and get new path
        output_dir = QFileDialog.getExistingDirectory(
            file_dialog, caption=title, directory=initial_dir)

        return output_dir

    def export_shapefiles(self):
        """
        Export shapefiles for WDM
        """
        for count, element_type in enumerate(wdm.ELEMENT_CODE_MAP):
            # Do export
            if config.DEBUG_MODE:
                print("DEBUG MODE: Exporting {}".format(element_type))
            try:
                wdm.export(element_type, self.db, self.output_dir)
            except rn_except.CannotOpenShapefilePopupError:
                print("{} failed".format(element_type))

            # Show progress to user in status bar
            msg = "Exporting shapefiles to WDM ({} of {}).".format(
                count, len(wdm.ELEMENT_CODE_MAP) - 1)
            self.iface.mainWindow().statusBar().showMessage(msg)

        # Tell user when export is finished
        self.iface.mainWindow().statusBar().clearMessage()
        self.complete_dlg.exec_()

