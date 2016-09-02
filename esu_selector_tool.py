# -*- coding: utf-8 -*-

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import (
    QAbstractItemView,
    QCursor,
    QSortFilterProxyModel,
    QTableWidgetItem,
    QColor)
from PyQt4.QtSql import QSqlQuery

from roadnet_dialog import StreetSelectorDlg
from generic_functions import ZoomSelectCanvas
from qgis.gui import QgsMapToolIdentify


class EsuSelectorTool(QgsMapToolIdentify):
    """
    Tool for showing/displaying a street record by selecting an ESU.
    Inherits the QGIS identify tool.
    """

    def __init__(self, street_browser_dk, iface, esu_layer, toolbar, db, mapper):
        """
        Build on init of QgsMapToolIdentify class for custom RN functionality.
        :param street_browser_dk: Street Browser dialog
        :param iface: Qgis interface reference
        :param esu_layer: ESU Graphic layer
        :param toolbar: toolbar instance
        :param db: database connection
        :param mapper: Qdatawidgetmapper of street browser
        """
        self.street_browser_dk = street_browser_dk
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.db = db
        self.zoom_funct = ZoomSelectCanvas(self.iface, self.street_browser_dk, self.db)
        self.layer = esu_layer
        self.toolbar = toolbar
        # Data widget mapper used in sb
        self.mapper = mapper
        # Set hand cursor
        self.cursor = QCursor(Qt.PointingHandCursor)
        # Create street selector dialog
        self.street_sel_dlg = StreetSelectorDlg()
        self.street_sel_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        # Connect street selector buttons
        self.connect_actions()
        QgsMapToolIdentify.__init__(self, self.canvas)

    def connect_actions(self):
        """
        Connect buttons + row double click
        """
        self.street_sel_dlg.ui.cancelPushButton.clicked.connect(self.cancel)
        self.street_sel_dlg.ui.okPushButton.clicked.connect(self.select_street_record)
        # Connect double click same as OK button
        self.street_sel_dlg.ui.usrnTableWidget.doubleClicked.connect(self.select_street_record)

    def activate(self):
        """
        Fire once tool is enabled. Overrides default method.
        """
        self.toolbar.street_sel_icon_state('on')
        self.canvas.setCursor(self.cursor)

    def unset_map_tool(self):
        """
        Deactivate the tool, called externally on roadnet stop
        """
        self.canvas.unsetMapTool(self)

    def toolName(self):
        return "ESU SELECTOR"

    def canvasReleaseEvent(self, mouseEvent):
        """
        Fire after canvas click.  Populate the street selector dialog and selects streets. Overrides default method.
        :param mouseEvent: mouse position x/y
        """
        results = self.identify(mouseEvent.x(), mouseEvent.y(), [self.layer])
        self.filter_results(results)
        # Select a single feature on the canvas
        feature = self.filter_results(results)
        if feature:
            ZoomSelectCanvas.select_features([feature], 'ESU Graphic')
            esu_id = feature.attribute("esu_id")
            self.populate_usrn_table(esu_id)

    def deactivate(self):
        """
        Fires once another map tool is selected. Overrides default method to change the icons on of the tool.
        """
        self.toolbar.street_sel_icon_state('off')
        self.street_sel_dlg.close()

    def reset_table(self, table_widget):
        """
        Clear table + reset row count
        :param table_widget: QTableWidget
        """
        table_widget.clearContents()
        table_widget.setRowCount(0)
        table_widget.setColumnWidth(0, 60)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def query_for_usrn(self, esu_id):
        """
        Get all street records which linked to the specified esu, returns list of tuples
        :param esu_id: ESU ID
        :return: List of streets
        """
        results = []
        sql = """
            SELECT lnkESU_STREET.usrn, tblSTREET.street_ref_type,
            tblSTREET.description
            FROM tblSTREET
            INNER JOIN
            lnkESU_STREET ON tblSTREET.usrn=lnkESU_STREET.usrn
            WHERE lnkESU_STREET.esu_id = %s AND
            lnkESU_STREET.currency_flag = 0 GROUP BY lnkESU_STREET.usrn
            ORDER BY lnkESU_STREET.usrn""" % str(esu_id)
        query = QSqlQuery(sql, self.db)
        while query.next():
            usrn = query.value(0)
            type_ = query.value(1)
            desc = query.value(2)
            results.append((usrn, "Type " + str(type_), desc))
        del(query)
        return results

    def populate_usrn_table(self, esu_id):
        """
        Populate the esu_id selector table widget with all linked usrn's
        :param esu_id: ESU ID
        """
        street_records = self.query_for_usrn(esu_id)
        if street_records:
            # Set esu_id label text
            esu_label = self.street_sel_dlg.ui.esuLabel
            esu_label.setText(str("ESU: " + str(esu_id)))
            table_widget = self.street_sel_dlg.ui.usrnTableWidget
            # Clear table
            self.reset_table(table_widget)
            row_count = table_widget.rowCount()
            # loop to populate records
            for record in street_records:
                col = 0
                table_widget.insertRow(row_count)
                for item in record:
                    t_item = QTableWidgetItem()
                    t_item.setText(str(item))
                    item_color = QColor(213, 234, 234)
                    t_item.setBackgroundColor(item_color)
                    t_item.setSelected(True)
                    self.street_sel_dlg.ui.usrnTableWidget.setItem(row_count, col, t_item)
                    col += 1
                row_count += 1
            table_widget.selectRow(0)
            self.street_sel_dlg.exec_()
        else:
            pass

    def set_sb_mapper_idx(self, usrn):
        """
        Use a proxy to find the mapper idx for the usrn
        :param usrn: USRN
        """
        model = self.mapper.model()
        # Create proxy
        search_proxy = QSortFilterProxyModel()
        search_proxy.setSourceModel(model)
        search_proxy.setDynamicSortFilter(True)
        search_proxy.setFilterKeyColumn(1)  # usrn col
        search_proxy.setFilterFixedString(str(usrn))
        # Assume only 1 record is in the filtered proxy
        source_idx = search_proxy.mapToSource(search_proxy.index(0, 0))
        source_row = source_idx.row()
        self.mapper.setCurrentIndex(source_row)

    def cancel(self):
        """
        Close dialog
        """
        self.street_sel_dlg.close()

    def select_street_record(self):
        """
        Zoom to street + set index in street browser
        """
        try:
            # Get usrn from current row
            cur_row = self.street_sel_dlg.ui.usrnTableWidget.currentRow()
            usrn = self.street_sel_dlg.ui.usrnTableWidget.item(cur_row, 0).text()
            # Zoom to whole street
            self.zoom_to_street(usrn)
            # Set db index
            self.set_sb_mapper_idx(usrn)
            self.street_sel_dlg.close()
            self.street_browser_dk.show()
        except AttributeError:
            # Nothing selected
            pass

    def zoom_to_street(self, usrn):
        """
        Zoom to canvas to the street
        :param usrn: USRN no
        """
        self.zoom_funct.zoom_to_record(usrn=usrn, select=True, zoom_to=True)

    def filter_results(self, results):
        """
        Returns a single selected feature
        :param results:
        :return: Feature or false for more than 1
        """
        if len(results) == 1:
            feature = results[0].mFeature
            return feature
        else:
            # More than 1 feature identified or 0 features identified
            return False
