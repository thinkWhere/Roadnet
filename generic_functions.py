# -*- coding: utf-8 -*-
import datetime
import os
from qgis.core import QGis, QgsPoint, QgsGeometry
from qgis.gui import QgsRubberBand, QgsVertexMarker

from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPushButton, QStackedWidget, QItemDelegate, QColor
from PyQt4.QtSql import QSqlQuery

import config

__author__ = 'matthew.walsh'


class DateMapperCustomDelegate(QItemDelegate):
    """
    A custom delegate to deal with populating qlineedits from sqlite dates
    """
    def __init__(self, date_cols, parent=None):
        self.date_cols = date_cols
        super(DateMapperCustomDelegate, self).__init__(parent)

    def setEditorData(self, editor, index):
        """
        Re-formats dates for the lineedit
        :param editor: Editor widget
        :param index: Model index
        """
        try:
            index_num = index.column()
            if index_num in self.date_cols:
                value = str(index.model().data(index, Qt.DisplayRole))
                date_obj = datetime.datetime.strptime(value, "%Y%m%d")
                date_clean = str(date_obj.strftime("%d/%m/%Y"))
                editor.setText(date_clean)
            else:
                QItemDelegate.setEditorData(self, editor, index)
        except ValueError:
            pass


class ZoomSelectCanvas:

    def __init__(self, iface, street_browser, db):
        self.iface = iface
        self.street_browser = street_browser
        self.plugin_dir = os.path.dirname(__file__)
        self.db = db

    def zoom_to_record(self, **kwargs):
        """
        Zoom map to extent of street (comprising of multiple esu's)
        :param kwargs: usrn, close, select, zoom_to
        """
        # Query db for ESU's which make up the street
        usrn = None
        close = False
        select = False
        zoom_to = False
        if 'usrn' in kwargs:
            usrn = kwargs['usrn']
        if 'close' in kwargs:
            close = kwargs['close']
        if 'select' in kwargs:
            select = kwargs['select']
        if 'zoom_to' in kwargs:
            zoom_to = kwargs['zoom_to']
        if usrn is None:
            usrn = self.street_browser.ui.usrnLineEdit.text()
        try:
            query = self.query_esu(usrn)
            feats_as_list = list(self.get_features_from_field_value(query, 'esu_id', 'ESU Graphic'))
            bbox_selected = None
            if select:
                bbox_selected = self.select_features(feats_as_list, 'ESU Graphic')
            if zoom_to and len(feats_as_list) > 0:
                self.zoom_to_extent(bbox_selected)
            else:
                # no ESUs attached to record
                return False
        except TypeError:
            # No esu's attached to record
            pass
        if close:
            self.close_browser()

    def get_features_from_field_value(self, value_list, field_n, layer_n):
        """
        Returns list of selected features give a list of esu's
        :rtype : QgsFeatureIterator
        :param esu_list: ESU;s to find and select
        :return: List of selected features
        """
        q_string = ""
        for value in value_list:
            q_string += '"%s" = %s OR ' % (str(field_n), str(value))
        q_string = q_string[:-3]
        # Get ref to layer
        layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_n)[0]
        # Select ESU's + get extent
        feats = layer.getFeatures(QgsFeatureRequest().setFilterExpression(q_string))
        return feats

    @staticmethod
    def select_features(feature_list, layer_name):
        """
        Select features in a specific layer, returns bbox
        :param feature_list: List of feats find extent
        :param layer_name: Name of layer in TOC
        :return: qgis bounding box
        """
        layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)[0]
        feat_ids = []
        for feature in feature_list:
            f_id = feature.id()
            feat_ids.append(f_id)
        layer.setSelectedFeatures(feat_ids)
        bbox = layer.boundingBoxOfSelected()
        return bbox

    def zoom_to_extent(self, bbox):
        """
        Zoom the max canvas to a bounding box
        :param bbox: extent to zoom to
        """
        bbox.scale(1.1)  # Expand the view to give some context.
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()

    def query_esu(self, usrn):
        """
        Fetch all esu's which are linked to a given usrn
        :param usrn: USRN
        :return: list of esu's
        """
        esus = []
        query_str = "SELECT esu_id FROM lnkESU_STREET WHERE usrn = %s AND currency_flag = 0;" % usrn
        query = QSqlQuery(query_str, self.db)
        while query.next():
            esus.append(query.value(0))
        return esus

    def close_browser(self):
        """
        Close the street browser
        """
        self.street_browser.close()


