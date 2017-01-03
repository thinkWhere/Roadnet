# -*- coding: utf-8 -*-
import os

from PyQt4.QtGui import QSortFilterProxyModel, QComboBox, QAbstractItemView, QMessageBox, QIcon, QPixmap
from PyQt4.QtSql import QSqlRelation, QSqlQuery
from PyQt4.QtCore import Qt
from PyQt4.Qt import Qt
from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest

from ..roadnet_dialog import QuickFindDlg

__author__ = 'matthew.walsh'


class PopulateFilterTableView:

    def __init__(self, parent, filter_dlg, db, model):
        self.parent = parent  # Parent is the street browser instance
        self.filter_dlg = filter_dlg
        self.db = db
        self.model = model
        self.table_view = self.filter_dlg.ui.resultsTableView
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.resizeColumnsToContents()
        self.plugin_dir = os.path.dirname(__file__)
        self.filter_dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        app_root = os.path.dirname(os.path.dirname(__file__))
        rn_icon = QIcon()
        rn_icon.addPixmap(QPixmap(os.path.join(app_root, "image", "rn_logo_v2.png")))
        self.filter_dlg.setWindowIcon(rn_icon)
        self.connect_filters()
        # Setup custom proxy
        self.proxy = MultiFilterProxyModel()  # Inherits QSortFilterProxyModel
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)
        self.table_view.setModel(self.proxy)
        # Only show required cols
        self.hide_columns()
        # Various setups for filtering
        self.set_header_data()
        self.relate_lookup_tables(self.model)
        self.populate_comboboxes()
        self.quick_find_dlg = None

        # Connect buttons
        self.filter_dlg.ui.gotoRecordPushButton.clicked.connect(lambda: self.goto_record(close=True))
        self.filter_dlg.ui.mapPushButton.clicked.connect(self.zoom_to_record)
        self.filter_dlg.ui.quickFindPushButton.clicked.connect(self.quick_find_show)

        self.update_filter_counter()

    def hide_columns(self):
        """
        Hides any unnecessary columns in the tableview
        """
        hide_cols = [0, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 21,
                     23, 24, 25, 26, 27, 28, 29]
        for column in hide_cols:
            self.table_view.hideColumn(column)

    def relate_lookup_tables(self, model):
        """
        Map to lookup tables
        :param model: model
        """
        model.setRelation(4, QSqlRelation("tlkpSTREET_REF_TYPE", "street_ref", "description"))
        model.setRelation(20, QSqlRelation("tlkpLOCALITY", "loc_ref", "name"))
        model.setRelation(22, QSqlRelation("tlkpTOWN", "town_ref", "name"))
        model.setRelation(17, QSqlRelation("tlkpSTREET_STATE", "state_ref", "state_desc"))

    def set_header_data(self):
        """
        Set header titles for qtableview model
        """
        self.model.setHeaderData(1, Qt.Horizontal, "USRN")
        self.model.setHeaderData(2, Qt.Horizontal, "Version")
        self.model.setHeaderData(4, Qt.Horizontal, "Street Type")
        self.model.setHeaderData(5, Qt.Horizontal, "Description")
        self.model.setHeaderData(20, Qt.Horizontal, "Locality")
        self.model.setHeaderData(22, Qt.Horizontal, "Town")
        self.model.setHeaderData(17, Qt.Horizontal, "State")

    def populate_comboboxes(self):
        """
        Populate comboboxes from db and add blank 0 index
        """
        ui_s = self.filter_dlg.ui
        query_lst = [("""SELECT name FROM tlkpTOWN
                         ORDER BY name DESC""", ui_s.townComboBox),
                     ("""SELECT state_desc FROM tlkpSTREET_STATE
                         ORDER BY state_desc DESC""", ui_s.stateComboBox),
                     ("""SELECT name FROM tlkpLOCALITY
                         ORDER BY name DESC""", ui_s.localityComboBox),
                     ("""SELECT description FROM tlkpSTREET_REF_TYPE
                         ORDER BY description DESC""", ui_s.recordTypeComboBox)]
        for query in query_lst:
            sql = query[0]
            combo = query[1]
            combo.clear()
            query = QSqlQuery(sql)
            while query.next():
                value = str(query.value(0))
                combo.insertItem(0, value)
            combo.insertItem(0, "")
            combo.setCurrentIndex(0)
            combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def zoom_to_record(self):
        """
        Zoom map to extent of street (comprising of multiple esu's)
        """
        tbl_idx = self.table_view.selectedIndexes()
        if tbl_idx:
            source_idx = self.proxy.mapToSource(tbl_idx[0])
            usrn = source_idx.data()
            # Query db for ESU's which make up the street
            if usrn and usrn != 0:
                query_str = "SELECT esu_id FROM lnkESU_STREET WHERE usrn = %s AND currency_flag = 0;" % usrn
                query = QSqlQuery(query_str, self.db)
                # Build query string
                q_string = ""
                while query.next():
                    q_string += '"esu_id" = %s OR ' % str(query.value(0))
                q_string = q_string[:-3]
                # Get ref to ESU layer
                esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
                # Select ESU's + get extent
                feats = esu_layer.getFeatures(QgsFeatureRequest().setFilterExpression(q_string))
                feat_ids = []
                for feature in feats:
                    f_id = feature.id()
                    feat_ids.append(f_id)
                esu_layer.setSelectedFeatures(feat_ids)
                esu_bbox = esu_layer.boundingBoxOfSelected()
                # Set new extent
                esu_bbox.scale(1.1)  # Zoom out slightly for context
                self.parent.iface.mapCanvas().setExtent(esu_bbox)
                self.parent.iface.mapCanvas().refresh()
                # Close connection to db and goto_record
                self.goto_record(close=False)

    def quick_find_show(self):
        """
        Show quick find dlg
        """
        self.quick_find_dlg = QuickFindDlg()
        self.quick_find_dlg.setParent(None)
        self.quick_find_dlg.ui.goPushButton.clicked.connect(self.go_quick_find)
        self.quick_find_dlg.exec_()

    def go_quick_find(self):
        """
        Jump to record based on known usrn
        """
        usrn_to_search = str(self.quick_find_dlg.ui.usrnLineEdit.text()).rstrip()
        row_count = self.model.rowCount()

        # Find matching row
        for counter in range(1, row_count + 1):
            idx = self.model.index(counter, 1)
            usrn = str(idx.data())
            if usrn_to_search == usrn:
                self.parent.goto_record(idx.row())
                self.quick_find_dlg.close()
                self.filter_dlg.close()
                return

        # Display error message if record not found
        no_usrn_msg_box = QMessageBox(QMessageBox.Warning, " ", "No USRN matching {}".format(usrn_to_search),
                                      QMessageBox.Ok, None)
        no_usrn_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        no_usrn_msg_box.exec_()

    def connect_filters(self):
        """
        Connect filters and clear button
        """
        self.filter_dlg.ui.townComboBox.activated['int'].connect(self.filter_layers)
        self.filter_dlg.ui.stateComboBox.activated['int'].connect(self.filter_layers)
        self.filter_dlg.ui.localityComboBox.activated['int'].connect(self.filter_layers)
        self.filter_dlg.ui.recordTypeComboBox.activated['int'].connect(self.filter_layers)
        self.filter_dlg.ui.descriptionLineEdit.textChanged.connect(self.filter_layers)
        self.filter_dlg.ui.clearPushButton.clicked.connect(self.clear_filter)

    def goto_record(self, close=False):
        """
        Map filtered record back to source, goto row and close filter dlg
        :param close: bool for close dlg
        """
        try:
            current_idx = self.table_view.selectedIndexes()
            source_idx = self.proxy.mapToSource(current_idx[0])
            source_row = source_idx.row()
            self.parent.goto_record(source_row)
            if close:
                self.filter_dlg.close()
        except IndexError:
            pass

    def filter_layers(self):
        """
        Create dict of filters and prompt to
        """
        self.filter_dlg.ui.totalSelectionLabel.setText("Filtering...")
        # Refs all combos + description lineedit
        town_combo = self.filter_dlg.ui.townComboBox
        state_combo = self.filter_dlg.ui.stateComboBox
        locality_combo = self.filter_dlg.ui.localityComboBox
        record_typ_combo = self.filter_dlg.ui.recordTypeComboBox
        description_lineedit = self.filter_dlg.ui.descriptionLineEdit
        # Get current index of comboboxes
        town_idx = town_combo.currentIndex()
        state_idx = state_combo.currentIndex()
        locality_idx = locality_combo.currentIndex()
        record_typ_idx = record_typ_combo.currentIndex()
        # Get text of the combo boxes + descripion lineedit
        town_txt = town_combo.itemText(town_idx)
        state_txt = state_combo.itemText(state_idx)
        locality_txt = locality_combo.itemText(locality_idx)
        record_typ_txt = record_typ_combo.itemText(record_typ_idx)
        description_txt = description_lineedit.text()
        filter_dict = {}
        # Add new filter to dict
        if town_txt:
            filter_dict[22] = town_txt
        if state_txt:
            filter_dict[17] = state_txt
        if locality_txt:
            filter_dict[20] = locality_txt
        if record_typ_txt:
            filter_dict[4] = record_typ_txt
        if description_txt:
            filter_dict[5] = description_txt
        # set filter dict to new dict
        self.proxy.filters = filter_dict
        # Dummy prompt the filter
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterFixedString('')
        # Update the selected rows counter
        self.update_filter_counter()
        # Select first row
        self.table_view.selectRow(0)

    def update_filter_counter(self):
        """
        Updates the counter which shows the number of rows in the filter selection
        """
        filter_row_count = str(self.proxy.rowCount())
        model_row_count = str(self.model.rowCount())
        self.filter_dlg.ui.totalSelectionLabel.setText(filter_row_count + " of " + model_row_count + " selected")

    def clear_filter(self):
        """
        Clear any filters on the source model
        """
        self.filter_dlg.ui.townComboBox.setCurrentIndex(0)
        self.filter_dlg.ui.stateComboBox.setCurrentIndex(0)
        self.filter_dlg.ui.localityComboBox.setCurrentIndex(0)
        self.filter_dlg.ui.recordTypeComboBox.setCurrentIndex(0)
        self.filter_dlg.ui.descriptionLineEdit.setText('')
        self.filter_layers()


class MultiFilterProxyModel(QSortFilterProxyModel):
    """Subclass to implement filtering multiple col filters against different values (multi combobox filter)"""
    def __init__(self, parent=None):
        super(MultiFilterProxyModel, self).__init__(parent)
        self.filters = {}  # column:SearchString

    def filterAcceptsRow(self, row_num, parent):
        """
        Each row in the source model is passed to this func, return True to accept the row.
        :rtype : bool
        :param row_num: row number
        """
        # Number of filters
        num_filters = len(self.filters)
        # Counter for successful filter
        filter_counter = 0
        # Only filter if we have to
        if self.filters:
            # Loop through items in dict and compare to value
            for col, search_str in self.filters.iteritems():
                # index of the cell to be filtered
                index = self.sourceModel().index(row_num, col, parent)
                # Text from the cell
                txt = unicode(index.data())
                # If description lineedit use find rather than equality
                if col == 5:
                    if txt.lower().find(search_str.lower()) != -1:
                        filter_counter += 1
                else:
                    # If text matches search then add to counter
                    if txt == search_str:
                        filter_counter += 1
            # All filters must pass to return the row
            if filter_counter == num_filters:
                return True
            else:
                return False
        else:
            return True
