# -*- coding: utf-8 -*-

import os

from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import Qt, pyqtSlot
from PyQt4.QtGui import (
    QDataWidgetMapper, 
    QAbstractItemView,
    QSortFilterProxyModel,
    QListWidgetItem,
    QMessageBox,
    QPixmap,
    QIcon)
from qgis.core import QgsMapLayerRegistry
from srwr_maintenance import MaintenanceTable
from srwr_reinstatement_cat import ReinstatementCategoriesTable
from srwr_special_designation import SpecialDesignationTable
from ..roadnet_dialog import FilterStreetRecordsDlg
from filter_street_records import PopulateFilterTableView
from edit import EditRecord
from add import AddRecord
from close import CloseRecord
from ..generic_functions import ZoomSelectCanvas, DateMapperCustomDelegate, ShowStreetCoordinates
from ..generic_functions import ipdb_breakpoint

__author__ = 'matthew.walsh'


class StreetBrowser:
    def __init__(self, iface, street_browser, model, db, params):
        # Local ref to street browsers dock and iface
        self.street_browser = street_browser
        self.iface = iface
        self.model = model
        self.db = db
        self.params = params
        self.fltr_street_rcd_dlg = FilterStreetRecordsDlg()
        # Connect db
        self.mapper = None
        self.proxy = None
        self.setup_proxy_and_mapper()
        self.show_street = None
        # Display first record on load
        self.mapper.toFirst()
        # Create instance of editing class
        self.modify = EditRecord(self.iface, self.street_browser, self.model, self.mapper, self.db, self.params)
        self.modify.edit_signals.currentIndexSet.connect(self.disable_close)
        self.add = AddRecord(self.iface, self.street_browser, self.model, self.mapper, self.db, self.params)
        self.close = CloseRecord(self.iface, self.street_browser, self.model, self.mapper, self.db, self.params)
        # Create instance of filter pop class
        self.pop_filter_table = PopulateFilterTableView(self, self.fltr_street_rcd_dlg, self.db, self.model)
        self.canvas_functs = ZoomSelectCanvas(self.iface, self.street_browser, self.db)
        self.srwr = ScottishRoadWorksRegister(self.street_browser, self.db, self.iface, self.params)
        self.srwr.tab_idx_changed(0)
        self.connect_model_navigation()

    def setup_proxy_and_mapper(self):
        """
        Map data fields to widgets in street browser and create proxy for filtering
        """
        self.mapper = QDataWidgetMapper()
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)
        self.mapper.setModel(self.proxy)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        # Set custom delegate for mapping to date widgets
        self.mapper.setItemDelegate(DateMapperCustomDelegate([6, 7, 8, 18]))
        self.mapper.currentIndexChanged.connect(self.mapper_idx_changed)
        self.map_widgets(self.mapper)

    def view_record(self):
        """
        Changes current displayed record to one from xref table
        """
        try:
            indexes = self.street_browser.ui.crossReferenceTableView.selectedIndexes()
            view_usrn = indexes[0].data()
            row_count = self.model.rowCount()
            counter = 0
            match = False
            while counter <= row_count and not match:
                idx = self.model.index(counter, 1)
                usrn = idx.data()
                counter += 1
                if view_usrn == usrn:
                    match = True
                    self.mapper.setCurrentIndex(idx.row())
        except IndexError:
            pass

    def mapper_idx_changed(self):
        """
        Remove abandoned 'show' geom and populate x-ref table
        """
        if str(self.street_browser.ui.showPushButton.text()).lower() == 'hide':
            self.show_street.remove()
            self.street_browser.ui.showPushButton.setText('Show')
        usrn = self.street_browser.ui.usrnLineEdit.text()
        xref = CrossRefTable(self.db, self.street_browser)
        xref.populate_cross_ref(usrn)
        self.populate_linked_esu_list()
        self.srwr_tab_repopulate()
        self.disable_close(usrn)

    def populate_linked_esu_list(self):
        """
        Populate the linked ESU list in the street browser
        """
        self.street_browser.ui.linkEsuListWidget.clear()
        # Add new linked esu's
        self.gn_fnc = ZoomSelectCanvas(self.iface, self.street_browser, self.db)
        esu_list = self.gn_fnc.query_esu(self.street_browser.ui.usrnLineEdit.text())
        for esu_id in esu_list:
            QListWidgetItem(str(esu_id), self.street_browser.ui.linkEsuListWidget)

    def set_buttons_initial_state(self, role):
        """
        checks the role of the user and enables/disables buttons accordingly
        if usrn button is already disabled it leaves it alone because usrn
        is linked to other categories
        :param role: user role
        :return: void
        """
        if role == 'admin' or role == 'editor':
            state = True
        else:
            state = False
        self.street_browser.ui.modifyPushButton.setEnabled(state)
        self.street_browser.ui.addPushButton.setEnabled(state)
        if self.street_browser.ui.closeOpPushButton.isEnabled():
            self.street_browser.ui.closeOpPushButton.setEnabled(state)

    def connect_model_navigation(self):
        """
        Connect record navigation buttons to widgetmapper functions
        """
        self.street_browser.ui.firstPushButton.clicked.connect(self.mapper.toFirst)
        self.street_browser.ui.lastPushButton.clicked.connect(self.mapper.toLast)
        self.street_browser.ui.previousPushButton.clicked.connect(self.mapper.toPrevious)
        self.street_browser.ui.nextPushButton.clicked.connect(self.mapper.toNext)
        # Connect filter btn to filter dlg
        self.street_browser.ui.filterPushButton.clicked.connect(self.filter_street_records)
        # Connect close button and map button
        kwargs = {'zoom_to': True, 'select': True, 'close': False}
        self.street_browser.ui.mapPushButton.clicked.connect(lambda: self.canvas_functs.zoom_to_record(**kwargs))
        self.street_browser.ui.viewPushButton.clicked.connect(self.view_record)
        self.street_browser.ui.showPushButton.clicked.connect(self.show_street_coordinates)
        # Connect modify button
        self.street_browser.ui.modifyPushButton.clicked.connect(self.modify_record)
        self.street_browser.ui.addPushButton.clicked.connect(self.add_record)
        self.street_browser.ui.closeOpPushButton.clicked.connect(self.close_record)
        # Connect SRWR tab
        self.street_browser.ui.srwrPushButton.clicked.connect(self.enable_srwr)
        # connect the default close button
        self.street_browser.signals.closed_sb.connect(self.remove_coords)

    def srwr_tab_repopulate(self):
        """
        Repopulate SRWR tab if appropriate
        """
        if self.street_browser.ui.srwrRecordsGroupBox.isVisible():
            cur_tab = self.street_browser.ui.srwrTabWidget.currentIndex()
            if not self.srwr:
                self.srwr = ScottishRoadWorksRegister(self.street_browser, self.db, self.iface, self.params)
            self.srwr.tab_idx_changed(cur_tab)

    def filter_street_records(self):
        self.fltr_street_rcd_dlg.exec_()  # DO NOT USE .show() FOR CHILD PROCESSES!

    def enable_srwr(self):
        """
        Toggles visibility of SRWR Records group
        """
        if self.street_browser.ui.srwrRecordsGroupBox.isVisible():
            self.street_browser.ui.srwrRecordsGroupBox.setVisible(False)
            self.street_browser.ui.srwrPushButton.setText("Show SRWR Details")
        else:
            self.street_browser.ui.srwrRecordsGroupBox.setVisible(True)
            self.street_browser.ui.srwrPushButton.setText("Hide SRWR Details")
            if not self.srwr:
                # Mimic tab change to populate the default tab
                self.srwr = ScottishRoadWorksRegister(self.street_browser, self.db, self.iface, self.params)
            self.srwr.tab_idx_changed(0)

    def show_street_coordinates(self):
        if str(self.street_browser.ui.showPushButton.text()).lower() == "show":
            startx = self.street_browser.ui.startXLineEdit.text()
            endx = self.street_browser.ui.endXLineEdit.text()
            starty = self.street_browser.ui.startYLineEdit.text()
            endy = self.street_browser.ui.endYLineEdit.text()
            coords = ((startx, starty), (endx, endy))
            if coords[0][0] and coords[1][0]:
                self.show_street = ShowStreetCoordinates(self.iface)
                self.show_street.show(coords)
                self.street_browser.ui.showPushButton.setText('Hide')
        else:
            self.show_street.remove()
            self.street_browser.ui.showPushButton.setText('Show')

    def modify_record(self):
        """
        Modify a an existing street record
        """
        if not self.is_layer_editing():
            self.modify.modify_record()

    def add_record(self):
        """
        Add a new new record
        """
        if not self.is_layer_editing():
            self.add.add()

    def close_record(self):
        """
        Close an existing street record
        """
        if not self.is_layer_editing():
            self.close.close()

    def is_layer_editing(self):
        """
        Checks if either the rd poly layer or esu layer are currently in editing state.
        :return: True if editing
        """
        esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
        rdpoly_layer = QgsMapLayerRegistry.instance().mapLayersByName('Road Polygons')[0]
        if esu_layer.isEditable() or rdpoly_layer.isEditable():
            no_add_esu_layer_msg_box = QMessageBox(QMessageBox.Warning, '',
                                                   'Cannot modify street record while editing layers',
                                                   QMessageBox.Ok, None)
            no_add_esu_layer_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_add_esu_layer_msg_box.exec_()
            return True
        else:
            return False

    def goto_record(self, index):
        """
        Navigate to a specific index in the model
        :param index: model idx
        """
        self.mapper.setCurrentIndex(index)

    def remove_coords(self):
        """
        remove the start/end coords from the canvas when the street browser is closed
        from the default button
        """
        if self.show_street:
            self.show_street.remove()
        if self.street_browser.ui.showPushButton.text() == "Hide":
            self.street_browser.ui.showPushButton.setText("Show")

    def map_widgets(self, mapper):
        """
        Map widgets to columns
        :param mapper: Data widget mapper
        """
        mapper.addMapping(self.street_browser.ui.classLineEdit, 19)  # street_class
        mapper.addMapping(self.street_browser.ui.versionLineEdit, 2)  # version_no
        mapper.addMapping(self.street_browser.ui.typeLineEdit, 4)  # street_ref_type
        mapper.addMapping(self.street_browser.ui.descriptionTextEdit, 5)  # description
        mapper.addMapping(self.street_browser.ui.localityLineEdit, 20)  # loc_ref
        mapper.addMapping(self.street_browser.ui.townLineEdit, 22)  # town_ref
        mapper.addMapping(self.street_browser.ui.countyLineEdit, 21)  # county_ref
        mapper.addMapping(self.street_browser.ui.authorityLineEdit, 9)  # authority
        mapper.addMapping(self.street_browser.ui.byLineEdit, 23)  # updated_by
        mapper.addMapping(self.street_browser.ui.updateDateLineEdit, 7)  # update_date
        mapper.addMapping(self.street_browser.ui.startDateLineEdit, 8)  # start_date
        mapper.addMapping(self.street_browser.ui.entryDateLineEdit, 6)  # entry_date
        mapper.addMapping(self.street_browser.ui.startXLineEdit, 11)  # start_xref
        mapper.addMapping(self.street_browser.ui.startYLineEdit, 12)  # start_yref
        mapper.addMapping(self.street_browser.ui.tolLineEdit, 15)  # tolerance
        mapper.addMapping(self.street_browser.ui.endXLineEdit, 13)  # end_xref
        mapper.addMapping(self.street_browser.ui.endYLineEdit, 14)  # end_yref
        mapper.addMapping(self.street_browser.ui.stateLineEdit, 17)  # street_state
        mapper.addMapping(self.street_browser.ui.stateDateLineEdit, 18)  # street_date
        mapper.addMapping(self.street_browser.ui.usrnLineEdit, 1)  # USRN

    @pyqtSlot(str)
    def disable_close(self, usrn):
        """
        disables the delete button
        in case a street is linked to other categories
        :param usrn : [str] the usrn of the current record in widget mapper
        """
        usrn_num_str = "SELECT (SELECT COUNT (usrn) FROM tblSPEC_DES WHERE usrn = {} AND currency_flag = 0) + " \
                       "(SELECT COUNT (usrn) FROM tblMAINT WHERE usrn = {} AND currency_flag = 0) + " \
                       "(SELECT COUNT (usrn) FROM tblREINS_CAT WHERE usrn = {} AND currency_flag = 0) AS NoUSRN"\
                       .format(usrn, usrn, usrn)
        usrn_num_query = QSqlQuery(usrn_num_str, self.db)
        usrn_num_query.first()
        linked_usrn_num = usrn_num_query.value(0)
        if linked_usrn_num > 0 or self.params['role'] == 'readonly':
            self.street_browser.ui.closeOpPushButton.setEnabled(False)
        else:
            self.street_browser.ui.closeOpPushButton.setEnabled(True)


