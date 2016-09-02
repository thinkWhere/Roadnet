# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDataWidgetMapper, QSortFilterProxyModel

from qgis.core import QgsPoint, QgsGeometry

from ..generic_functions import DateMapperCustomDelegate

__author__ = 'matthew.walsh'


class WidgetInfoObject:
        """
        Holds information about each of the widgets on the forms.
        """
        widget = None
        widget_type = None
        db_col = int()
        date_col = bool
        id_col = bool
        mapped = bool

        white = False

        def __init__(self, widget, widget_type, db_col, mapped=True, date_col=False, white=False, id_col=False):
            """
            Creates a WidgetInfoObject.
            :param widget: QWidget
            :param widget_type: Type of widget
            :param db_col: int database column linked to widget
            :param mapped: bool for mapped widgets
            :param date_col: Bool for if the widget holds a date
            :param white: Bool for if the widget should be white during edit mode
            :param id_col: Bool for if the widget contains an ID
            """
            self.widget = widget
            self. db_col = db_col
            self.mapped = mapped
            self.date_col = date_col
            self.id_col = id_col
            self.widget_type = widget_type
            self.white = white


class WidgetTypeEnum:
    """
    Enum for types of widget.
    """
    lineedit = 1
    dateedit = 2
    textedit = 3
    combo = 4

    def __init__(self):
        pass


class SetupMaintRecordOperationsButtons:
    """
    Enable/disable the SRWR operations buttons.
    """
    def __init__(self, street_browser, model, whole_rd_col, params):
        """
        :param street_browser: street browsers ui
        :param model: model
        :param whole_rd_col: Whole Rd col idx
        :param params: params dict
        """
        self.street_browser = street_browser
        self.model = model
        self.whole_rd_col = whole_rd_col
        self.params = params

    def setup(self):
        """
        Logic to enable operation buttons. If whole road then new records cannot be assigned
        """
        idx = self.street_browser.ui.srwrTabWidget.currentIndex()
        rc = self.model.rowCount()
        # Only enable srwr ops buttons if not in add/edit mode on street records
        filter_enabled = self.street_browser.ui.filterPushButton.isEnabled()
        if filter_enabled:
            if idx == 0:
                self.setup_maint_tab_buttons(rc)
            else:
                self.setup_other_tab_buttons(rc)

    def setup_maint_tab_buttons(self, row_count):
        """
        Logic to enable operation buttons. If whole road then new records cannot be assigned
        :param row_count: model row count
        """
        # Only change is not read only
        if self.params['role'] != 'readonly':
            if row_count > 0:
                counter = 0
                add = True
                while counter < row_count:
                    whole_rd = self.model.data(self.model.index(counter, self.whole_rd_col), Qt.DisplayRole)
                    counter += 1
                    if str(whole_rd).lower() == "yes":
                        add = False
                        break
                self.change_button_state(modify=True, add=add, delete=True, view=True)
            else:
                self.change_button_state(add=True)
        else:
            self.change_button_state(view=True)

    def setup_other_tab_buttons(self, row_count):
        """
        Logic to enable operation buttons.
        :param row_count: model row count
        """
        # Only change is not read only
        if self.params['role'] != 'readonly':
            if row_count > 0:
                self.change_button_state(modify=True, add=True, delete=True, view=True)
            else:
                self.change_button_state(add=True)

    def change_button_state(self, add=False, modify=False, delete=False, view=False):
        """
        Enable/disable the record operation buttons
        :param add: bool enable add
        :param modify: bool enable modify
        :param delete: bool enable delete
        :param view: bool enable view
        """
        self.street_browser.ui.srwrAddPushButton.setEnabled(add)
        self.street_browser.ui.srwrViewPushButton.setEnabled(view)
        self.street_browser.ui.srwrDeletePushButton.setEnabled(delete)
        self.street_browser.ui.srwrModifyPushButton.setEnabled(modify)