class MapLookupValues:
    """
    Retrieve the actual data values for any relational row in a model
    """

    class FieldObject:
        """Class to represent a (possibly) mapped field"""
        name = ""
        index = None  # int
        relational = None  # bool
        display_data = ""
        lookup_data = ""

    def __init__(self, model):
        self.model = model

    def find_relation(self, row, col):
        """
        Find the lookup table value for a given row and col, returns a FieldObject
        :param row:
        :param col:
        :return:
        """
        # Get non-relational data to populate field
        record = self.model.record(row)
        field_name = record.fieldName(col)
        disp_data = record.field(col).value()

        # Get data for relational columns
        column_relation = self.model.relation(col)
        if column_relation.isValid():
            relational = True
            data_num = self._get_foreign_key_id(row, col)
        else:
            relational = False
            data_num = ""

        # Populate the field object for return
        field = self.create_field_obj(field_name, col, disp_data, data_num, relational)
        return field

    def _get_foreign_key_id(self, row, col):
        """
        Return the foreign key used in the relational model i.e. the value stored in
        the master database table.  This is a hack because the relationModel method was
        failing.  Column IDs are used because names can change in model.
        :param row: Row of the model
        :param col: Column of the model
        :return: Integer data row id converted to a string.
        """
        record = self.model.record(row)
        pk_uid = record.field('PK_UID').value()
        # Using SELECT * is also a horrible hack, but the model has different column names
        # to the original table.  This will break if SELECT statement for model changes.
        sql = """SELECT *
                 FROM tblSTREET WHERE
                 PK_UID IS {pk_uid};""".format(pk_uid=pk_uid)
        db = self.model.database()
        foreign_key_query = QSqlQuery(sql, db)
        if not foreign_key_query.next():
            # Something went wrong when selecting first result
            raise ValueError(foreign_key_query.lastError().text())
        record = foreign_key_query.record()
        id_as_string = "{}".format(record.value(col))
        return id_as_string

    def all_mapped_fields(self, row, lookup_display_col, lookup_data_col):
        """
        Returns a list of FieldObjects with mapped data as an attribute for each col in the row
        :param row:
        :param lookup_display_col:
        :param lookup_data_col:
        :return:
        """
        all_mapped = []
        record = self.model.record(row)
        for col in range(record.count()):
            field_obj = self.find_relation(row, col)
            all_mapped.append(field_obj)
        return all_mapped

    def create_field_obj(self, f_name, index, disp_data, data, relational):
        """
        Set attributes on new FieldObject instance
        :rtype : FieldObject
        :param f_name: Field name
        :param index: idx
        :param disp_data: display data
        :param data: display data or lookup value
        :param relational: Relational field
        """
        field = self.FieldObject()
        field.display_data = disp_data
        field.lookup_data = data
        field.name = f_name
        field.index = index
        field.relational = relational
        return field