class CrossRefTable:
    """
    Populate and style the cross reference qtableview
    """

    def __init__(self, db, street_browser):
        # locals refs
        self.db = db
        self.street_browser = street_browser
        self.cross_ref_lv = self.street_browser.ui.crossReferenceTableView

    def populate_cross_ref(self, usrn):
        """
        Selects all records which share the same ESU and have most recent currency_flag
        :param usrn: Current USRN
        """
        sql = """\
            SELECT DISTINCT tblSTREET.usrn, tblSTREET.street_ref_type,
                   tblSTREET.description
                FROM lnkESU_STREET INNER JOIN tblSTREET
                    ON tblSTREET.usrn=lnkESU_STREET.usrn
                WHERE tblSTREET.currency_flag = 0
                    AND lnkESU_STREET.currency_flag = 0
                    AND lnkESU_STREET.esu_id
                        IN (SELECT esu_id FROM lnkESU_STREET WHERE usrn = {usrn})
                    AND lnkESU_STREET.usrn != {usrn};""".format(usrn=usrn)
        # Use delegate to prefix street ref
        model = SqlCustomDelegate(self.db)
        model.setQuery(sql)
        # Get query result row count
        any_rows = model.rowCount()
        # Style + setup of qtreeview
        if any_rows > 0:
            self.cross_ref_lv.setAlternatingRowColors(True)
            self.cross_ref_lv.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.cross_ref_lv.setColumnWidth(0, 60)
            self.cross_ref_lv.setColumnWidth(1, 40)
            self.cross_ref_lv.setColumnWidth(2, 230)
            self.street_browser.ui.viewPushButton.setEnabled(True)
        else:
            self.street_browser.ui.viewPushButton.setEnabled(False)
        self.cross_ref_lv.setModel(model)


