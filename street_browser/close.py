# -*- coding: utf-8 -*-
import datetime

from PyQt4.QtCore import Qt
from PyQt4.QtSql import QSqlQuery

from qgis.core import QgsMapLayerRegistry

from Roadnet.roadnet_dialog import SaveRecordDlg
from edit import UpdateEsuSymbology

__author__ = 'matthew.walsh'


class CloseRecord:
    """
    Deals with closing a street record and its associated links
    """
    save_dlg = None

    def __init__(self, iface, street_browser, model, mapper, db, params):
        self.street_browser = street_browser
        self.iface = iface
        self.model = model
        self.mapper = mapper
        self.db = db
        self.params = params

    def close(self):
        """
        Main method to begin close event
        """
        usrn = str(self.street_browser.ui.usrnLineEdit.text())
        self.save_dlg = SaveRecordDlg()  # Create a fresh one each time
        self.modify_save_dlg(usrn)
        self.save_dlg.exec_()

    def modify_save_dlg(self, usrn):
        """
        Update the save dlg ui for a close event
        :param usrn: current USRN
        """
        self.save_dlg.ui.label.setText("Are you sure you want to close " + usrn)
        self.save_dlg.ui.savePushButton.setText("Close")
        self.save_dlg.ui.savePushButton.clicked.connect(lambda: self.close_record(usrn))
        self.save_dlg.ui.revertPushButton.clicked.connect(self.cancel)
        self.save_dlg.ui.revertPushButton.setText("Cancel")
        self.save_dlg.ui.cancelPushButton.hide()
        self.save_dlg.setWindowTitle("Close record")
        self.save_dlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    def cancel(self):
        self.save_dlg.close()

    def close_record(self, usrn):
        """
        Actions to close record
        :param usrn: current USRN
        """
        # Close database records
        usrn = self.street_browser.ui.usrnLineEdit.text()
        today = str(datetime.datetime.now().strftime("%Y%m%d"))
        self.close_current_record(usrn, today)
        self.close_esu_links(usrn, today)
        self.repopulate_model()

        # Update ESU symbology
        esu_list = list()
        counter = 0
        while counter < self.street_browser.ui.linkEsuListWidget.count():
            esu_list.append(self.street_browser.ui.linkEsuListWidget.item(counter).text())
            counter += 1
        esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
        UpdateEsuSymbology(self.db, esu_layer).update(usrn, esu_list=esu_list)

        # Update display
        self.iface.mapCanvas().refresh()
        self.save_dlg.close()

    def close_esu_links(self, usrn, closure_date):
        """
        Close any existing ESU links which are linked to this street
        :param usrn: current USRN
        :param closure_date: date string (yyyymmdd)
        """
        sql = """UPDATE lnkESU_STREET SET currency_flag=1, closure_date=%s WHERE usrn = %s AND currency_flag = 0""" \
              % (closure_date, usrn)
        query = QSqlQuery(sql, self.db)

    def close_current_record(self, usrn, closure_date):
        """
        Close the street record
        :param usrn: current USRN
        :param closure_date: date string (yyyymmdd)
        """
        sql = """UPDATE tblSTREET
                     SET currency_flag=1,
                         closure_date={closure_date},
                         closed_by='{username}'
                     WHERE usrn={usrn} AND
                         currency_flag=0;
                """.format(closure_date=closure_date, usrn=usrn,
                           username=self.params['UserName'])
        query = QSqlQuery(sql, self.db)

    def repopulate_model(self):
        """
        Repopulate the model to reflect the changes
        """
        self.model.select()
        while self.model.canFetchMore():
            self.model.fetchMore()
        # jump to new record (inserted at end)
        self.mapper.toFirst()
