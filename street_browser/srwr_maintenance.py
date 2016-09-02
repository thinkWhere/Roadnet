# -*- coding: utf-8 -*-
import datetime
import operator

from PyQt4.QtCore import Qt, QDate, QPyNullVariant, QObject, pyqtSignal
from PyQt4.QtGui import QStackedWidget, QMessageBox, QListWidgetItem
from PyQt4.QtSql import (
    QSqlRelationalTableModel,
    QSqlTableModel,
    QSqlRelation,
    QSqlQuery)
from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest

from Roadnet.roadnet_dialog import SrwrMaintDlg, SaveRecordDlg
from edit import EditStartEndCoords, EditEsuLink
from srwr import (
    SetupMaintRecordOperationsButtons,
    WidgetInfoObject,
    WidgetTypeEnum,
    SrwrViewRecord)
from Roadnet.generic_functions import ZoomSelectCanvas, ShowStreetCoordinates


class MaintenanceTable(object):
    """
    Populates and initial setup of SRWR maintenance tab
    """
    table = "tblMAINT"
    hide_cols = [0, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    whole_rd_col = 7
    currency_flag_col = 18
    usrn_col = 3
    start_end_coords_cols = [9, 10, 11, 12]

    def __init__(self, street_browser, usrn, db, tv, iface, params):
        self.street_browser = street_browser
        self.usrn = usrn
        self.db = db
        self.table_view = tv
        self.iface = iface
        self.params = params
        self.signals = MaintenanceTableSignals()
        self.model = self.setup_model()
        self.relate_lookup_tables(self.model)
        self.select()
        self.apply_model_to_view()
        self.hide_table_view_columns()
        self.header_font_size()
        self.connect_buttons()
        self.table_view.selectRow(0)
        SetupMaintRecordOperationsButtons(self.street_browser, self.model, self.whole_rd_col, self.params).setup()
        self.view_i = None
        self.add_i = None
        self.modify_i = None
        self.delete_i = None
        self.generic_functs = ZoomSelectCanvas(self.iface, self.street_browser, self.db)
        self.show_coords = None
        self.rdpoly_layer = None

        self.dlg = SrwrMaintDlg()

    def connect_buttons(self):
        """
        Connect buttons
        """
        self.street_browser.ui.srwrAddPushButton.clicked.connect(lambda: self.view_or_modify(add=True))
        self.street_browser.ui.srwrViewPushButton.clicked.connect(lambda: self.view_or_modify(view=True))
        self.street_browser.ui.srwrModifyPushButton.clicked.connect(lambda: self.view_or_modify(modify=True))
        self.street_browser.ui.srwrDeletePushButton.clicked.connect(lambda: self.view_or_modify(delete=True))
        self.street_browser.ui.srwrExtentPushButton.clicked.connect(self.show_srwr_extents)

    def show_srwr_extents(self):
        """
        Show or Hide the start/end coords of the current selected record
        """
        if self.street_browser.ui.srwrExtentPushButton.text() == "Show Extents":
            row = self.table_view.selectionModel().currentIndex().row()
            startx = self.model.data(self.model.index(row, self.start_end_coords_cols[0]), Qt.DisplayRole)
            starty = self.model.data(self.model.index(row, self.start_end_coords_cols[1]), Qt.DisplayRole)
            endx = self.model.data(self.model.index(row, self.start_end_coords_cols[2]), Qt.DisplayRole)
            endy = self.model.data(self.model.index(row, self.start_end_coords_cols[3]), Qt.DisplayRole)
            coords = ((startx, starty), (endx, endy))
            if self.show_coords:
                self.show_coords.remove()
            if startx and endy:
                self.show_coords = ShowStreetCoordinates(self.iface)
                self.show_coords.show(coords)
                self.street_browser.ui.srwrExtentPushButton.setText("Hide Extents")
        else:
            self.show_coords.remove()
            self.street_browser.ui.srwrExtentPushButton.setText("Show Extents")

    def disconnect_buttons(self):
        """
        Disconnect the tab operations buttons from all connected method
        """
        self.street_browser.ui.srwrAddPushButton.clicked.disconnect()
        self.street_browser.ui.srwrViewPushButton.clicked.disconnect()
        self.street_browser.ui.srwrModifyPushButton.clicked.disconnect()
        self.street_browser.ui.srwrDeletePushButton.clicked.disconnect()
        self.street_browser.ui.srwrExtentPushButton.clicked.disconnect()
        # Remove coords
        if self.show_coords:
            self.show_coords.remove()
            self.street_browser.ui.srwrExtentPushButton.setText("Show Extents")

    def view_or_modify(self, add=False, modify=False, delete=False, view=False):
        """
        Launch the Add, modify or view form
        :param add: bool option
        :param modify: bool option
        :param delete: bool option
        :param view: bool option
        """

        # Create fresh instance of maintenance dialog
        self.dlg = SrwrMaintDlg()

        widget_info = [WidgetInfoObject(self.dlg.ui.maintIdLineEdit, WidgetTypeEnum.lineedit, 1, id_col=True),
                       WidgetInfoObject(self.dlg.ui.versionLineEdit, WidgetTypeEnum.lineedit, 2),
                       WidgetInfoObject(self.dlg.ui.refLineEdit, WidgetTypeEnum.lineedit, 4),
                       WidgetInfoObject(self.dlg.ui.locationTextEdit, WidgetTypeEnum.textedit, 6, white=True),
                       WidgetInfoObject(self.dlg.ui.swaLineEdit, WidgetTypeEnum.lineedit, 5),
                       WidgetInfoObject(self.dlg.ui.roadStatLineEdit, WidgetTypeEnum.lineedit, 8),
                       WidgetInfoObject(self.dlg.ui.lorNoLineEdit, WidgetTypeEnum.lineedit, 19, white=True),
                       WidgetInfoObject(self.dlg.ui.routeLineEdit, WidgetTypeEnum.lineedit, 20, white=True),
                       WidgetInfoObject(self.dlg.ui.adoptLineEdit, WidgetTypeEnum.lineedit, 17, date_col=True),
                       WidgetInfoObject(self.dlg.ui.entryDateLineEdit, WidgetTypeEnum.lineedit, 13, date_col=True),
                       WidgetInfoObject(self.dlg.ui.byLineEdit, WidgetTypeEnum.lineedit, 14),
                       WidgetInfoObject(self.dlg.ui.notesTextEdit, WidgetTypeEnum.textedit, 21, white=True),
                       WidgetInfoObject(self.dlg.ui.startXLineEdit, WidgetTypeEnum.lineedit, 9),
                       WidgetInfoObject(self.dlg.ui.startYLineEdit, WidgetTypeEnum.lineedit, 10),
                       WidgetInfoObject(self.dlg.ui.endXLineEdit, WidgetTypeEnum.lineedit, 11),
                       WidgetInfoObject(self.dlg.ui.endYLineEdit, WidgetTypeEnum.lineedit, 12),
                       WidgetInfoObject(self.dlg.ui.swaComboBox, WidgetTypeEnum.combo, 5, mapped=False),
                       WidgetInfoObject(self.dlg.ui.roadStatComboBox, WidgetTypeEnum.combo, 8, mapped=False),
                       WidgetInfoObject(self.dlg.ui.adoptDateEdit, WidgetTypeEnum.dateedit, 17, mapped=False)]

        query_lst = {
            "SELECT description, swa_org_ref FROM tlkpORG": self.dlg.ui.swaComboBox,
            "SELECT description, road_status_ref FROM tlkpROAD_STATUS": self.dlg.ui.roadStatComboBox}

        idx = self.table_view.selectionModel().currentIndex()

        if add:
            if not self.check_layer_editing():
                self.add_i = SrwrAddMaintenanceRecord(self.model, self.iface, self.db, self.street_browser, self.dlg,
                                                  self.whole_rd_col, self.currency_flag_col, self.usrn_col, widget_info,
                                                  query_lst, self.params)
                self.add_i.view(idx, self.usrn)
                self.disable_sb_modifications()
                self.rdpoly_layer.setReadOnly(True)
        elif modify:
            if not self.check_layer_editing():
                self.modify_i = SrwrModifyMaintenanceRecord(self.model, self.iface, self.db, self.street_browser,
                                                            self.dlg, self.whole_rd_col, self.currency_flag_col,
                                                            self.usrn_col, widget_info, query_lst, self.params)
                self.modify_i.view(idx, self.usrn)
                self.disable_sb_modifications()
                self.rdpoly_layer.setReadOnly(True)
        elif delete:
            if not self.check_layer_editing():
                self.delete_i = SrwrDeleteMaintenanceRecord(self.street_browser, self.db, self.model, self.usrn,
                                                        self.table_view)
                self.delete_i.delete()
                # emit the signal that checks for linked usrns
                self.signals.current_usrn_links.emit(self.usrn)
        elif view:
            self.view_i = SrwrViewMaintenanceRecord(self.model, self.iface, self.street_browser,
                                                    self.dlg, self.whole_rd_col, widget_info,
                                                    self.db, self.params)
            self.view_i.view(idx, self.usrn)
        else:
            pass

    def check_layer_editing(self):
        """
        Checks if either the rd poly layer is currently in editing state.
        :return: True if editing
        """
        self.rdpoly_layer = QgsMapLayerRegistry.instance().mapLayersByName('Road Polygons')[0]
        if self.rdpoly_layer.isEditable():
            msg_box = QMessageBox(QMessageBox.Warning, '',
                                                       'Cannot modify a maintenance record while editing the Road '
                                                       'Polygon layer',
                                                   QMessageBox.Ok, None)
            msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            msg_box.exec_()
            return True
        else:
            return False

    def hide_table_view_columns(self):
        """
        Hide columns in the list from displaying in the table
        """
        for idx in self.hide_cols:
            self.table_view.setColumnHidden(idx, True)

    def setup_model(self):
        """
        Load the table into a model and set edit strategy
        :rtype : QSqlRelationalTableModel
        """
        model = QSqlRelationalTableModel(db=self.db)
        model.setTable(self.table)
        model.setFilter("currency_flag = 0 AND usrn = " + str(self.usrn))
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.setJoinMode(model.LeftJoin)
        return model

    def relate_lookup_tables(self, model):
        """
        Relate the lookup tables to the model data
        :param model: QSqlRelationalTableModel
        """
        model.setRelation(5, QSqlRelation("tlkpORG", "swa_org_ref", "description"))
        model.setHeaderData(5, Qt.Horizontal, "Organisation")
        model.setHeaderData(4, Qt.Horizontal, "Ref No")
        model.setRelation(8, QSqlRelation("tlkpROAD_STATUS", "road_status_ref", "description"))
        model.setHeaderData(8, Qt.Horizontal, "Road Status Ref")
        model.setRelation(7, QSqlRelation("tlkpWHOLE_ROAD", "whole_road", "description"))
        model.setHeaderData(7, Qt.Horizontal, "Whole Road")
        model.setHeaderData(3, Qt.Horizontal, "USRN")
        model.setHeaderData(6, Qt.Horizontal, "Location")
        model.setHeaderData(2, Qt.Horizontal, "Version")
        model.setHeaderData(1, Qt.Horizontal, "ID")

    def select(self, usrn=None):
        """
        Select the records for a street and select the first row
        :param usrn: usrn to filter on
        """
        if usrn:
            self.usrn = usrn
            self.model.setFilter("currency_flag = 0 AND usrn = " + str(self.usrn))
        # Make the selection
        self.model.select()
        # Get all rows from db into model
        while self.model.canFetchMore():
            self.model.fetchMore()
        SetupMaintRecordOperationsButtons(self.street_browser, self.model, self.whole_rd_col, self.params).setup()
        # Select first row
        self.street_browser.ui.maintTableView.selectRow(0)

    def get_model(self):
        """
        Return the populated model
        :return: data model
        """
        return self.model

    def apply_model_to_view(self):
        """
        Set the model to the table
        """
        self.table_view.setModel(self.model)

    def header_font_size(self):
        """
        Reduce the horizontal header font size from the default.
        """
        font = self.table_view.horizontalHeader().font()
        font.setPointSize(8)
        self.table_view.horizontalHeader().setFont(font)

    def disable_sb_modifications(self):
        """
        Disable option to modify street records
        """
        self.street_browser.ui.addPushButton.setEnabled(False)
        self.street_browser.ui.modifyPushButton.setEnabled(False)
        self.street_browser.ui.closeOpPushButton.setEnabled(False)


class MaintenanceTableSignals(QObject):
    """
    Class holding signals for srwr maintenance table
    """
    current_usrn_links = pyqtSignal(str)


class SrwrViewMaintenanceRecord(SrwrViewRecord):
    """
    Extents the view record class to display a list widget of linked road polygons.
    """

    def __init__(self, model, iface, street_browser, dialog, whole_rd_col, widget_info, db, params):
        super(SrwrViewMaintenanceRecord, self).__init__(model, iface, dialog, whole_rd_col, widget_info, params)
        self.iface = iface
        self.street_browser = street_browser
        self.db = db
        self.zoom_select_canvas = ZoomSelectCanvas(iface, self.street_browser, self.db)
        self.rd_poly_ids = []

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
        self.populate_rdpoly_list()
        self.hide_buttons()
        self.view_dlg.show()

    def populate_rdpoly_list(self):
        """
        Populates the road polygon list.
        """
        sql = "SELECT rd_pol_id FROM lnkMAINT_RD_POL WHERE maint_id = %s and currency_flag = 0" % \
              (self.view_dlg.ui.maintIdLineEdit.text())
        query = QSqlQuery(sql, self.db)
        while query.next():
            rd_pol = query.value(0)
            QListWidgetItem(str(rd_pol), self.view_dlg.ui.rdPolyListWidget)
            self.rd_poly_ids.append(rd_pol)

    def zoom_to_map(self):
        """
        Zoom to the selected maintenance record polygons and selects them
        :return: void
        """
        feats = self.zoom_select_canvas.get_features_from_field_value(self.rd_poly_ids, 'rd_pol_id', 'Road Polygons')
        bbox = self.zoom_select_canvas.select_features(feats, 'Road Polygons')
        self.zoom_select_canvas.zoom_to_extent(bbox)


class SrwrAddMaintenanceRecord(SrwrViewRecord):
    """
    Builds on functionality of SrwrViewRecord. Allows user to add a new maintenance record to a street. This also
    includes all the methods to deal with opening and closing links to polygons.
    """
    usrn_col = int()
    currency_flag_col = int()

    def __init__(self, model, iface, db, street_browser, dlg, whole_rd_col, cur_flag_col, usrn_col, widget_info,
                 query_lst, params):
        """
        Initialise for adding a new record.
        :param model: Model
        :param iface: qgis iface hook
        :param db: database connection
        :param street_browser: street browser instance
        :param dlg: dialog instance
        :param whole_rd_col: int whole road column
        :param cur_flag_col: int currency flag col
        :param usrn_col: int usrn column
        :param widget_info: list of WidgetInfoObjects
        :param query_lst: list of queries for lookups
        """
        super(SrwrAddMaintenanceRecord, self).__init__(model, iface, dlg, whole_rd_col, widget_info, params)
        self.db = db
        self.street_browser = street_browser

        self.currency_flag_col = cur_flag_col
        self.usrn_col = usrn_col
        self.query_lst = query_lst

        self.params = params
        self.rdpoly_layer = QgsMapLayerRegistry.instance().mapLayersByName('Road Polygons')[0]

        self.links = None
        self.usrn = None

        # Connect buttons to edit links/start-end coords
        self.view_dlg.ui.editCoordsPushButton.clicked.connect(self.edit_coords)
        self.view_dlg.ui.editLinkPushButton.clicked.connect(self.edit_links)

        self.save_dlg = SaveRecordDlg()
        self.save_dlg.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.save_dlg.ui.savePushButton.clicked.connect(self.save_record_changes)
        self.save_dlg.ui.revertPushButton.clicked.connect(self.revert_maint)
        self.save_dlg.ui.cancelPushButton.clicked.connect(lambda: self.save_dlg.close())
        self.connect_widgets_validation()

        # All road poly ID's for symbology updates
        self.rd_pol_links = None

    def connect_widgets_validation(self):
        """
        Connect signals on widgets to update the validation requirements
        """
        self.view_dlg.ui.wholeRoadCheckBox.stateChanged.connect(self.whole_rd_state)
        self.view_dlg.ui.locationTextEdit.textChanged.connect(self.location_text_changed)
        # Signals for validation label colour changes
        try:
            self.view_dlg.ui.swaComboBox.currentIndexChanged.connect(self.swa_idx_changed)
        except AttributeError:
            # Reinstatement cat has no SWA field
            pass

    def location_text_changed(self):
        """
        Change the location field label colour if validation passes/fails
        """
        loc_textedit = self.view_dlg.ui.locationTextEdit
        loc_len = len(loc_textedit.toPlainText())
        if loc_len > 0:
            self.view_dlg.ui.locationLabel.setStyleSheet("color : black")
        else:
            self.view_dlg.ui.locationLabel.setStyleSheet("color : red")

    def swa_idx_changed(self, idx):
        """
        Change the swa field label
        :param idx: index of selected column
        """
        if idx != 0:
            self.view_dlg.ui.swaLabel.setStyleSheet("color : black")
        else:
            self.view_dlg.ui.swaLabel.setStyleSheet("color : red")

    def whole_rd_state(self, state):
        """
        Toggle associated behaviour of the whole road checkbox. e.g disable textedit, set coords to same as street.
        :param state: The state of the checkbox, 2=checked, 0=unchecked
        """
        if state == 2:
            self.view_dlg.ui.locationTextEdit.setPlainText("Whole road")
            self.view_dlg.ui.locationTextEdit.setEnabled(False)
            self.view_dlg.ui.editCoordsPushButton.setEnabled(False)
            self.set_whole_rd_coords()
        else:
            self.view_dlg.ui.locationTextEdit.setEnabled(True)
            self.view_dlg.ui.editCoordsPushButton.setEnabled(True)
            self.view_dlg.ui.locationTextEdit.setPlainText("")
            self.clear_coords()

    def clear_coords(self):
        """
        Clears all the coords lineedits
        """
        self.view_dlg.ui.startXLineEdit.setText("")
        self.view_dlg.ui.startYLineEdit.setText("")
        self.view_dlg.ui.endXLineEdit.setText("")
        self.view_dlg.ui.endYLineEdit.setText("")

    def set_whole_rd_coords(self):
        """
        Sets the maint record coords to the same as the whole rd (ie street record)
        """
        start_x = self.street_browser.ui.startXLineEdit.text()
        start_y = self.street_browser.ui.startYLineEdit.text()
        end_x = self.street_browser.ui.endXLineEdit.text()
        end_y = self.street_browser.ui.endYLineEdit.text()
        self.view_dlg.ui.startXLineEdit.setText(start_x)
        self.view_dlg.ui.startYLineEdit.setText(start_y)
        self.view_dlg.ui.endXLineEdit.setText(end_x)
        self.view_dlg.ui.endYLineEdit.setText(end_y)

    def populate_combos(self):
        """
        Populate all comboboxes from db lookup tables. Combos sorted alphabetically with a 0 (default None) value at
        the top.
        """
        for query_str, combo in self.query_lst.iteritems():
            query = QSqlQuery(query_str)
            all_items = {}
            while query.next():
                text = str(query.value(0))
                value = str(query.value(1))
                all_items[text] = value
            sorted_items = sorted(all_items.iteritems(), key=operator.itemgetter(0), reverse=True)
            default_none = None
            for item in sorted_items:
                text = item[0]
                data = item[1]
                if int(data) != 0:
                    combo.insertItem(0, text, userData=data)
                else:
                    default_none = item
            if default_none:
                combo.insertItem(0, default_none[0], userData=default_none[1])
            else:
                combo.insertItem(0, "")
            combo.setCurrentIndex(0)

    def entry_date_default(self):
        """
        Sets the default entry date to the current date.
        """
        now_date = datetime.datetime.now()
        now_formatted = now_date.strftime("%d/%m/%Y")
        self.view_dlg.ui.entryDateLineEdit.setText(str(now_formatted))

    def generate_ids(self, max_id_query, max_ref_query, db):
        """
        Calculate the new maint id, ref and default version number, then set in the form.
        :param max_id_query: query string for max ID
        :param max_ref_query: query string for max ref
        :param db: database connection
        """
        # ID = max ID + 1
        id_query = QSqlQuery(max_id_query, db)
        id_query.seek(0)
        try:
            maint_id = int(id_query.value(0)) + 1
        except TypeError:
            maint_id = 1
        # Reference no = max ref + 1 (regardless of currency flag)
        max_ref_query = max_ref_query + self.street_browser.ui.usrnLineEdit.text()
        ref_query = QSqlQuery(max_ref_query, db)
        ref_query.seek(0)
        ref = ref_query.value(0)
        if type(ref) != QPyNullVariant:
            ref_value = int(ref) + 1
        else:
            ref_value = 1
        # Set values in gui
        self.id_lineedit.setText(str(maint_id))
        self.view_dlg.ui.refLineEdit.setText(str(ref_value))
        self.view_dlg.ui.versionLineEdit.setText(str(1))

    def view(self, idx, usrn):
        """
        Extends the default view behaviour for adding records.
        :param idx: model index
        :param usrn: current usrn
        """
        self.style_lineedits()
        self.enable_btns()
        self.switch_stacked()
        self.set_username()
        self.populate_combos()
        self.set_mandatory_fields()
        id_query = "SELECT MAX(maint_id) FROM tblMAINT"
        ref_query = "SELECT MAX(reference_no) FROM tblMAINT WHERE usrn = "
        self.generate_ids(id_query, ref_query, self.db)
        self.entry_date_default()
        self.usrn = usrn
        self.view_dlg.show()

    def set_username(self):
        """
        Sets the 'created by' lineedit value to the current user.
        """
        username = str(self.params['UserName'])
        self.view_dlg.ui.byLineEdit.setText(username)

    def enable_btns(self):
        """
        enable the edit links and edit coords push buttons for editing
        """
        self.view_dlg.ui.editCoordsPushButton.setEnabled(True)
        self.view_dlg.ui.editLinkPushButton.setEnabled(True)
        self.view_dlg.ui.closePushButton.setText("Complete")

    def set_mandatory_fields(self):
        """
        Set the stylesheet for the mandatory fields (red labels)
        """
        self.view_dlg.ui.swaLabel.setStyleSheet("color : red")
        self.view_dlg.ui.locationLabel.setStyleSheet("color : red")

    def switch_stacked(self):
        """
        Switch all stacked widgets
        """
        all_stackedwidgets = self.view_dlg.findChildren(QStackedWidget)
        for stacked in all_stackedwidgets:
            stacked.setCurrentIndex(1)

    def style_lineedits(self):
        """
        Set lineedits to white/editable
        """
        for w in self.widgets:
            if w.white:
                w.widget.setStyleSheet("background-color: white")
                w.widget.setReadOnly(False)

    def edit_coords(self):
        """
        Edit the start/end coords.
        """
        coord_le = {"start_xref": self.view_dlg.ui.startXLineEdit,
                    "start_yref": self.view_dlg.ui.startYLineEdit,
                    "end_xref": self.view_dlg.ui.endXLineEdit,
                    "end_yref": self.view_dlg.ui.endYLineEdit}
        button = self.view_dlg.ui.editCoordsPushButton
        coords = EditStartEndCoords(self.iface, coord_le, self.model, self.mapper, button, edit=False)
        coords.show()

    def edit_links(self):
        """
        Edit which polygons are attached to a maintenance record. Passes in any links from the edit session.
        """
        button = self.view_dlg.ui.editLinkPushButton
        layer = 'Road Polygons'
        dis_attr = 'rd_pol_id'
        if self.links:
            pre_unsaved = self.links.get_final_selection()[0]
            self.links = EditMaintLink(self.iface, button, self.db, layer_name=layer, unsaved=pre_unsaved,
                                       dis_attr=dis_attr, view_dlg=self.view_dlg)
        else:
            self.links = EditMaintLink(self.iface, button, self.db, layer_name=layer, dis_attr=dis_attr,
                                       view_dlg=self.view_dlg)
        self.links.show()

    def complete(self):
        """
        Show the save dialog, this takes over the save/revert process
        """
        self.save_dlg.exec_()

    def create_rd_poly_links(self, maint_id):
        """
        Create road polygon links to a maintenance record, if they don't already exist (not versioned like esu links)
        :param maint_id: maintenance record ID
        """
        if self.links:
            # rd poly links have been edited
            final_sel = self.links.get_final_selection()[0]
            # Find existing links
            existing = self.existing_rd_poly_links(maint_id)
            for rd_poly in final_sel:
                # Check if the link already exists
                # existing = self.check_existing_link(rd_poly, maint_id)
                if rd_poly not in existing:
                    # Create the link if it doesnt exist already
                    sql = "INSERT INTO lnkMAINT_RD_POL (rd_pol_id, currency_flag, maint_id) VALUES (%s, 0, %s)" % \
                          (rd_poly, maint_id)
                    insert_q = QSqlQuery(sql, self.db)

    def existing_rd_poly_links(self, maint_id):
        """
        Gets all the road polygons (id) associated with a maintenance record (live records only)
        :rtype : list
        :param maint_id: maintenance id
        """
        sql = "SELECT rd_pol_id FROM lnkMAINT_RD_POL WHERE maint_id = %s AND currency_flag = 0" % maint_id
        rd_polys = []
        query = QSqlQuery(sql, self.db)
        while query.next():
            rd_polys.append(query.value(0))
        return rd_polys

    def save_record_changes(self):
        """
        Validate the changes, update rd poly links and create a new record in the model.
        """
        self.rdpoly_layer.setReadOnly(False)
        self.revert_sb_modify_buttons()
        self.save_dlg.close()
        maint_id = self.id_lineedit.text()
        valid_loc = self.validate_location_mandatory()
        valid_swa = self.validate_swa_mandatory()
        valid_whole_rd = self.validate_existing_maint_records()
        valid_maint_links = self.validate_poly_maint_links(maint_id)
        if valid_loc and valid_swa and valid_whole_rd:
            self.create_rd_poly_links(maint_id)
            self.update_rdpoly_symbology(maint_id)
            self.view_dlg.close()
            # Create new record
            self.update_model()
            # Commit to db + insert any esu links
            self.model.submitAll()
            # Select the new record in the tableview
            last_row = int(self.model.rowCount())
            self.street_browser.ui.maintTableView.selectRow(last_row - 1)
        else:
            kwargs = {'swa': valid_swa, 'location': valid_loc, 'whole_rd': valid_whole_rd}
            self.validation_failed_messages(**kwargs)

    def revert_sb_modify_buttons(self):
        """
        Re-enable the street browser add/modify buttons, also delete if no SRWR records exist.
        :return:
        """
        maint_rc = self.street_browser.ui.maintTableView.rowAt(0)
        spec_des_rc = self.street_browser.ui.specDesTableView.rowAt(0)
        reins_cat_rc = self.street_browser.ui.reinstCatTableView.rowAt(0)
        total = maint_rc + spec_des_rc + reins_cat_rc
        if total < 0:
            del_bool = False
        else:
            del_bool = True
        self.street_browser.ui.closeOpPushButton.setEnabled(del_bool)
        self.street_browser.ui.addPushButton.setEnabled(True)
        self.street_browser.ui.modifyPushButton.setEnabled(True)

    def update_rdpoly_symbology(self, maint_id):
        """
        Updates the symbology of the current streets rdpoly links based on the value of the maint record road status.
        If the rdpoly feature is attached to multiple maint records then a warning is displayed and special symbology
        applied.
        :param maint_id: Maintenance record ID
        """
        if self.links:
            esu_selection = self.links.get_final_selection()
            final_sel = esu_selection[0]
            orig_sel = esu_selection[1]
            # Create distinct list of all rdpolys (added/existing links and those removed/unlinked)
            rd_pol_ids = final_sel + list(set(orig_sel) - set(final_sel))
        else:
            rd_pol_ids = self.existing_rd_poly_links(maint_id)
        cur_idx = self.view_dlg.ui.roadStatComboBox.currentIndex()
        # Build symbology value (+10 unless unassigned, multiple or default)
        record_symbology = int(self.view_dlg.ui.roadStatComboBox.itemData(cur_idx))
        # '<none>' values is hard coded to unassigned
        if record_symbology == 0:
            record_symbology = 1
        else:
            record_symbology = record_symbology + 10
        # Check no other records are attached to the same rd
        multi_rdpolys = []
        for rd_poly in rd_pol_ids:
            sql = "SELECT maint_id FROM lnkMAINT_RD_POL WHERE (rd_pol_id = %s) AND (currency_flag = 0)" % rd_poly
            query = QSqlQuery(sql, self.db)
            size = 0
            while query.next():
                size += 1
            query.seek(0)
            if size == 0:
                # No records attached to rdpoly (unlinked from this record)
                symbology = 1
            elif size == 1:
                if int(query.value(0)) == int(maint_id):
                    # Only attached to this record so update symbology with type
                    symbology = record_symbology
                else:
                    # Unlink of previously invalid
                    sql_old_invalid = "SELECT road_status_ref FROM tblMAINT WHERE maint_id = %s" % str(query.value(0))
                    query_invalid_old = QSqlQuery(sql_old_invalid, self.db)
                    query_invalid_old.seek(0)
                    road_stat_ref = query_invalid_old.value(0)
                    road_stat_ref += 10
                    symbology = road_stat_ref
            else:
                # More than one other record attached
                symbology = 2  # 2 = multiple
                multi_rdpolys.append(rd_poly)
            self.set_rdpoly_attribute(rd_poly, symbology, 1)
        if multi_rdpolys:
            message = "The following road polygons are linked to multiple maintenance records:\n"
            message += ", ".join(str(x) for x in multi_rdpolys)
            links_msg = QMessageBox(QMessageBox.Warning, "", message, QMessageBox.Ok, None)
            links_msg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            links_msg.exec_()
        self.iface.mapCanvas().refresh()

    def set_rdpoly_attribute(self, rdpoly_id, value, field):
        """
        Set the attribute field of a road polygon feature.
        :param rdpoly_id: rdpoly to update
        :param value: value to set
        :param field: field index
        """
        filter_ = '"rd_pol_id" = %s' % rdpoly_id
        feat = self.rdpoly_layer.getFeatures(QgsFeatureRequest().setFilterExpression(filter_)).next()
        fid = feat.id()
        self.rdpoly_layer.dataProvider().changeAttributeValues({fid: {field: value}})

    def validation_failed_messages(self, **kwargs):
        """
        Build error message for failed validation
        :param kwargs: All validation results
        """
        message = ""
        if 'whole_rd' in kwargs:
            if not kwargs['whole_rd']:
                message += 'Record Cannot be whole road. Other maintenance records already exist for this street.\n'
        if 'swa' in kwargs:
            if not kwargs['swa']:
                message += "SWA field is mandatory.\n"
        if 'location' in kwargs:
            if not kwargs['location']:
                message += "Location field is mandatory.\n"
        if 'designation' in kwargs:
            if not kwargs['designation']:
                message += 'Designation field is mandatory.\n'
        if 'desc' in kwargs:
            if not kwargs['desc']:
                message += "Description field is mandatory.\n"
        if 'des_date' in kwargs:
            if not kwargs['des_date']:
                message += "Date field is mandatory.\n"
        if 'category' in kwargs:
            if not kwargs['category']:
                message += "Another record with the selected category already applies to the whole road.\n"
        val_fail_msg_box = QMessageBox(QMessageBox.Warning, "", message, QMessageBox.Ok, None)
        val_fail_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        val_fail_msg_box.exec_()

    def update_model(self):
        """
        Create a new record in the model and set the values.
        """
        record = self.model.record()
        # Set usrn
        record.setValue(self.usrn_col, self.usrn)
        # Set currency flag
        record.setValue(self.currency_flag_col, str(0))
        # Set whole road
        whole_road = str(0)
        if self.view_dlg.ui.wholeRoadCheckBox.isChecked():
            whole_road = str(1)
        record.setValue(self.whole_road_col, whole_road)
        # Loop through all the widgets set the data accordingly
        for w in self.widgets:
            data = None
            # Entry date
            if w.widget_type == WidgetTypeEnum.lineedit:
                if w.date_col:
                    date_f = self.display_date_to_db(w.widget.text())
                    # Don't store date if its the default
                    if date_f != '20000101' or date_f is not None:
                        data = date_f
                else:
                    # All standard editable lineedits
                    data = w.widget.text()
            # Combo fields
            elif w.widget_type == WidgetTypeEnum.combo:
                cur_idx = w.widget.currentIndex()
                data = w.widget.itemData(cur_idx)
            # Textedit fields
            elif w.widget_type == WidgetTypeEnum.textedit:
                data = w.widget.toPlainText()
            # Date edits
            elif w.widget_type == WidgetTypeEnum.dateedit:
                dateedit_date = w.widget.text()
                db_date = self.display_date_to_db(dateedit_date)
                if db_date != '20000101':
                    data = db_date
            else:
                pass
            if data:
                record.setValue(w.db_col, data)
        # Add the record to the end of the model
        self.model.insertRecord(-1, record)
        SetupMaintRecordOperationsButtons(self.street_browser, self.model, self.whole_road_col, self.params).setup()

    def display_date_to_db(self, disp_date):
        """
        Change date from datepicker format to db friendly format (yyyymmdd)
        :rtype : string
        :param disp_date: date to change
        :return : formatted date
        """
        try:
            date_obj = datetime.datetime.strptime(disp_date, "%d/%m/%Y")
            data = str(date_obj.strftime("%Y%m%d"))
        except ValueError:
            return None
        return data

    def revert_maint(self):
        """
        close both the save dlg and the view dlg on a revert event
        """
        self.rdpoly_layer.setReadOnly(False)
        self.revert_sb_modify_buttons()
        self.save_dlg.close()
        self.view_dlg.close()

    def validate_existing_maint_records(self):
        """
        If the record is whole road then check no other maint records are attached to the street.
        :return: True if validation passes
        """
        whole_rd = self.view_dlg.ui.wholeRoadCheckBox.isChecked()
        row_count = self.model.rowCount()
        if whole_rd:
            if row_count == 0:
                # Must first record
                return True
            elif row_count == 1:
                # Check if it was a modification of an existing record
                maint_id_tbl = str(self.model.data(self.model.index(0, 1), Qt.DisplayRole))
                maint_id_dlg = str(self.view_dlg.ui.maintIdLineEdit.text())
                if maint_id_tbl == maint_id_dlg:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def validate_location_mandatory(self):
        """
        Checks that all mandatory fields are populated
        :rtype : bool
        :return True if all passed validation
        """
        self.view_dlg.ui.locationTextEdit.toPlainText()
        loc_text = str(self.view_dlg.ui.locationTextEdit.toPlainText())
        if len(loc_text) == 0:
            return False
        else:
            return True

    def validate_swa_mandatory(self):
        """
        Checks if a SWA has been selected for the record
        :return: true a SWA has been selected in the drop down list.
        """
        if self.view_dlg.ui.swaComboBox.currentIndex() == 0:
            return False
        else:
            return True

    def validate_poly_maint_links(self, maint_id):
        """
        Checks if a rd polygon is attached to any other maint records
        :param maint_id: ID to exclude
        :return: True if valid, i.e. no links are associated with other maint records
        """
        if self.links:
            final = self.links.get_final_selection()[0]
            rd_pol_clause = str()
            for rd_pol_id in final:
                rd_pol_clause += "rd_pol_id = " + str(rd_pol_id) + " OR "
            rd_pol_clause = rd_pol_clause[:-3]
            sql = "SELECT maint_id FROM lnkMAINT_RD_POL WHERE (%s) AND (maint_id != %s) AND (currency_flag = 0)" % \
                  (rd_pol_clause, maint_id)
            query = QSqlQuery(sql, self.db)
            all_rd_pol_ids = []
            query.seek(0)
            while query.next():
                all_rd_pol_ids.append(query.value(0))
            # Make distinct and set as class var
            self.rd_pol_links = list(set(all_rd_pol_ids))
            if len(all_rd_pol_ids) > 0:
                return False
            else:
                return True
        else:
            return True


class SrwrModifyMaintenanceRecord(SrwrAddMaintenanceRecord):
    """
    Builds on functionality of SrwrAddMaintenanceRecord. Adds methods to populate the form with a existing record and
    the updates existing records rather than creating new.
    """

    def __init__(self, model, iface, db, street_browser, dlg, whole_rd_col, cur_flag_col, usrn_col, widget_info,
                 query_lst, params):
        """
        Adds some extra class variables ontop of the SrwrAddMaintenanceRecord init.
        :param model: Model
        :param iface: qgis iface hook
        :param db: database connection
        :param street_browser: street browser
        :param dlg: dialog
        :param whole_rd_col: whole road column
        :param cur_flag_col: currency flag column
        :param usrn_col: usrn column
        :param widget_info: list of WidgetInfoObjects
        :param query_lst: list of queries for lookups
        """
        super(SrwrModifyMaintenanceRecord, self).__init__(model, iface, db, street_browser, dlg, whole_rd_col,
                                                          cur_flag_col, usrn_col, widget_info, query_lst, params)
        self.pre_edit_row = int()
        self.iface = iface
        self.street_browser = street_browser
        self.db = db

        # Snapshot of record values before edits are made
        self.before_mod_values = None

        # list containing polygon ids linked to maint record
        self.rd_poly_ids = []

        # instance of generic functions class for zoom/select polygons
        self.zoom_select_canvas = ZoomSelectCanvas(self.iface, self.street_browser, self.db)

    def view(self, idx, usrn):
        """
        Overrides base method to deal with a modification.
        :param idx: current record model index
        :param usrn: USRN of modified record link
        """
        row = idx.row()
        self.pre_edit_row = row

        self.style_lineedits()
        self.enable_btns()
        self.switch_stacked()
        self.populate_combos()
        self.set_mandatory_fields()

        self.mapper.setCurrentIndex(row)
        self.populate_rdpoly_list()
        self.set_initial_values()
        self.entry_date_default()
        self.whole_road_checkbox(row)
        self.update_version_number()
        # After initial setup take a snapshot of values
        self.before_mod_values = self.snapshot_record_values()
        self.usrn = usrn
        self.view_dlg.show()

    def update_version_number(self):
        """
        Increment the current version number by 1 and set in the form.
        """
        version_plus_one = int(self.view_dlg.ui.versionLineEdit.text()) + 1
        self.view_dlg.ui.versionLineEdit.setText(str(version_plus_one))

    def populate_rdpoly_list(self):
        """
        Populates the road polygon list.
        """
        maint_id = self.view_dlg.ui.maintIdLineEdit.text()
        sql = "SELECT rd_pol_id FROM lnkMAINT_RD_POL WHERE maint_id = %s AND currency_flag = 0" % maint_id
        query = QSqlQuery(sql, self.db)
        while query.next():
            rd_pol = query.value(0)
            QListWidgetItem(str(rd_pol), self.view_dlg.ui.rdPolyListWidget)
            self.rd_poly_ids.append(rd_pol)

    def snapshot_record_values(self):
        """
        Creates a snapshot of the current record.
        :rtype : dict
        :return: dict - key = table idx, value = text value
        """
        cur_dict = {}
        for w in self.widgets:
            if w.widget_type == WidgetTypeEnum.lineedit:
                text = w.widget.text().rstrip()
                cur_dict[w.db_col] = text
            elif w.widget_type == WidgetTypeEnum.textedit:
                text = w.widget.toPlainText().rstrip()
                cur_dict[w.db_col] = text
            elif w.widget_type == WidgetTypeEnum.combo:
                text = w.widget.currentText().rstrip()
                cur_dict[w.db_col] = text
        return cur_dict

    def entry_date_default(self):
        """
        Set the datepicker date from the lineedit value, if no date present then use default (01/01/2001).
        Overrides method in base class.
        """
        for w in self.widgets:
            if w.date_col:
                if str(w.widget.text()):
                    date = datetime.datetime.strptime(w.widget.text(), "%d/%m/%Y")
                    date_obj = QDate(date.year, date.month, date.day)
                    # self.view_dlg.ui.adoptDateEdit.setDate(date_obj)
                    for w_1 in self.widgets:
                        if (w_1.widget_type == WidgetTypeEnum.dateedit) and (w.db_col == w_1.db_col):
                            w_1.widget.setDate(date_obj)
                else:
                    for w_2 in self.widgets:
                        if w_2.widget_type == WidgetTypeEnum.dateedit and w.db_col == w_2.db_col:
                            w_2.widget.setDate(QDate(00, 01, 01))

    def close_rd_poly_links(self, maint_id):
        """
        Close any road polygon links which have been removed from the picker
        :param maint_id: Maintenance record ID
        """
        if self.links:
            org_sel = self.links.get_final_selection()[1]
            final_sel = self.links.get_final_selection()[0]
            for org_rd_poly in org_sel:
                if org_rd_poly not in final_sel:
                    sql = "UPDATE lnkMAINT_RD_POL SET currency_flag=1 WHERE rd_pol_id = %s AND maint_id = %s" % \
                          (org_rd_poly, maint_id)
                    query = QSqlQuery(sql, self.db)

    def save_record_changes(self):
        """
        Create record and add to model if validation is passed.
        """
        self.rdpoly_layer.setReadOnly(False)
        self.revert_sb_modify_buttons()
        maint_id = self.id_lineedit.text()
        self.save_dlg.close()
        valid_loc = self.validate_location_mandatory()
        valid_swa = self.validate_swa_mandatory()
        valid_whole_rd = self.validate_existing_maint_records()
        valid_maint_links = self.validate_poly_maint_links(maint_id)
        if valid_loc and valid_swa and valid_whole_rd:
            # Update of links doesnt require version change
            self.create_rd_poly_links(maint_id)
            # Close any links removed
            self.close_rd_poly_links(maint_id)
            self.update_rdpoly_symbology(maint_id)
            dirty = self.is_record_dirty()
            if dirty:
                self.update_model()
                self.model.submitAll()
            # Reselect the same row
            self.street_browser.ui.maintTableView.selectRow(self.pre_edit_row)
            self.view_dlg.close()
        else:
            kwargs = {'swa': valid_swa, 'location': valid_loc, 'whole_rd': valid_whole_rd}
            self.validation_failed_messages(**kwargs)

    def update_model(self):
        """
        Sets the data in the model to the values in the dialog
        """
        current = self.mapper.currentIndex()
        # Increment the version number
        version_col = 2
        self.model.setData(self.model.createIndex(current, version_col), self.view_dlg.ui.versionLineEdit.text())
        # Set whole road
        whole_road = str(0)
        if self.view_dlg.ui.wholeRoadCheckBox.isChecked():
            whole_road = str(1)
        self.model.setData(self.model.createIndex(current, self.whole_road_col), whole_road)
        # Loop through all the widgets set the data accordingly
        for w in self.widgets:
            data = None
            # Entry date
            if w.widget_type == WidgetTypeEnum.lineedit:
                if w.date_col:
                    date_f = self.display_date_to_db(w.widget.text())
                    # Don't store date if its the default
                    if date_f != '20000101' or date_f is not None:
                        data = date_f
                else:
                    # All standard editable lineedits
                    data = w.widget.text()
            # Combo fields
            elif w.widget_type == WidgetTypeEnum.combo:
                cur_idx = w.widget.currentIndex()
                data = w.widget.itemData(cur_idx)
            # Textedit fields
            elif w.widget_type == WidgetTypeEnum.textedit:
                data = w.widget.toPlainText()
            # Date edits
            elif w.widget_type == WidgetTypeEnum.dateedit:
                dateedit_date = w.widget.text()
                db_date = self.display_date_to_db(dateedit_date)
                if db_date != '20000101':
                    data = db_date
            else:
                pass
            if data:
                self.model.setData(self.model.createIndex(current, w.db_col), data)
        SetupMaintRecordOperationsButtons(self.street_browser, self.model, self.whole_road_col, self.params).setup()

    def is_record_dirty(self):
        """
        Check if any edits have been made by comparing snapshot of data from before edit session started
        :rtype : bool
        :return : True if record is dirty
        """
        new_values = self.snapshot_record_values()
        for idx, org_value in self.before_mod_values.iteritems():
            if org_value != new_values[idx]:
                return True
        adopt_new = self.view_dlg.ui.adoptDateEdit.text()
        adopt_old = self.view_dlg.ui.adoptLineEdit.text()
        if adopt_new != adopt_old:
            # Default date in datepicker would equal empty string in lineedit
            if adopt_new != "01/01/2000":
                return True
        return False

    def set_initial_values(self):
        """
        Overrides the base class method to set the combo values, all others are set by the mapper
        """
        for w in self.widgets:
            if w.widget_type == WidgetTypeEnum.combo:
                for w_1 in self.widgets:
                    if w_1.widget_type == WidgetTypeEnum.lineedit and w.db_col == w_1.db_col:
                        current_txt = w_1.widget.text()
                        idx = w.widget.findText(current_txt)
                        w.widget.setCurrentIndex(idx)

    def zoom_to_map(self):
        """
        Zoom to the selected maintenance record polygons and selects them
        :return: void
        """
        feats = self.zoom_select_canvas.get_features_from_field_value(self.rd_poly_ids, 'rd_pol_id', 'Road Polygons')
        bbox = self.zoom_select_canvas.select_features(feats, 'Road Polygons')
        self.zoom_select_canvas.zoom_to_extent(bbox)


class EditMaintLink(EditEsuLink):
    """
    Inherits EditEsuLink. Makes gui changes and changes initial population method.
    """

    def __init__(self, iface, button, db, **kwargs):
        super(EditMaintLink, self).__init__(iface, button, db, **kwargs)
        self.esu_dlg.ui.usrnLabel.setText("")
        self.esu_dlg.ui.label.setText("Modify the selection on the map canvas to add/remove Road Polygons.")
        self.esu_dlg.setWindowTitle("Edit Road Polygon Maintenance Links")
        self.view_dlg = None
        if "view_dlg" in kwargs:
            self.view_dlg = kwargs["view_dlg"]

    def close_save_dlg(self):
        """
        Disconnect, save + close if valid
        """
        try:
            self.layer.selectionChanged.disconnect(self.esu_selection_changed)
        except TypeError:
            pass
        self.view_dlg.ui.rdPolyListWidget.clear()
        for esu in self.selected_dict:
            self.final_selection.append(esu)
            QListWidgetItem(str(esu), self.view_dlg.ui.rdPolyListWidget)
        self.button.setEnabled(True)
        self.esu_dlg.close()

    def populate_listwidget(self):
        """
        Deals with initial population and slot connection
        """
        if self.unsaved:
            # Re-populate list with previously selected but unsaved rd_polys. i.e. with same modification
            for esu in self.unsaved:
                self.selected_dict[int(esu)] = QListWidgetItem(str(esu), self.esu_dlg.ui.esuLinkListWidget)
            self.original_selection = self.unsaved
        else:
            sql = "SELECT rd_pol_id FROM lnkMAINT_RD_POL WHERE maint_id = %s and currency_flag = 0" % \
                  (self.view_dlg.ui.maintIdLineEdit.text())
            query = QSqlQuery(sql, self.db)
            rd_pol_list = []
            while query.next():
                rd_pol = query.value(0)
                rd_pol_list.append(rd_pol)
            self.original_selection = rd_pol_list
            for esu in rd_pol_list:
                        self.selected_dict[int(esu)] = QListWidgetItem(str(esu), self.esu_dlg.ui.esuLinkListWidget)

        # Select the rd polygons
        feats = self.gn_fnc.get_features_from_field_value(self.original_selection, 'rd_pol_id', 'Road Polygons')
        bbox = self.gn_fnc.select_features(feats, self.layer_name)
        test_bbox = bbox.isNull()
        if not test_bbox:
            self.gn_fnc.zoom_to_extent(bbox)
        # Connect selection changed signal
        self.connect_selection_change()


class SrwrDeleteMaintenanceRecord(object):
    """
    Delete a maintenance record.
    """

    id_col = 1

    def __init__(self, street_browser, db, model, usrn, table_view):
        """
        :param street_browser: Street browser dialog
        :param db: Qt database connection
        :param model: srwr model
        :param usrn: current usrn
        """
        self.street_browser = street_browser
        self.db = db
        self.model = model
        self.usrn = usrn
        self.table_view = table_view

    def delete(self):
        """
        Main method for deleting a record. Closes the record in tblMAINT.
        """
        row = self.table_view.currentIndex().row()
        maint_id = self.model.data(self.model.index(row, self.id_col), Qt.DisplayRole)
        confirm_delete_dlg = QMessageBox(
                                         " ",
                                        "Are you sure you want to delete record " + str(maint_id),
                                         QMessageBox.Warning, QMessageBox.Yes, QMessageBox.No,
                                         QMessageBox.NoButton, None)
        confirm_delete_dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        confirm_delete_result = confirm_delete_dlg.exec_()
        # Check if save requested
        if confirm_delete_result == QMessageBox.Yes:
            if not self.any_existing_records(maint_id):
                self.close_record_db(maint_id, 'tblMAINT', 'maint_id')
                self.refresh_model()
                self.table_view.selectRow(0)
            else:
                # Cant delete because maint record is attached to a polygon
                no_delete_msg_box = QMessageBox(QMessageBox.Warning, " ", "Cannot delete a maintenance record "
                                                "while it is attached to a road polygon",
                                                QMessageBox.Ok, None)
                no_delete_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                no_delete_msg_box.exec_()
        if confirm_delete_result == QMessageBox.No:
            pass

    def close_record_db(self, id_, table, id_col_name):
        """
        :param table: SRWR table
        :param id_col_name: ID column name
        :param id_: Record ID
        """
        today = str(datetime.datetime.now().strftime("%Y%m%d"))
        user = self.street_browser.ui.byLineEdit.text()
        sql = 'UPDATE %s SET currency_flag=1, closure_date=%s, closed_by="%s" WHERE usrn = %s AND %s = %s ' \
              'AND currency_flag = 0' % (table, today, user, self.usrn, id_col_name, id_)
        query = QSqlQuery(sql, self.db)

    def any_existing_records(self, maint_id):
        """
        Checks if a maint record is attached to any road polygons.
        :param maint_id: maintenance ID
        :return: True if record has live attachments
        """
        sql = "SELECT rd_pol_id FROM lnkMAINT_RD_POL WHERE maint_id = %s AND currency_flag = 0" % maint_id
        query = QSqlQuery(sql, self.db)
        if query.seek(0):
            return True
        else:
            return False

    def refresh_model(self):
        """
        Repopulate the model
        """
        self.model.select()
        while self.model.canFetchMore():
            self.model.fetchMore()
