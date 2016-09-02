# -*- coding: utf-8 -*-
import datetime as dt
import os

from PyQt4.QtGui import QFileDialog
import Roadnet.roadnet_exceptions as rn_except
from Roadnet.roadnet_dialog import RampLengthOfRoadsDlg
from Roadnet.ramp import length_of_roads as lor
from Roadnet import config


class LengthOfRoadsExportHandler(object):
    output_dir = None

    def __init__(self, db, params, iface):
        """
        Class for coordinating calculation of Length of Roads and associated GUI
        functions.
        :param db: Open QSqlDatabase object
        :param params: Dictionary of roadNet parameters
        :param iface: QGIS iface object
        """
        self.db = db
        self.params = params
        self.iface = iface
        self.dlg = RampLengthOfRoadsDlg()
        self.textbox = self.dlg.ui.plainTextEdit

    def export_length_of_roads(self):
        """
        Calculate road length, then show GUI with results to user.
        """
        # Calculate road length
        try:
            try:
                lor_text = self.get_length_of_roads_text()
            except rn_except.BadSpatialiteVersionError, e:
                raise rn_except.BadSpatialiteVersionPopupError(e.args[0])
        # this section allows development to continue on 14.04
        # Remove final try-except block before production
        except rn_except.BadSpatialiteVersionPopupError, e:
            lor_text = e.args[0]

        # Add header and footer to text
        header_text = "# RAMP  -  Length of Roads Report  -  Created {}\n\n".format(
            dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        lor_text = header_text + lor_text + '\n'
        if config.DEBUG_MODE:
            print("DEBUG MODE: lor_text =\n{}".format(lor_text))

        # Show gui window with results
        self.textbox.setPlainText(lor_text)
        save_result = self.dlg.exec_()  # Dialog returns 1 or 0 on close
        if save_result:
            # Get updated text with any user edits
            lor_text = self.textbox.toPlainText()
            # Open dialog and save file
            self.save_to_file_and_update_output_dir(lor_text)

    def get_length_of_roads_text(self):
        """
        Call length_of_roads function to prepare text string.  Inform user and
        catch errors
        :return: str length_of_roads_text
        """
        # Show progress to user in status bar
        msg = "Calculating RAMP Length of roads"
        self.iface.mainWindow().statusBar().showMessage(msg)

        # Calculate length of roads
        lor_text = lor.get_length_of_roads_text(self.db)

        # Clear status bar
        self.iface.mainWindow().statusBar().clearMessage()

        return lor_text

    def save_to_file_and_update_output_dir(self, text):
        """
        Save text string to file, opening dialog for user.
        :param text: str Text to save to file
        """
        file_path = self.get_valid_file_path()

        if file_path:  # file_path = '' if user cancels
            with open(file_path, 'w') as f:
                f.write(text)
            self.output_dir = os.path.dirname(file_path)

    def get_valid_file_path(self):
        """
        Check validity of output path stored in params. Get new path
        if not valid.
        :return: str path for file
        """
        # Choose path to start in
        try:
            if os.path.isdir(self.params['RAMP_output_directory']):
                initial_dir = self.params['RAMP_output_directory']
            else:
                initial_dir = os.path.expanduser('~')
        except TypeError:
            initial_dir = os.path.expanduser('~')

        # Show dialog
        title = "Save RAMP Length of Road report"
        filename_filter = ("Text or CSV files (*.txt *.csv);;Text files (*.txt)"
                           ";;CSV files (*.csv);;All files (*)")
        file_path = QFileDialog.getSaveFileName(
            None, caption=title, directory=initial_dir, filter=filename_filter)

        # Add .txt if suffix not specified
        if file_path:
            if "." not in file_path:
                file_path += ".txt"

        return file_path
