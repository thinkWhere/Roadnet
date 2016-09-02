# -*- coding: utf-8 -*-
import os
import weakref
import collections

from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import QMessageBox
from PyQt4.QtSql import QSqlQuery

from qgis.core import QgsMapLayerRegistry

from Roadnet import config
from Roadnet.generic_functions import ipdb_breakpoint
from Roadnet import vector_layers
from Roadnet.geometry.mcl_edit_handler import MclEditHandler
from Roadnet.ramp.wdm_export_handler import WdmExportHandler
from Roadnet.ramp.length_of_roads_export_handler import LengthOfRoadsExportHandler
from Roadnet.ramp.selector_tools import MclSelectorTool, RampSelectorTool
from Roadnet.ramp.record_editors import MclRecordEditor, RdpolyRecordEditor
from Roadnet.ramp.mcl_auto_numbering_tool import MclAutoNumberingTool
import Roadnet.roadnet_exceptions as rn_except


def show_messagebox(message, message_type=QMessageBox.Information):
    """
    Pop up a QMessage information box containing message
    """
    msg_box = QMessageBox(
        message_type, " ", message,
        QMessageBox.Ok, None)
    msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    msg_box.exec_()


class Ramp(object):
    """
    Class to hold RAMP features and link to roadNet.
    """
    ramp_started = False
    mcl = None
    mcl_edit_handler = None
    auto_numbering_tool = None
    element = None
    hierarchy = None
    _rn = None
    mcl_selector_tool = None
    mcl_record_editor = None
    rdpoly_selector_tool = None
    rdpoly_record_editor = None

    def __init__(self, roadnet):
        self.rn = roadnet

    @property
    def rn(self):
        # Making rn a property allows easy overwriting of getters and setters.
        return self._rn()

    @rn.setter
    def rn(self, value):
        # A weakref is used because reference to roadnet is circular
        self._rn = weakref.ref(value)

    def __getattr__(self, attr):
        """
        This is called when an attribute does not exist.  In this case
        roadNet attributes are also searched.
        """
        return getattr(self.rn, attr)

    def start_ramp(self):
        self.ramp_started = True

    def stop_ramp(self):
        # Remove the RAMP vector layers
        for vlayer in [self.element, self.mcl, self.hierarchy]:
            if vlayer:
                try:
                    vector_layers.remove_spatialite_layer(vlayer, self.iface)
                except rn_except.RemoveNonExistentLayerPopupError:
                    # Layer has already been deleted
                    pass

        # Unset RAMP map tools
        if self.mcl_selector_tool:
            self.canvas.unsetMapTool(self.mcl_selector_tool)

        self.ramp_started = False

    def run_ramp_load_layers(self):
        """
        Add the MCL, Hierarchy and Element layers to the QGIS display
        """
        try:
            self.check_ramp_table_structure()
        except rn_except.BadRampTableStructureError:
            return

        db_path = self.db.databaseName()

        # Set layer names as ordered dict so that they load in correct order
        layers = collections.OrderedDict([('Hierarchy', 'rdpoly'),
                                          ('Element', 'rdpoly'),
                                          ('MCL', 'mcl')])

        registry = QgsMapLayerRegistry.instance()

        for key, vlayer in layers.items():
            pointer = key.lower()
            # Check layer isn't already loaded and visible
            if len(registry.mapLayersByName(key)) > 0:
                if config.DEBUG_MODE:
                    print("DEBUG MODE: {} already added".format(key))
                continue

            # Load layer, displaying error message in case of failure
            try:
                layer = vector_layers.add_styled_spatialite_layer(
                    vlayer, key, db_path, self.iface)
            except rn_except.QMessageBoxWarningError:
                # Exception informed user of invalid layer name via message box
                continue

            # Store link to layer
            setattr(self, pointer, layer)

        # Connect editing signals for mcl
        try:
            self.mcl.editingStarted.connect(self.editing_mcl_begin)
            self.mcl.editingStopped.connect(self.editing_mcl_end)
        except AttributeError:
            # Throws if MCL layer couldn't be loaded
            pass

    def editing_mcl_begin(self):
        """
        Creates class to listen for edit events on the MCL layer
        """
        # Always prohibit overlapping MCLs
        handle_intersect_flag = True

        # Disable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        self.mcl_edit_handler = MclEditHandler(
            self.iface, self.mcl, self.db, self.params, handle_intersect_flag)

    def editing_mcl_end(self):
        self.mcl_edit_handler = None
        self.params['session_includes_edits'] = True
        # Re-enable attributes dialog
        QSettings().setValue(
            '/qgis/digitizing/disable_enter_attribute_values_dialog', False)
        if self.mcl.isEditable() is True:
            # Rolling back changes ends destroys geometry_handler class but
            # layer remains editable.  In this case, recreate it.
            self.editing_mcl_begin()

    def run_ramp_road_length(self):
        """
        Run Length of roads export
        """
        lor_export_handler = LengthOfRoadsExportHandler(self.db, self.params,
                                                        self.iface)

        # Calculate length of roads
        try:
            lor_export_handler.export_length_of_roads()
        except rn_except.BadSpatialiteVersionPopupError, e:
            return

        # Save directory for later
        self.params['RAMP_output_directory'] = lor_export_handler.output_dir

    def run_ramp_export_wdm(self):
        """
        Run export to WDM
        """
        wdm_export_handler = WdmExportHandler(self.db, self.params, self.iface)

        # Directory is set to '' if user presses cancel
        if wdm_export_handler.output_dir == '':
            return

        # Export
        wdm_export_handler.export_shapefiles()

        # Save directory for later
        self.params['RAMP_output_directory'] = wdm_export_handler.output_dir

    def run_ramp_mcl_select(self):
        """
        Run module
        """
        if self.mcl is None:
            msg = "RAMP MCL layer must be loaded to use this tool"
            show_messagebox(msg, QMessageBox.Warning)
            return

        # Set MCL layer to active
        self.iface.setActiveLayer(self.mcl)

        # Activate selector tool
        # Done here, rather than __init__ because mcl layer doesn't exist then.
        self.mcl_selector_tool = MclSelectorTool(self.canvas, self.mcl, self.toolbar)
        self.canvas.setMapTool(self.mcl_selector_tool)

        # Start editor tool
        self.mcl_record_editor = MclRecordEditor(self.db, self.mcl_selector_tool,
                                                 self.iface)

    def run_mcl_auto_number(self):
        """
        Run module
        """
        if self.mcl is None:
            msg = "RAMP MCL layer must be loaded to use this tool"
            show_messagebox(msg, QMessageBox.Warning)
            return

        # Set MCL layer to active
        self.iface.setActiveLayer(self.mcl)

        # Deactivate other map tools, (throws attribute if tool not running)
        try:
            self.mcl_selector_tool.deactivate()
        except AttributeError:
            pass
        try:
            self.rdpoly_selector_tool.deactivate()
        except AttributeError:
            pass

        # Start auto numbering tool
        self.auto_numbering_tool = MclAutoNumberingTool(self.mcl, self.db,
                                                        self.iface)
        self.auto_numbering_tool.launch()

    def run_ramp_rdpoly_select(self):
        """
        Ramp selector tool is based on Element view of rdpoly table.
        """
        if self.element is None:
            msg = "RAMP Element layer must be loaded to use this tool"
            show_messagebox(msg, QMessageBox.Warning)
            return

        # Set MCL layer to active
        self.iface.setActiveLayer(self.element)

        # Activate selector tool
        # Done here, rather than __init__ because mcl layer doesn't exist then.
        self.rdpoly_selector_tool = RampSelectorTool(self.canvas, self.element, self.toolbar)
        self.canvas.setMapTool(self.rdpoly_selector_tool)

        # Start editor tool
        self.rdpoly_record_editor = RdpolyRecordEditor(self.db, self.rdpoly_selector_tool,
                                                       self.iface)

    def check_ramp_table_structure(self):
        """
        Ensure that rdpoly and mcl tables have correct column order, as this
        is necessary for mappings to work correctly.
        """
        table_structures = {
            'rdpoly': ['PK_UID', 'symbol', 'rd_pol_id', 'element', 'hierarchy',
                       'ref_1', 'ref_2', 'desc_1', 'desc_2', 'desc_3', 'ref_3',
                       'currency_flag', 'part_label', 'label', 'label1',
                       'feature_length', 'r_usrn', 'mcl_cref', 'geometry'],
            'mcl': ['PK_UID', 'esu_id', 'symbol', 'usrn', 'rec_type',
                    'desc_text', 'locality', 'town', 'entry_date',
                    'typ_3_usrn', 'typ_3_desc', 'typ_4_usrn', 'typ_4_desc',
                    'lor_ref_1', 'lor_ref_2', 'lor_desc', 'lane_number',
                    'speed_limit', 'rural_urban_id', 'section_type',
                    'adoption_status', 'mcl_ref', 'street_classification',
                    'in_pilot', 'carriageway', 'geometry']}

        for table, good_cols in table_structures.iteritems():
            actual_names = self.get_table_column_names(table)
            if actual_names != good_cols:
                msg = "Table {} is not suitable for RAMP.  ".format(table)
                msg += "This is probably due to database migration prior to "
                msg += "RAMP development.  Contact thinkWhere for advice."
                raise rn_except.BadRampTableStructureError(msg)

    def get_table_column_names(self, table_name):
        """
        Get list of table column names.
        :param table_name:
        :return: list of table column names
        """
        sql = "PRAGMA table_info({})".format(table_name)
        query = QSqlQuery(sql, self.db)

        col_names = []
        while query.next():
            record = query.record()
            col_names.append(record.value('name'))

        return col_names