class SqlCustomDelegate(QSqlQueryModel):
    """
    Delegate to add 'Type' to prefix street ref number
    """

    def __init__(self, db, parent=None):
        super(SqlCustomDelegate, self).__init__(parent)
        self.db = db

    def data(self, index, int_role=None):
        """
        Reimplementation of data method if is col 1 (street type)
        :param index: model index
        :param int_role: Display role/User role etc
        :return: Modified value with Type prefix
        """
        value = QSqlQueryModel.data(self, index, int_role)
        if value and int_role == Qt.DisplayRole:
            if index.column() == 1:
                value = "Type " + str(value)
        return value


class ScottishRoadWorksRegister:
    """
    Wrapper class for populating SRWR tabs.
    """

    def __init__(self, street_browser, db, iface, params):
        self.street_browser = street_browser
        self.db = db
        self.iface = iface
        self.params = params
        self.connect_signals()
        self.maint_tab = None
        self.spec_des_tab = None
        self.reins_cat_tab = None

    def connect_signals(self):
        """
        Connect tab changed signal
        """
        self.street_browser.ui.srwrTabWidget.currentChanged.connect(self.tab_idx_changed)

    def tab_idx_changed(self, idx):
        """
        Sets the class variables to an instance of the appropriate SRWR type (e.g.maintenance)
        :param idx: current tab index
        """
        usrn = self.street_browser.ui.usrnLineEdit.text()
        self.disconnect_all()

        if idx == 0:
            self.spec_des_tab = None
            self.reins_cat_tab = None
            self.maint_tab = MaintenanceTable(self.street_browser, usrn, self.db,
                                              self.street_browser.ui.maintTableView, self.iface, self.params)
            self.maint_tab.signals.current_usrn_links.connect(self.disable_close)

        elif idx == 1:
            self.reins_cat_tab = None
            self.maint_tab = None
            self.spec_des_tab = SpecialDesignationTable(self.street_browser, usrn, self.db,
                                                        self.street_browser.ui.specDesTableView, self.iface, self.params)
            self.spec_des_tab.signals.current_usrn_links.connect(self.disable_close)

        elif idx == 2:
            self.maint_tab = None
            self.spec_des_tab = None
            self.reins_cat_tab = ReinstatementCategoriesTable(self.street_browser, usrn, self.db,
                                                              self.street_browser.ui.reinstCatTableView, self.iface,
                                                              self.params)
            self.reins_cat_tab.signals.current_usrn_links.connect(self.disable_close)

        else:
            pass

    def disconnect_all(self):
        """
        Disconnect all buttons
        """
        if self.maint_tab:
            try:
                self.maint_tab.disconnect_buttons()
            except TypeError:
                pass
        if self.spec_des_tab:
                try:
                    self.spec_des_tab.disconnect_buttons()
                except TypeError:
                    pass
        if self.reins_cat_tab:
            try:
                self.reins_cat_tab.disconnect_buttons()
            except TypeError:
                pass

    @pyqtSlot(str)
    def disable_close(self, usrn):
        """
        disables the delete button
        in case a street is linked to other categories
        :param usrn : [str] the usrn of the current record in widget mapper
        """
        print " signal received " + str(usrn)
        usrn_num_str = "SELECT (SELECT COUNT (usrn) FROM tblSPEC_DES WHERE usrn = {} AND currency_flag = 0) + " \
                       "(SELECT COUNT (usrn) FROM tblMAINT WHERE usrn = {} AND currency_flag = 0) + " \
                       "(SELECT COUNT (usrn) FROM tblREINS_CAT WHERE usrn = {} AND currency_flag = 0) AS NoUSRN"\
                       .format(usrn, usrn, usrn)
        usrn_num_query = QSqlQuery(usrn_num_str, self.db)
        usrn_num_query.first()
        linked_usrn_num = usrn_num_query.value(0)
        if linked_usrn_num > 0 or self.params['role'] == 'readonly':
            self.street_browser.ui.closeOpPushButton.setEnabled(False)
        else:
            self.street_browser.ui.closeOpPushButton.setEnabled(True)
