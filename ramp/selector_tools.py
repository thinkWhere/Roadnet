# -*- coding: utf-8 -*-

from qgis.gui import QgsMapToolIdentifyFeature
from qgis.core import QgsMapLayerRegistry, QgsExpression, QgsFeatureRequest
from PyQt4.QtCore import pyqtSignal, Qt, QObject
from PyQt4.QtGui import QCursor, QDialogButtonBox

from Roadnet.roadnet_dialog import RampEditLinkedPolysDlg
from Roadnet import config
from Roadnet.generic_functions import ipdb_breakpoint


class MclSelectorTool(QgsMapToolIdentifyFeature):
    """
    Select tool clicked on by user and emit the mcl_id.
    :param canvas: QGIS Map canvas instance
    :param vlayer: Vector layer to query
    """
    selected_id = pyqtSignal(str)  # Define custom signal to emit.

    def __init__(self, canvas, vlayer, toolbar):
        QgsMapToolIdentifyFeature.__init__(self, canvas, vlayer)
        self.canvas = canvas
        self.vlayer = vlayer
        self.toolbar = toolbar
        self.featureIdentified.connect(self.select_mcl)

    def select_mcl(self, feature):
        """
        Select the identified MCL and emit the mcl_ref
        :param feature: QgsFeature emitted by featureIdentified signal
        """
        mcl_ref_as_str = "{:.0f}".format(feature.attribute('mcl_ref'))
        self.selected_id.emit(mcl_ref_as_str)
        if config.DEBUG_MODE:
            print("DEBUG MODE: MCL {} selected".format(mcl_ref_as_str))
        self.vlayer.setSelectedFeatures([feature.id()])

    def toolName(self):
        return "MCL Selector Tool"

    def activate(self):
        """
        Overrides parent class.  Set custom cursor and change icon.
        """
        self.canvas.setCursor(QCursor(Qt.PointingHandCursor))
        self.toolbar.mcl_selector_icon_state("on")

    def deactivate(self):
        """
        Overrides parent class.  Change icon back.
        """
        self.toolbar.mcl_selector_icon_state("off")


class RampSelectorTool(QgsMapToolIdentifyFeature):
    """
    Select tool clicked on by user and emit the rd_pol_id.
    :param canvas: QGIS Map canvas instance
    :param vlayer: Vector layer to query
    """
    selected_id = pyqtSignal(str)  # Define custom signal to emit.

    def __init__(self, canvas, vlayer, toolbar):
        QgsMapToolIdentifyFeature.__init__(self, canvas, vlayer)
        self.canvas = canvas
        self.vlayer = vlayer
        self.toolbar = toolbar
        self.featureIdentified.connect(self.select_rdpoly)

    def select_rdpoly(self, feature):
        """
        Select the identified rdpoly and emit the rd_pol_id
        :param feature: QgsFeature emitted by featureIdentified signal
        """
        rd_pol_id_as_str = "{:.0f}".format(feature.attribute('rd_pol_id'))
        self.selected_id.emit(rd_pol_id_as_str)
        if config.DEBUG_MODE:
            print("DEBUG MODE: RAMP rdpoly {} selected".format(rd_pol_id_as_str))
        self.vlayer.setSelectedFeatures([feature.id()])

    def toolName(self):
        return "Ramp Polygon Selector Tool"

    def activate(self):
        """
        Overrides parent class.  Set custom cursor and change icon.
        """
        self.canvas.setCursor(QCursor(Qt.PointingHandCursor))
        self.toolbar.rdpoly_selector_icon_state("on")

    def deactivate(self):
        """
        Overrides parent class.  Change icon back.
        """
        self.toolbar.rdpoly_selector_icon_state("off")


