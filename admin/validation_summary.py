# -*- coding: utf-8 -*-
from PyQt4.QtGui import QTableWidgetItem, QResizeEvent, QTableWidget, QMessageBox
from PyQt4.QtCore import QSize, Qt, QModelIndex
from ..generic_functions import ipdb_breakpoint, ZoomSelectCanvas

__author__ = 'Alessandro Cristofori'


class ValidationSummary:
    def __init__(self, validation_dk, iface, db, tolerance):
        self.validation_dk = validation_dk
        self.tolerance = tolerance
        self.tables = {}
        self.list_check_tables = None
        self.init_tables()
        self.columns_count = None
        self.include_footpath = False
        self.iface = iface
        self.db = db
        self.zoom_select_canvas = ZoomSelectCanvas(self.iface, None, self.db)

    def init_tables(self):
        """ initalise dictionary that relates each table in the
        report to each checkbox int the validation form """
        self.tables = {
            0: self.validation_dk.ui.dupDesTable,
            1: self.validation_dk.ui.noLinkEsuTable,
            2: self.validation_dk.ui.noType3Table,
            3: self.validation_dk.ui.dupEsuRefTable,
            4: self.validation_dk.ui.notEsuStreetTable,
            5: self.validation_dk.ui.type12StreetsTable,
            6: self.validation_dk.ui.type34StreetsTable,
            7: self.validation_dk.ui.unofficialTypeStreetsTable,
            8: self.validation_dk.ui.startEndTable,
            9: self.validation_dk.ui.tinyEsuTable,
            10: self.validation_dk.ui.noGeomEsuTable,
            11: self.validation_dk.ui.notMaintTable,
            12: self.validation_dk.ui.notReinsTable,
            13: self.validation_dk.ui.asdMaintCoordTable,
            14: self.validation_dk.ui.asdSpecDesCoordTable,
            15: self.validation_dk.ui.asdReinsCoordTable,
            16: self.validation_dk.ui.maintRecTable,
            17: self.validation_dk.ui.polyMaintTable,
            18: self.validation_dk.ui.multiPolyTable,
            19: self.validation_dk.ui.tinyPolysTable,
            20: self.validation_dk.ui.noGeomPolysTable
        }
        # clean up previous tolerance values if any
        tol_text_temp = self.validation_dk.ui.toleranceLabel.text()
        present_value = tol_text_temp.split(":")
        if present_value[1]:
            tol_text_temp = present_value[0] + ":"
        tol_text = tol_text_temp + " " + str(self.tolerance) + " metres"
        self.validation_dk.ui.toleranceLabel.setText(tol_text)

    def set_table(self, content_list, table_id):
        """
        this method accesses the passed lists and gets the data to populate
        the respective table on the dock window
        :param content_list: list[string] report items
        :return: void
        """
        # get the number of rows
        n_rows = len(content_list)
        # if we have no results we keep the headers
        if n_rows is not 1:
            n_rows = len(content_list) - 1
            if table_id is 2 or table_id is 3:
                self.write_subtitles(table_id)
        # iterate through each row
        header_list = str(content_list[0][0]).split(',')
        n_columns = len(header_list)
        self.columns_count = n_columns
        ref_table = self.tables[table_id]
        ref_table.setRowCount(n_rows)
        ref_table.setColumnCount(n_columns)
        ref_table.setHorizontalHeaderLabels(header_list)
        self.populate_table(content_list, table_id)

    def write_subtitles(self, table_id):
        """
        writes subtitles to certain widget tables only if they have records
        :param table_id: [int] the reference table on the widget
        :return: void
        """
        if table_id == 2:
            # add subtitle on the third table
            self.validation_dk.ui.noType3Label.setText("NOTE : Some of these ESUs may be linked to private "
                                                       "parts of streets that are part public and part private.")
        if table_id == 3:
            # add item to the label on the fourth table
            self.validation_dk.ui.dupEsuRefLabel.setText("The following ESUs have duplicate ESU references. "
                                                         "It is important that these are unique values. "
                                                         "\nThese references are based on the ESU midpoint "
                                                         "and are used when exporting to DTF.")

    def populate_table(self, content_list, table_id):
        """
        populates the created table with the data
        :param table_id: int the id of the table to which write the data
        :param content_list: string data content
        :return: void
        """
        ref_table = self.tables[table_id]
        # handles the special case of the start/end list
        if table_id == 8:
            l = 1
            while l <= len(content_list) - 1:
                m = 0
                while m <= len(content_list[l]) - 1:
                    table_item = QTableWidgetItem(str(content_list[l][m]).replace(",", ""), 0)
                    ref_table.setItem(l, m, table_item)
                    m += 1
                l += 1
            ref_table.removeRow(0)
        else:
            if table_id == 2 and self.include_footpath:
                self.validation_dk.ui.type3GroupBox.setTitle(
                    str(self.validation_dk.ui.type3GroupBox.title()) + " (including footpaths)"
                )
            # writes data to columns
            i = 1
            ordered_list = []
            while i <= len(content_list) - 1:
                item_list = str(content_list[i][0]).split('|')
                ordered_list.append(item_list)
                i += 1
            j = 0
            while j <= len(ordered_list) - 1:
                k = 0
                while k <= len(ordered_list[j]) - 1:
                    table_item = QTableWidgetItem(str(ordered_list[j][k]), 0)
                    ref_table.setItem(j, k, table_item)
                    k += 1
                j += 1
        # resize column widths to content
        ref_table.resizeColumnsToContents()
        # hide horizontal header
        ref_table.verticalHeader().hide()
        m = 0
        columns_sizes = 0
        while m <= self.columns_count - 1:
            header = ref_table.horizontalHeaderItem(m)
            column_size = ref_table.sizeHintForColumn(m)
            columns_sizes += column_size
            m += 1
        ref_table.horizontalHeader().setStretchLastSection(True)
        old_size = QSize()
        new_size = QSize()
        old_size.setWidth(ref_table.width())
        new_size.setWidth(columns_sizes)
        resize_event = QResizeEvent(new_size, old_size)
        ref_table.resizeEvent(resize_event)
        ref_table_selection_model = ref_table.selectionModel()
        ref_table.doubleClicked.connect(lambda: self.get_esu_or_usrn(ref_table_selection_model))
        ref_table.setToolTip("Double click on a record to zoom to the feature.")

    def show_validation_widget(self):
        """shows the validation widget"""
        self.validation_dk.show()

    def clear_tables_contents(self):
        """ clear the tables from any previous data """
        self.list_check_tables = self.validation_dk.findChildren(QTableWidget)
        for table in self.list_check_tables:
            table.clear()

    def get_esu_or_usrn(self, selection_model):
        """
        get the appropriate information from the table to zoom to
        the record feature
        :param selection_model: selection index of the double clicked table
        :return: void
        """
        selected_indexes = selection_model.selectedIndexes()
        useful_data = {}

        # get the selected record data
        i = 0
        for selected_index in selected_indexes:
            selected_index_model = selected_index.model()
            column_name = selected_index_model.headerData(i, Qt.Horizontal, Qt.DisplayRole).strip()
            # build a dictionary of useful columns:data
            if column_name in ('ESU ID', 'Polygon ID', 'USRN'):
                try:
                    column_data = int(selected_index.data())
                except (ValueError, TypeError):
                    self.show_no_features_found_warning()
                    return
                useful_data[column_name] = column_data
            i += 1

        if useful_data == {}:
            self.show_no_features_found_warning()
            return
        # extracts data and column to zoom
        dict_has_esu_id = ("ESU ID" in useful_data.keys())
        dict_has_poly_id = ("Polygon ID" in useful_data.keys())
        dict_has_usrn = ("USRN" in useful_data.keys())
        if dict_has_usrn and dict_has_poly_id:
            self.zoom_to_feature("Polygon ID", useful_data["Polygon ID"])
        elif dict_has_esu_id and dict_has_usrn:
            self.zoom_to_feature("ESU ID", useful_data["ESU ID"])
        else:
            for key, value in useful_data.iteritems():
                self.zoom_to_feature(key, value)

    def zoom_to_feature(self, column_name, item_id):
        """
        gets the id to link the feature to the generic functions to zoom
        :param item_id: the id of the feature we want to zoom to
        :param column_name: the column containing the id
        :return:
        """
        layer_names = {'ESU ID': 'ESU Graphic', 'Polygon ID': 'Road Polygons'}
        id_column_names = {'ESU ID': 'esu_id', 'Polygon ID': 'rd_pol_id'}
        if column_name == "USRN":
            usrn_has_feat = self.zoom_select_canvas.zoom_to_record(usrn=item_id, zoom_to=True, select=True)
            if usrn_has_feat is False:
                self.show_no_features_found_warning()
        else:
            item_id = [item_id]
            feats_as_list = list(self.zoom_select_canvas.get_features_from_field_value(
                item_id, id_column_names[column_name], layer_names[column_name]))
            bbox_selected = self.zoom_select_canvas.select_features(feats_as_list, layer_names[column_name])
            if len(feats_as_list) > 0:
                self.zoom_select_canvas.zoom_to_extent(bbox_selected)
            else:
                self.show_no_features_found_warning()

    def show_no_features_found_warning(self):
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
        self.iface.mapCanvas().refresh()
        no_feat_found_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                            "No map feature exists to zoom to.", QMessageBox.Ok, None)
        no_feat_found_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        no_feat_found_msg_box.exec_()

