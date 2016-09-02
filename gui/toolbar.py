# -*- coding: utf-8 -*-
import os.path

from PyQt4.QtCore import QSize, SIGNAL
from PyQt4.QtGui import QMenuBar, QIcon, QAction, QToolTip, QCursor

__author__ = 'matthew.walsh'


class RoadnetToolbar(object):
    """
    Toolbar for roadnet
    """
    sb_btn = None
    street_sel_btn = None
    sb_icon = None
    ss_off_icon = None
    ss_on_icon = None

    rn_menu = None
    exp_menu = None
    admin_menu = None
    ramp_menu = None

    mcl_auto_number_btn = None
    mcl_auto_number_on_icon = None
    mcl_auto_number_off_icon = None
    mcl_select_btn = None
    mcl_select_on_icon = None
    mcl_select_off_icon = None
    rdpoly_select_btn = None
    rdpoly_select_on_icon = None
    rdpoly_select_off_icon = None

    start_rn = None
    stop_rn = None
    change_db_path = None
    settings = None
    create_restore = None
    change_pwd = None
    help = None
    exp_lgs = None
    exp_srwr = None
    exp_lsg_shp = None
    exp_maintain_poly = None
    exp_list_roads = None
    meta_menu = None
    edit_lsg_lu = None
    edit_srwr_lu = None
    validation_rpt = None
    street_rpt = None
    clean_rdpoly = None

    load_layers = None
    road_length = None
    export_wdm = None
    ramp_validation = None
    about = None

    def __init__(self, iface, plugin_dir, with_ramp):
        """
        Initial setup of toolbar (pre-login)
        """
        self.iface = iface
        self.plugin_dir = plugin_dir
        self.with_ramp = with_ramp
        self.canvas = self.iface.mapCanvas()
        # Create toolbar
        self.toolbar = self.iface.addToolBar(u'Roadnet')
        self.toolbar.setObjectName(u'Roadnet')

        # Create menubar
        self.menubar = QMenuBar()
        self.define_button_icons_and_actions()
        self.populate_menubar()

        # Add menubar to toolbar
        self.toolbar.addWidget(self.menubar)
        self.toolbar.setIconSize(QSize(100, 100))

        # Set initial state
        self.set_state('init')

    def define_button_icons_and_actions(self):
        # Top level buttons
        # Street Browser button
        self.sb_icon = QIcon(os.path.join(self.plugin_dir, "image", "sb_icon.png"))
        self.sb_btn = QAction(self.sb_icon, "w", self.iface.mainWindow())
        self.sb_btn.setToolTip("Street Browser")
        self.sb_btn.hovered.connect(lambda: self._actionHovered(self.sb_btn))
        # Street selector button
        self.ss_off_icon = QIcon(
                os.path.join(self.plugin_dir, "image", "ss_off_icon.png"))
        self.ss_on_icon = QIcon(
                os.path.join(self.plugin_dir, "image", "ss_on_icon.png"))
        self.street_sel_btn = QAction(self.ss_off_icon, "OFF", self.menubar)
        self.street_sel_btn.setToolTip("Street Selector")
        self.street_sel_btn.hovered.connect(lambda: self._actionHovered(self.street_sel_btn))

        # Setup RAMP buttons if required
        if self.with_ramp:
            self.define_ramp_button_icons_and_actions()

    def define_ramp_button_icons_and_actions(self):
        # Select MCL section button
        self.mcl_select_on_icon = QIcon(os.path.join(self.plugin_dir,
                                                     "image", "edit_mcl_on_icon.png"))
        self.mcl_select_off_icon = QIcon(os.path.join(self.plugin_dir,
                                                      "image", "edit_mcl_off_icon.png"))
        self.mcl_select_btn = QAction(self.mcl_select_off_icon, "",
                                      self.iface.mainWindow())
        self.mcl_select_btn.setToolTip("Select MCL section")
        self.mcl_select_btn.hovered.connect(
            lambda: self._actionHovered(self.mcl_select_btn))

        # MCL auto numbering tool button
        self.mcl_auto_number_on_icon = QIcon(os.path.join(self.plugin_dir,
                                                          "image", "number_mcls_on_icon.png"))
        self.mcl_auto_number_off_icon = QIcon(os.path.join(self.plugin_dir,
                                                           "image", "number_mcls_off_icon.png"))
        self.mcl_auto_number_btn = QAction(self.mcl_auto_number_off_icon, "",
                                           self.iface.mainWindow())
        self.mcl_auto_number_btn.setToolTip("Auto number MCL sections")
        self.mcl_auto_number_btn.hovered.connect(
            lambda: self._actionHovered(self.mcl_auto_number_btn))

        # Select feature button
        self.rdpoly_select_on_icon = QIcon(os.path.join(self.plugin_dir,
                                                   "image", "edit_poly_on_icon.png"))
        self.rdpoly_select_off_icon = QIcon(os.path.join(self.plugin_dir,
                                                      "image", "edit_poly_off_icon.png"))
        self.rdpoly_select_btn = QAction(self.rdpoly_select_off_icon, "",
                                       self.iface.mainWindow())
        self.rdpoly_select_btn.setToolTip("Select RAMP polygon")
        self.rdpoly_select_btn.hovered.connect(
            lambda: self._actionHovered(self.rdpoly_select_btn))

    def populate_menubar(self):
        # Top level menu items + add buttons
        self.rn_menu = self.menubar.addMenu("roadNet")
        self.add_roadnet_menu_items()
        self.menubar.addActions([self.street_sel_btn, self.sb_btn])
        self.exp_menu = self.menubar.addMenu("Export")
        self.add_export_menu_items()
        self.admin_menu = self.menubar.addMenu("Admin")
        self.add_admin_menu_items()
        if self.with_ramp:
            self.ramp_menu = self.menubar.addMenu("RAMP")
            self.add_ramp_menu_items()
            self.menubar.addActions([self.mcl_select_btn,
                                     self.mcl_auto_number_btn,
                                     self.rdpoly_select_btn])

    def add_roadnet_menu_items(self):
        # Add actions to Roadnet menu
        self.start_rn = self.rn_menu.addAction("Start roadNet")
        self.stop_rn = self.rn_menu.addAction("Stop roadNet")
        self.rn_menu.addSeparator()
        self.change_db_path = self.rn_menu.addAction("Change Database Location")
        self.settings = self.rn_menu.addAction("Settings")
        self.rn_menu.addSeparator()
        self.create_restore = self.rn_menu.addAction("Create Restore Point")
        self.change_pwd = self.rn_menu.addAction("Change Password")
        self.rn_menu.addSeparator()
        self.help = self.rn_menu.addAction("Help")
        self.about = self.rn_menu.addAction("About")

    def add_export_menu_items(self):
        # Add actions to Export menu
        self.exp_lgs = self.exp_menu.addAction("Export LSG")
        self.exp_srwr = self.exp_menu.addAction("Export SRWR")
        self.exp_menu.addSeparator()
        self.exp_lsg_shp = self.exp_menu.addAction("Export LSG Shapes")
        self.exp_maintain_poly = self.exp_menu.addAction(
            "Export Maintenance Polygons")
        self.exp_menu.addSeparator()
        self.exp_list_roads = self.exp_menu.addAction("List of Roads")

    def add_admin_menu_items(self):
        """
        Add actions to the admin menu.
        """
        self.meta_menu = self.admin_menu.addAction("Metadata")
        self.admin_menu.addSeparator()
        self.edit_lsg_lu = self.admin_menu.addAction("Edit LSG Lookups")
        self.edit_srwr_lu = self.admin_menu.addAction("Edit SRWR Lookups")
        self.admin_menu.addSeparator()
        self.validation_rpt = self.admin_menu.addAction("Validation Report")
        self.street_rpt = self.admin_menu.addAction("Street Reports")
        self.admin_menu.addSeparator()
        self.clean_rdpoly = self.admin_menu.addAction("Update Symbology")
        self.sb_btn.setEnabled(True)

    def add_ramp_menu_items(self):
        """
        Create actions that appear as items in RAMP menu
        """
        self.load_layers = self.ramp_menu.addAction("Load RAMP/MCL layers")
        self.ramp_menu.addSeparator()
        self.road_length = self.ramp_menu.addAction("Road length report")
        self.export_wdm = self.ramp_menu.addAction("Export for WDM")

    def set_state(self, role):
        """
        Set toolbar state, i.e. which buttons are enabled, based on user
        role.

        :param role: String from ['init', 'editor', 'readonly']
        """
        # Define buttons used in each mode
        roadnet_buttons = [self.start_rn, self.stop_rn, self.create_restore,
                           self.change_db_path, self.change_pwd, self.settings,
                           self.street_sel_btn, self.sb_btn, self.exp_menu,
                           self.admin_menu, self.meta_menu, self.edit_lsg_lu,
                           self.edit_srwr_lu, self.validation_rpt,
                           self.street_rpt, self.help, self.about]
        ramp_buttons = [self.ramp_menu, self.mcl_select_btn,
                        self.mcl_auto_number_btn, self.rdpoly_select_btn]

        init = [self.start_rn, self.change_db_path, self.about, self.help]
        readonly = [self.stop_rn, self.street_sel_btn, self.sb_btn,
                    self.exp_menu, self.admin_menu, self.meta_menu,
                    self.validation_rpt, self.street_rpt, self.settings,
                    self.create_restore, self.help, self.about]

        if self.with_ramp:
            roadnet_buttons += ramp_buttons
            readonly += ramp_buttons

        editor = readonly + [self.create_restore, self.change_pwd,
                             self.edit_lsg_lu, self.edit_srwr_lu]

        # Disable all buttons
        for button in roadnet_buttons:
            button.setEnabled(False)
        # Enable required buttons
        if role == 'init':
            for button in init:
                button.setEnabled(True)
        if role == 'readonly':
            for button in readonly:
                button.setEnabled(True)
        if role == 'editor':
            for button in editor:
                button.setEnabled(True)

    def street_sel_icon_state(self, state):
        """
        Change the text/icon of the street selector button to reflect state
        """
        if state == 'on':
            self.street_sel_btn.setText('on')
            self.street_sel_btn.setIcon(self.ss_on_icon)
        if state == 'off':
            self.street_sel_btn.setText('off')
            self.street_sel_btn.setIcon(self.ss_off_icon)

    def mcl_selector_icon_state(self, state):
        """
        Change the text/icon of the street selector button to reflect state
        """
        if state == 'on':
            self.mcl_select_btn.setText('on')
            self.mcl_select_btn.setIcon(self.mcl_select_on_icon)
        if state == 'off':
            self.mcl_select_btn.setText('off')
            self.mcl_select_btn.setIcon(self.mcl_select_off_icon)

    def rdpoly_selector_icon_state(self, state):
        """
        Change the text/icon of the street selector button to reflect state
        """
        if state == 'on':
            self.rdpoly_select_btn.setText('on')
            self.rdpoly_select_btn.setIcon(self.rdpoly_select_on_icon)
        if state == 'off':
            self.rdpoly_select_btn.setText('off')
            self.rdpoly_select_btn.setIcon(self.rdpoly_select_off_icon)

    def _actionHovered(self, action):
        tip = action.toolTip()
        QToolTip.showText(QCursor.pos(), tip)