class EditLinkedPolysTool(QObject):
    """
    Allow the user to view and update a list of selected features.
    """
    linked_polys_updated = pyqtSignal(list)
    current_mcl = None

    def __init__(self, original_selection, iface, parent_dlg):
        """
        :param original_selection: List of 'str' of rd_pol_ids
        """
        super(EditLinkedPolysTool, self).__init__()  # Need this to enable signals
        self.original_selection = original_selection
        self.iface = iface
        self.parent_dlg = parent_dlg

        self.dlg = RampEditLinkedPolysDlg()
        self.dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.dlg.move(50, 50)

        self.mcl, self.element, self.hierarchy = get_pointers_to_ramp_vector_layers()
        self.connect_signals()

    def connect_signals(self):
        """
        Connect GUI signals
        """
        ok_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Ok)
        cancel_button = self.dlg.ui.buttonBox.button(QDialogButtonBox.Cancel)
        ok_button.clicked.connect(self.done)
        cancel_button.clicked.connect(self.cancel)

    def launch(self):
        """
        Change layer to polygons and show the dialog
        :return:
        """
        # Clear selection from MCL layer to avoid confusion
        self.current_mcl = self.mcl.selectedFeatures()
        self.mcl.setSelectedFeatures([])

        # Activate element layer and select features from original selection
        self.iface.setActiveLayer(self.element)
        self.select_features_by_rd_pol_id(self.original_selection)

        # Connect selection changed signal once initial selection made
        self.element.selectionChanged.connect(self.update_linked_poly_box_from_selection)

        self.populate_linked_poly_box(self.original_selection)
        self.parent_dlg.showMinimized()
        self.dlg.show()

    def update_linked_poly_box_from_selection(self):
        """
        Update the linked poly box with the newly selected features.
        """
        selected_features = self.element.selectedFeatures()
        if selected_features:
            selected_rd_pol_ids = [str(feature['rd_pol_id'])
                                   for feature in selected_features]
        else:
            selected_rd_pol_ids = []
        self.populate_linked_poly_box(selected_rd_pol_ids)

    def select_features_by_rd_pol_id(self, linked_polygons):
        """
        Select map features based on rd_pol_id.
        :param linked_polygons: list of str of rd_pol_id
        """
        expr = "rd_pol_id IN ({})".format(', '.join(linked_polygons))
        linked_features = self.element.getFeatures(
            QgsFeatureRequest(QgsExpression(expr)))
        ids = [feature.id() for feature in linked_features]
        self.element.setSelectedFeatures(ids)

    def populate_linked_poly_box(self, items):
        """
        Populate the Linked Polygons box with items
        :param items: list of strings
        """
        poly_box = self.dlg.ui.linkedPolysListWidget
        poly_box.clear()
        poly_box.addItems(items)

    def get_items_from_linked_poly_box(self):
        """
        Get the values from the Linked Polygons box
        :return: list of strings
        """
        poly_box = self.dlg.ui.linkedPolysListWidget
        items = []
        for i in range(poly_box.count()):
            items.append(poly_box.item(i).data(Qt.DisplayRole))
        return items

    def done(self):
        """
        Closes the dialog and updates internal list of linked polys
        :return: list of str rd_pol_ids
        """
        # Emit updated values
        linked_polys = self.get_items_from_linked_poly_box()
        self.linked_polys_updated.emit(linked_polys)

        # Return selection to MCL layer and close dialog
        self.element.setSelectedFeatures([])
        self.iface.setActiveLayer(self.mcl)
        self.mcl.setSelectedFeatures(self.current_mcl)
        self.parent_dlg.showNormal()
        self.dlg.close()

    def cancel(self):
        """
        Closes the dialog and leaves linked polys at original value
        :return: list of str rd_pol_ids
        """
        # Change cancelled, so just emit original values
        self.linked_polys_updated.emit(self.original_selection)

        # Return selection to MCL layer and close dialog
        self.element.setSelectedFeatures([])
        self.iface.setActiveLayer(self.mcl)
        self.mcl.setSelectedFeatures(self.current_mcl)
        self.parent_dlg.showNormal()
        self.dlg.close()


def get_pointers_to_ramp_vector_layers():
    """
    Get links to vector layer instances, MCL, Element and Hierarchy
    :return: QgsVectorLayers
    """
    reg = QgsMapLayerRegistry.instance()
    mcl = reg.mapLayersByName('MCL')[0]
    element = reg.mapLayersByName('Element')[0]
    hierarchy = reg.mapLayersByName('Hierarchy')[0]
    return mcl, element, hierarchy