class SwitchStreetBrowserMode:
    """
    Switch the street browser between edit mode and read only mode, only deals with GUI changes
    """

    def __init__(self, street_browser):
        self.street_browser = street_browser

    def edit(self):
        # Change the items to edit mode
        self.street_browser.ui.descriptionTextEdit.setReadOnly(False)
        self.street_browser.ui.descriptionTextEdit.setStyleSheet("background-color: white")
        # Change index of stacked widgets
        self.switch_stacked_widget(1)
        self.toggle_buttons(False)
        # Manually enable edit buttons
        self.street_browser.ui.editEsuPushButton.setEnabled(True)
        self.street_browser.ui.editCoordsPushButton.setEnabled(True)

    def read_only(self):
        # Returns the street browser to read only
        self.street_browser.ui.descriptionTextEdit.setReadOnly(True)
        self.street_browser.ui.descriptionTextEdit.setStyleSheet("background-color : rgb(213,234,234)")
        self.street_browser.ui.descriptionLabel.setStyleSheet("color : black")
        self.street_browser.ui.typeLabel.setStyleSheet("color : black")
        self.street_browser.ui.countyLabel.setStyleSheet("color : black")
        self.street_browser.ui.authorityLabel.setStyleSheet("color : black")
        # Change index of stacked widgets
        self.switch_stacked_widget(0)
        self.toggle_buttons(True)
        # Manually disable edit buttons
        self.street_browser.ui.editEsuPushButton.setEnabled(False)
        self.street_browser.ui.editCoordsPushButton.setEnabled(False)
        # Force the tab widget back to the maint tab
        self.street_browser.ui.srwrTabWidget.setCurrentIndex(0)

    def switch_stacked_widget(self, index):
        # Change index of stacked widgets
        all_stackedwidgets = self.street_browser.findChildren(QStackedWidget)
        for stacked in all_stackedwidgets:
            stacked.setCurrentIndex(index)

    def toggle_buttons(self, enable):
        # Enable/disable buttons
        all_buttons = self.street_browser.findChildren(QPushButton)
        always_enabled = ["Help", "Complete"]
        for button in all_buttons:
            if button.text() not in always_enabled:
                button.setEnabled(enable)

    def mandatory_field_check(self):
        # Checks to ensure all mandatory fields are populated
        desc_text = str(self.street_browser.ui.descriptionTextEdit.toPlainText())
        if len(desc_text) == 0:
            return False
        else:
            return True


class ShowStreetCoordinates:
    """
    Creates temp geoms to show the start and end coordinates of a street
    """
    def __init__(self, iface):
        self.canvas = iface.mapCanvas()
        self.rb_line = QgsRubberBand(self.canvas, QGis.Line)
        self.rb_start = QgsVertexMarker(self.canvas)
        self.rb_end = QgsVertexMarker(self.canvas)
        self.style()

    def style(self):
        # Style start marker
        self.rb_start.setColor(QColor('blue'))
        self.rb_start.setIconSize(16)
        self.rb_start.setPenWidth(4)
        # Style end marker
        self.rb_end.setColor(QColor('red'))
        self.rb_end.setIconSize(16)
        self.rb_end.setPenWidth(4)
        # Style line
        self.rb_line.setColor(QColor('grey'))
        self.rb_line.setWidth(3)

    def show(self, coords):
        # Breakdown coords
        start = coords[0]
        end = coords[1]
        # Create start and end points
        start_point = QgsPoint(float(start[0]), float(start[1]))
        self.rb_start.setCenter(start_point)
        end_point = QgsPoint(float(end[0]), float(end[1]))
        self.rb_end.setCenter(end_point)
        # Create line
        line_pts = [start_point, end_point]
        line_geom = QgsGeometry().fromPolyline(line_pts)
        self.rb_line.setToGeometry(line_geom, None)

    def remove(self):
        self.canvas.scene().removeItem(self.rb_start)
        self.canvas.scene().removeItem(self.rb_end)
        self.canvas.scene().removeItem(self.rb_line)


def ipdb_breakpoint():
    """
    Drops code into IPython debugger when QGIS is run from command line.  
    Otherwise returns an error.  Press 'c' to *continue* running code.
    """
    import ipdb 
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    ipdb.set_trace()

def pydev_breakpoint():
    """
    Creates a debug point for pydev that can be accessed by Pycharm.
    """
    print("Starting pydev debug server.")
    import pydevd
    pydevd.settrace('localhost',
                    port=53100,
                    stdoutToServer=True,
                    stderrToServer=True)
