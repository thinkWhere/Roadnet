# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Roadnet
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
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import (
    QMessageBox,
    QPixmap,
    QIcon,
    QDesktopServices)
from PyQt4.QtSql import QSqlDatabase
from qgis.utils import *
from qgis.core import *

from esu_selector_tool import EsuSelectorTool
from roadnet_dialog import (
    AdminMetadataDlg,
    ChPwdDlg,
    AboutDlg,
    ExportLsgDlg,
    ExportLsgShapefileDlg,
    ExportPolyDlg,
    ExportsLorDlg,
    ExportsSwrfDlg,
    LsgLookupDlg,
    SrwrLookupDlg,
    StreetBrowserDlg,
    StreetReportsDlg,
    ValidationDlg)
from generic_functions import ipdb_breakpoint
from street_browser.street_browser import StreetBrowser
from exports.exports import (
    ExportDTF,
    ExportSRWR,
    ExportLOR,
    ExportLsgShp,
    ExportPoly)
from admin.admin_menu import ExportStreetReport
from admin.metadata import Metadata
from admin.lsg_lookup import LsgLookUp
from admin.srwr_lookup import SrwrLookup
from admin.validation import Validation
from admin.update_symbology import UpdateSymbology
from gui.toolbar import RoadnetToolbar
from geometry.esu_edit_handler import EsuEditHandler
from geometry.rdpoly_edit_handler import RdpolyEditHandler
from rn_menu.change_pwd import ChangePwd
from rn_menu.about import About
from ramp.ramp import Ramp
import config
import database
import login
import params_and_settings
import roadnet_exceptions as rn_except
import vector_layers

__author__ = 'matthew.walsh'