class SrwrViewRecord(object):
    """
    Functionality to view a SRWR record in separate form. This class is generic and can be used by all 3 SRWR tabs.
    """
    whole_road_col = int()

    def __init__(self, model, iface, dialog, whole_rd_col, widget_info, params):
        """
        Basic setup of class variables and some initial setup of mapper.
        :param model: Model from tableview
        :param iface: qgis iface hook
        :param dialog: dialog which is unique to each tab
        :param whole_rd_col: int for whole road column in tab table
        :param widget_info: List of widgetinfo objects for the provided dialog
        """
        self.view_dlg = dialog
        self.widgets = widget_info

        # Find the date columns from the widget info objects
        self.date_cols = []
        self.id_lineedit = None
        for w in widget_info:
            if w.date_col:
                self.date_cols.append(w.db_col)
            if w.id_col:
                self.id_lineedit = w.widget

        self.model = model
        self.whole_road_col = whole_rd_col
        self.iface = iface
        self.mapper = None
        self.proxy = None
        self.params = params
        self.view_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        self.setup_mapper()
        self.view_dlg.ui.mapPushButton.clicked.connect(self.zoom_to_map)
        self.view_dlg.ui.closePushButton.clicked.connect(self.complete)

    def whole_rd_state(self, state):
        """
        Checks if its a whole record and set checkbox accordingly
        :param state: Current state
        """
        checked = True
        if state == 2:
            checked = False
        self.view_dlg.ui.wholeRoadCheckBox.blockSignals(True)
        self.view_dlg.ui.wholeRoadCheckBox.setChecked(checked)
        self.view_dlg.ui.wholeRoadCheckBox.setChecked(False)

    def view(self, idx, usrn):
        """
        View a record details in a dialog
        :param idx: index of view in the model
        :param usrn: usrn of current record
        """
        row = idx.row()
        self.mapper.setCurrentIndex(row)
        self.view_dlg.ui.wholeRoadCheckBox.setEnabled(False)
        self.whole_road_checkbox(row)
        self.hide_buttons()
        self.view_dlg.show()

    def zoom_to_map(self):
        """
        Zoom the canvas to the start/end coords of the maint record
        """
        startx = self.view_dlg.ui.startXLineEdit.text()
        endx = self.view_dlg.ui.endXLineEdit.text()
        starty = self.view_dlg.ui.startYLineEdit.text()
        endy = self.view_dlg.ui.endYLineEdit.text()
        # Only zoom if values are present
        if startx and starty:
            coords_f = [QgsPoint(float(startx), float(starty)), QgsPoint(float(endx), float(endy))]
            geom = QgsGeometry().fromMultiPoint(coords_f)
            bbox = geom.boundingBox()
            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh()

    def complete(self):
        """
        Close the view form.
        """
        self.view_dlg.close()

    def whole_road_checkbox(self, row):
        """
        Sets whole road combo box based on value as it cannot be mapped.
        :param row: row in model
        """
        whole_rd = self.model.data(self.model.index(row, self.whole_road_col), Qt.DisplayRole)
        if whole_rd == 1 or str(whole_rd).lower() == "yes":
            self.view_dlg.ui.wholeRoadCheckBox.setChecked(True)
            self.view_dlg.ui.locationTextEdit.setPlainText("Whole road")
        else:
            self.view_dlg.ui.wholeRoadCheckBox.setChecked(False)

    def hide_buttons(self):
        """
        Hide buttons
        """
        self.view_dlg.ui.editLinkPushButton.setVisible(False)
        self.view_dlg.ui.editCoordsPushButton.setVisible(False)

    def setup_mapper(self):
        """
        Create the data widget mapper and set a proxy on the model
        """
        self.mapper = QDataWidgetMapper()
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)
        self.mapper.setModel(self.proxy)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        # Set custom delegate for mapping to date widgets
        self.mapper.setItemDelegate(DateMapperCustomDelegate(self.date_cols))
        self.map_widgets(self.mapper)

    def map_widgets(self, mapper):
        """
        Map widgets to columns
        :param mapper: QDataWidgetMapper
        """
        for w in self.widgets:
            if w.mapped:
                mapper.addMapping(w.widget, w.db_col)
