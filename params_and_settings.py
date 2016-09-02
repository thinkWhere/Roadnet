# -*- coding: utf-8 -*-
"""Contains the ParamsFile class used to manipulate the parameters file."""
import os
import xml.etree.ElementTree as ETree
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox

from roadnet_dialog import SettingsDlg
import roadnet_exceptions as rn_except

__author__ = 'Alessandro, john.stevenson'


class ParamsFileHandler(object):
    """
    Interface to the Params.xml file to allow easy reading and writing and
    passing of information via a dictionary.
    """
    tree = None
    root = None
    xmlfile_path = None

    def __init__(self, file_path):
        """
        Reads file data and structure as tree.  This is retained and used
        when data are written back to file.

        :param file_path: Path of XML file
        """
        self.xmlfile_path = file_path

    def validate_params_file(self):
        """
        Check the Params.xml file and give user-friendly warnings about errors.
        """
        if not os.path.isfile(self.xmlfile_path):
            msg = 'roadNet needs a valid Params.xml file to start.\n\n'
            msg += "Parameters file missing from:\n\n{}".format(
                self.xmlfile_path)
            raise rn_except.MissingParamsFilePopupError(msg)

        # Check all keys are present and valid
        params = self.read_to_dictionary()
        required_keys = ['RNDataStorePath', 'DbName', 'RNPolyEdit', 'RNsrwr',
                         'Language', 'UserName', 'AutoSplitESUs',
                         'PreventOverlappingPolygons', 'RAMP', 'RAMP_output_directory']

        # Stop with error if keys are missing
        missing_keys = []
        for key in required_keys:
            if key not in params.keys():
                missing_keys.append(key)
        if len(missing_keys) > 0:
            msg = 'roadNet needs a valid Params.xml file to start.\n\n'
            msg += ("The following keys are missing from <Params.xml>:\n\n" +
                    '\n'.join(missing_keys))
            raise rn_except.InvalidParamsKeysPopupError(msg)

        # Warn if extra keys are found
        extra_keys = []
        for key in params:
            if key not in required_keys:
                extra_keys.append(key)
        if len(extra_keys) > 0:
            message = ("The following extra keys were found in <Params.xml>:\n\n" +
                       '\n'.join(extra_keys))
            raise rn_except.ExtraParamsKeysPopupError(message)

    def read_to_dictionary(self):
        """
        Return a dictionary containing the contents of the xml file.

        :return params: Dictionary of parameter values.
        """
        self._update_tree()
        params = dict()

        for xml_param in self.root.iter('Parameter'):
            key = xml_param.attrib['name']
            value = xml_param.text
            if value is None:
                # Replace None in empty values with blank strings
                params[key] = ''
            else:
                params[key] = value

        return params

    def update_xml_file(self, input_params):
        """
        Writes a dictionary of parameters to the file to save the values.  Only
        parameters that were in the original Params.xml file are saved.

        :param input_params: Dictionary of parameter values.
        :return:
        """
        self._update_tree()
        for xml_param in self.root.iter('Parameter'):
            key = xml_param.attrib['name']
            xml_param.text = input_params[key]

        with open(self.xmlfile_path, 'w') as outfile:
            self.tree.write(outfile)

    def _update_tree(self):
        """
        Read tree and root information from the file.
        """
        with open(self.xmlfile_path, 'r') as infile:
            self.tree = ETree.parse(infile)
            self.root = self.tree.getroot()

    @staticmethod
    def _show_warning_message_box(message):
        """
        Show a warning message box.
        :param message: Message string
        """
        msg_box = QMessageBox(QMessageBox.Warning, " ", message,
                              QMessageBox.Ok, None)
        msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        msg_box.exec_()


class SettingsDialogHandler(object):
    """
    Creates and holds reference to Settings dialog.  Provides functions to
    read and write params dictionary based on GUI checkboxes.
    """
    def __init__(self, params):
        """
        Create settings dialog instance.
        """
        self.params = params
        self.dlg = SettingsDlg()
        self.check_boxes = {
            'AutoSplitESUs': self.dlg.ui.esuCheckBox,
            'PreventOverlappingPolygons': self.dlg.ui.rdpolyCheckBox,
            'RAMP': self.dlg.ui.rampCheckBox}

    def show_dialog_and_update_params(self):
        """
        Update params dictionary by showing dialog for user to select check
        boxes.
        :return params: dictionary of parameters
        """
        self.set_checkboxes_from_params()

        # Launch dialog to let user change settings
        self.dlg.exec_()
        checkbox_params = self.get_params_from_checkboxes()

        if checkbox_params['RAMP'] != self.params['RAMP']:
            self.show_ramp_settings_changed_warning(checkbox_params)

        # Write updated values to params dictionary
        for key, value in checkbox_params.iteritems():
            self.params[key] = value

        return self.params

    def set_checkboxes_from_params(self):
        """
        Set tick status of checkboxes with values from internal params
        dictionary.
        """
        for box in self.check_boxes:
            if self.params[box].lower() == 'true':
                self.check_boxes[box].setChecked(True)
            elif self.params[box].lower() == 'false':
                self.check_boxes[box].setChecked(False)
            else:
                msg = "{} flag in Params.xml must be 'true' or 'false'".format(
                    box)
                raise ValueError(msg)

    def get_params_from_checkboxes(self):
        """
        Get tick status of checkboxes as a dictionary.
        :return params: dictionary with parameter values
        """
        params = {}
        for box in self.check_boxes:
            if self.check_boxes[box].isChecked():
                params[box] = 'true'
            else:
                params[box] = 'false'
        return params

    @staticmethod
    def show_ramp_settings_changed_warning(checkbox_params):
        """
        Display message box informing user that QGIS restarted needed
        :param checkbox_params: Dictionary with updated checkbox parameters
        """
        if checkbox_params['RAMP'] == 'true':
            ramp_status = 'enabled'
        else:
            ramp_status = 'disabled'
        message = ("RAMP {}.\n\nRestart roadNet "
                   "for changes to take effect.".format(ramp_status))

        # Show message box
        msg_box = QMessageBox(QMessageBox.Information, " ", message,
            QMessageBox.Ok, None)
        msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        msg_box.exec_()


def update_via_dialog(params):
    """
    Update params dictionary by showing dialog for user to select check
    boxes.
    :param params: dictionary of parameters
    :return params: updated dictionary of parameters
    """
    settings_handler = SettingsDialogHandler(params)
    updated_params = settings_handler.show_dialog_and_update_params()
    return updated_params