class Roadnet:
    """
    QGIS plugin for managing street gazetteer data.  thinkWhere 2015.
    """
    def __init__(self, iface):
        """
        Connect the plugin to the QGIS interface.  This code is run every time
        that QGIS boots.

        :param iface: QGIS interface
        :return:
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Roadnet.__init__ called')
        self.iface = iface  # Save reference to the QGIS interface
        self.canvas = self.iface.mapCanvas()
        self.plugin_dir = os.path.dirname(__file__)
        self.clean_rdpoly = None
        self.db = None
        self.esu = None
        self.model = None
        self.rdpoly = None
        self.roadnet_started = False
        self.selector_tool = None
        self.street_browser = None
        self.street_browser_dk = None
        self.toolbar = None

        # Setup params file
        params_file_path = os.path.join(self.plugin_dir, 'Params.xml')
        self.params_file_handler = params_and_settings.ParamsFileHandler(params_file_path)
        try:
            self.params_file_handler.validate_params_file()
        except rn_except.QMessageBoxWarningError:  # Parent of two different Params errors
            return
        self.params = self.params_file_handler.read_to_dictionary()

        # Connect to Ramp
        self.ramp = Ramp(self)

    def initGui(self):
        """
        Set up the GUI components.  This code is only run when the plugin has
        been activated in the plugin manager.

        :return:
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: initGui called')
        self.init_toolbar()
        self.toolbar.set_state('init')

    def start_roadnet(self):
        """
        Start the plugin.  Log in the user, connect to database, load layers,
        set toolbar up appropriately.
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Starting roadNet')

        # Check the database
        if (self.params['RNDataStorePath'] == '') or (self.params['DbName'] == ''):
            if not self.run_change_db_path():
                return
        db_path = os.path.join(self.params['RNDataStorePath'],
                               self.params['DbName'])
        try:
            database.check_file(db_path)
        except IOError:
            if not self.run_change_db_path():
                return
        # Log the user in
        login.login_and_get_role(self.params)
        self.toolbar.set_state(self.params['role'])
        if self.params['role'] == 'init':
            return
        # Open database and model
        self.db = database.open_working_copy(self.params)  # params knows role
        database.update_geometry_statistics(self.db)
        self.model = database.get_model(self.db)
        # Add layers + connect edit signals, zoom to rdpoly
        self.add_rdpoly_layer()  # Layer added as self.rdpoly
        self.add_esu_layer()  # Layer added as self.esu + selector tool init
        self.params['session_includes_edits'] = False
        # Create the street browser instance
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Initialising street browser')
        self.street_browser_dk = StreetBrowserDlg(self.params)
        self.street_browser_dk.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        rn_icon = QIcon()
        rn_icon.addPixmap(QPixmap(os.path.join(self.plugin_dir, "image", "rn_logo_v2.png")))
        self.street_browser_dk.setWindowIcon(rn_icon)
        self.street_browser = StreetBrowser(self.iface, self.street_browser_dk, self.model, self.db, self.params)
        self.disable_srwr()  # Hide SRWR tab
        self.street_browser.set_buttons_initial_state(self.params['role'])
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Initialising street selector tool')
        # Initialise selector tool
        self.selector_tool = EsuSelectorTool(self.street_browser_dk,
                                             self.iface,
                                             self.esu,
                                             self.toolbar,
                                             self.db,
                                             self.street_browser.mapper)
        # Start RAMP
        if self.params['RAMP'] == 'true':
            self.ramp.start_ramp()
        self.roadnet_started = True

    def stop_roadnet(self):
        """
        Stop the plugin.  Close windows, disconnect and save databases, reset
        toolbars to initial state.
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Stopping roadNet')

        # Stop RAMP, then reinitialise
        if self.ramp.ramp_started:
            self.ramp.stop_ramp()
            self.ramp = Ramp(self)

        # Unset the street selector and reset toolbar
        if self.iface.mapCanvas().mapTool():  # Tool is None if roadNet just stopped
            current_tool = self.iface.mapCanvas().mapTool().toolName()
            if current_tool == "ESU SELECTOR":
                self.selector_tool.unset_map_tool()

        # Reinitialise toolbar to reflect changes in RAMP settings
        self.toolbar.toolbar = None  # Delete previous toolbar instance
        self.init_toolbar()

        # Remove layers
        for vlayer in [self.esu, self.rdpoly]:
            vlayer.layerDeleted.disconnect()  # Disconnect auto-reload signal
            try:
                vector_layers.remove_spatialite_layer(vlayer, self.iface)
            except rn_except.RemoveNonExistentLayerPopupError:
                pass
        self.esu = None
        self.rdpoly = None

        # Reset street browser and other components
        self.street_browser_dk.close()
        self.street_browser_dk = None
        self.street_browser = None
        self.model = None

        # Disconnect database, and save if necessary
        connection_name = self.db.connectionName()
        self.db.close()
        self.db = None
        QSqlDatabase.removeDatabase(connection_name)
        if not config.DEBUG_MODE:
            database.update_sqlite_files(self.params)

        # Update params file
        self.params_file_handler.update_xml_file(self.params)

        self.roadnet_started = False

    def tr(self, message):
        return QCoreApplication.translate('Roadnet', message)

    def init_toolbar(self):
        # toolbar init
        if self.params['RAMP'] == 'true':
            with_ramp_flag = True
        else:
            with_ramp_flag = False
        self.toolbar = RoadnetToolbar(self.iface, self.plugin_dir, with_ramp_flag)

        # Roadnet tools
        self.toolbar.start_rn.triggered.connect(lambda: self.start_roadnet())
        self.toolbar.stop_rn.triggered.connect(lambda: self.stop_roadnet())
        self.toolbar.street_sel_btn.triggered.connect(self.activate_esu_selector)
        self.toolbar.sb_btn.triggered.connect(self.run_sb)
        self.toolbar.change_db_path.triggered.connect(self.run_change_db_path)
        self.toolbar.create_restore.triggered.connect(self.run_db_restore_point)
        self.toolbar.change_pwd.triggered.connect(self.run_change_pwd)
        self.toolbar.about.triggered.connect(self.run_about)
        self.toolbar.settings.triggered.connect(self.run_settings)
        # help menu
        self.toolbar.help.triggered.connect(self.run_help)
        # export menu
        self.toolbar.exp_lgs.triggered.connect(self.run_lsg_exp)
        self.toolbar.exp_srwr.triggered.connect(self.run_srwr_exp)
        self.toolbar.exp_list_roads.triggered.connect(self.run_lor_exp)
        self.toolbar.exp_maintain_poly.triggered.connect(self.run_export_poly)
        self.toolbar.exp_lsg_shp.triggered.connect(self.run_export_esu)
        # Admin tools
        self.toolbar.street_rpt.triggered.connect(self.run_street_report)
        self.toolbar.meta_menu.triggered.connect(self.run_metadata)
        self.toolbar.edit_lsg_lu.triggered.connect(self.run_lsg_lookup)
        self.toolbar.edit_srwr_lu.triggered.connect(self.run_srwr_lookup)
        self.toolbar.validation_rpt.triggered.connect(self.run_validation)
        self.toolbar.clean_rdpoly.triggered.connect(self.run_clean_rdpoly_symbology)
        # RAMP items
        if self.params['RAMP'] == 'true':
            self.toolbar.mcl_auto_number_btn.triggered.connect(self.ramp.run_mcl_auto_number)
            self.toolbar.mcl_select_btn.triggered.connect(self.ramp.run_ramp_mcl_select)
            self.toolbar.rdpoly_select_btn.triggered.connect(self.ramp.run_ramp_rdpoly_select)
            self.toolbar.load_layers.triggered.connect(self.ramp.run_ramp_load_layers)
            self.toolbar.road_length.triggered.connect(self.ramp.run_ramp_road_length)
            self.toolbar.export_wdm.triggered.connect(self.ramp.run_ramp_export_wdm)

    def activate_esu_selector(self):
        """
        Fire on esu selector button. Sets reference to ESU Graphic layer and
        activates the street selector tool.
        """
        self.iface.setActiveLayer(self.esu)
        self.iface.mapCanvas().setMapTool(self.selector_tool)

    def unload(self):
        """
        Removes the plugin menu item and sb_icon from QGIS GUI
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: unload called')
            lock_file = os.path.join(self.params['RNDataStorePath'], 'RNLock')
            if os.path.isfile(lock_file):
                os.remove(lock_file)
        if self.roadnet_started:
            self.stop_roadnet()
        if self.toolbar:  # No toolbar exists if Params file was missing
            self.toolbar.toolbar = None

    def run_db_restore_point(self):
        """
        Saves a copy of the working database as <database>_restore.sqlite.
        :return: void
        """
        database.db_restore_point(self.params)

    def run_change_db_path(self):
        """
        function that shows the db path change dialog window
        :return: [bool] True if the user clicks on OK, False if on Cancel
        """
        return database.change_db_path(self.params, self.params_file_handler)

    def run_change_pwd(self):
        """
        function that changes the access password for the current user
        :return:
        """
        self.change_pwd_dlg = ChPwdDlg()
        change_pwd = ChangePwd(self.change_pwd_dlg,
                               self.iface,
                               self.db,
                               self.plugin_dir,
                               self.params)
        self.change_pwd_dlg.exec_()
        del change_pwd

    def run_about(self):
        """
        function that shows the about window with information
        on plug-in version copyright and licensing
        """
        about_dlg = AboutDlg()
        about_dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        about = About(about_dlg, self.plugin_dir)
        about_dlg.exec_()
        del about

    def run_sb(self):
        """
        Shows the street browser dialog window, if its already visible then raise to front and give focus.
        """
        self.street_browser_dk.signals.closed_sb.connect(self.street_browser.remove_coords)
        if self.street_browser_dk.isVisible():
            self.street_browser_dk.activateWindow()
            if self.street_browser_dk.isMinimized():
                self.street_browser_dk.showNormal()
        else:
            self.street_browser_dk.show()

    def run_lsg_exp(self):
        """
        function that shows the export LSG dialog window
        """
        self.export_lsg_dk = ExportLsgDlg()
        self.export_lsg = ExportDTF(self.iface, self.export_lsg_dk, self.params, self.db)
        self.export_lsg_dk.exec_()

    def run_srwr_exp(self):
        """
        function that shows the export SRWR dialog window
        """
        self.export_swrf_dk = ExportsSwrfDlg()
        self.export_srwr = ExportSRWR(self.iface, self.export_swrf_dk, self.params, self.db)
        self.export_swrf_dk.exec_()

    def run_lor_exp(self):
        """
        function that shows the export list of roads dialog window
        """
        self.export_lor_dk = ExportsLorDlg()
        self.export_lor = ExportLOR(self.iface, self.export_lor_dk, self.db)
        self.export_lor_dk.exec_()

    def run_export_esu(self):
        """
        function that exports ESU streets line layer
        """
        self.iface.setActiveLayer(self.esu)
        self.export_lsg_shp_dk = ExportLsgShapefileDlg()
        self.export_lsg_shp = ExportLsgShp(self.iface, self.export_lsg_shp_dk, self.db, self.params)
        self.export_lsg_shp_dk.exec_()

    def run_export_poly(self):
        """
        function that exports polygons layer
        :return:
        """
        self.iface.setActiveLayer(self.rdpoly)
        self.export_polgons_dk = ExportPolyDlg()
        self.export_poly = ExportPoly(self.iface, self.export_polgons_dk, self.db)
        self.export_polgons_dk.exec_()

    def run_street_report(self):
        """
        function that shows the run street report dialog window
        """
        self.street_reports_dlg = StreetReportsDlg()
        self.export_street_reports = ExportStreetReport(
            self.iface, self.db, self.street_reports_dlg, self.params)
        self.street_reports_dlg.exec_()

    def run_metadata(self):
        """
        Initialise and display the metadata information window
        :return:
        """
        # Initialise metadata each time dialog is launched
        self.admin_metadata_dlg = AdminMetadataDlg()
        self.metadata = Metadata(self.iface, self.db, self.admin_metadata_dlg,
                                 self.params)
        self.admin_metadata_dlg.show()

    def run_lsg_lookup(self):
        """
        Open the LSG lookup definition dialog window
        :return:
        """
        self.lsg_lookup_dlg = LsgLookupDlg()
        self.lsg_lookup = LsgLookUp(self.iface, self.db, self.lsg_lookup_dlg)
        self.lsg_lookup_dlg.show()

    def run_srwr_lookup(self):
        """
        Open the SRWR lookup definition dialog window
        """
        self.srwr_lookup_dlg = SrwrLookupDlg()
        self.srwr_lookup = SrwrLookup(self.iface, self.db, self.srwr_lookup_dlg)
        self.srwr_lookup_dlg.exec_()

    def run_validation(self):
        """
        function that runs the validation report window
        :return:
        """
        self.validation_dlg = ValidationDlg()
        self.validation = Validation(self.iface, self.db, self.validation_dlg,
                                     self.plugin_dir, self.params)
        self.validation_dlg.exec_()

    def run_clean_rdpoly_symbology(self):
        """
        Run the road polygon symbology cleanup tool.
        :return:
        """
        self.clean_rdpoly = UpdateSymbology(self.db, self.rdpoly, self.esu)
        self.clean_rdpoly.show_symbology_dlg()

    def run_help(self):
        """
        Open the help pdf in the default web browser
        """
        help = QDesktopServices()
        help_url = QUrl("http://www.thinkwhere.com/index.php/download_file/240/")
        if not help.openUrl(help_url):
            no_browser_msg_box = QMessageBox(QMessageBox.Warning, " ", "roadNet cannot find a web browser "
                                                                       "to open the help page", QMessageBox.Ok, None)
            no_browser_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_browser_msg_box.exec_()
            return

    def run_settings(self):
        """
        Show the settings dialog
        """
        updated_params = params_and_settings.update_via_dialog(self.params)
        self.params_file_handler.update_xml_file(updated_params)

    def disable_srwr(self):
        """
        Initially make the SRWR tab invisible.
        """
        self.street_browser_dk.ui.srwrRecordsGroupBox.setVisible(False)

    def add_rdpoly_layer(self):
        """
        Load Road Polygon layer from spatialite file.  Connect triggers for
        editing, and so they can reload themselves if removed.
        """
        if config.DEBUG_MODE:
            print("DEBUG_MODE: Adding Road Polygon layer.")
        self.rdpoly = vector_layers.add_styled_spatialite_layer(
            'rdpoly', 'Road Polygons', self.params['working_db_path'], self.iface,
            style='rdpoly')
        self.rdpoly.editingStarted.connect(self.editing_rdpoly_begin)
        self.rdpoly.editingStopped.connect(self.editing_rdpoly_end)
        self.rdpoly.layerDeleted.connect(self.add_rdpoly_layer)

    def add_esu_layer(self):
        """
        Load ESU layer from spatialite file.  Connect triggers for editing, and
        so they can reload themselves if removed.
        """
        if config.DEBUG_MODE:
            print("DEBUG_MODE: Adding ESU layer.")
        self.esu = vector_layers.add_styled_spatialite_layer(
            'esu', 'ESU Graphic', self.params['working_db_path'], self.iface,
            style='esu')
        self.esu.editingStarted.connect(self.editing_esu_begin)
        self.esu.editingStopped.connect(self.editing_esu_end)
        self.esu.layerDeleted.connect(self.add_esu_layer)  # Reload if removed
        # Create the selector tool instance
        if self.roadnet_started:
            if config.DEBUG_MODE:
                print('DEBUG_MODE: Re-initialising street selector tool')
            # Recreate selector tool
            self.selector_tool = EsuSelectorTool(self.street_browser_dk,
                                                 self.iface,
                                                 self.esu,
                                                 self.toolbar,
                                                 self.db,
                                                 self.street_browser.mapper)

    def editing_esu_begin(self):
        """
        Creates classes that listen for various edit events on the Esu layer
        """
        if self.params['AutoSplitESUs'] == 'true':
            handle_intersect_flag = True
        else:
            handle_intersect_flag = False

        # Disable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        self.esu_edit_handler = EsuEditHandler(
            self.iface, self.esu, self.db, self.params, handle_intersect_flag)

    def editing_esu_end(self):
        self.esu_edit_handler = None
        self.params['session_includes_edits'] = True
        # Re-enable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if self.esu.isEditable() is True:
            # Rolling back changes ends destroys geometry_handler class but
            # layer remains editable.  In this case, recreate it.
            self.editing_esu_begin()

    def editing_rdpoly_begin(self):
        if self.params['PreventOverlappingPolygons'] == 'true':
            handle_intersect_flag = True
        else:
            handle_intersect_flag = False

        # Disable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        self.rdpoly_edit_handler = RdpolyEditHandler(
            self.iface, self.rdpoly, self.db, self.params, handle_intersect_flag)

    def editing_rdpoly_end(self):
        self.rdpoly_edit_handler = None
        self.params['session_includes_edits'] = True
        # Re-enable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if self.rdpoly.isEditable() is True:
            # Rolling back changes ends destroys geometry_handler class but
            # layer remains editable.  In this case, recreate it.
            self.editing_rdpoly_begin()

    def get_multiple_part_esus(self):
        """
        Helper function, not used in roadNet, that can be called manually
        to list ESUs whose geometries have more than one part.
        :return: list of esu ids
        """
        esu_ids = []
        for f in self.esu.getFeatures():
            g = QgsGeometry(f.geometry())  # Make a copy
            if g.deletePart(1):
                esu_ids.append(f['esu_id'])
        return esu_ids

