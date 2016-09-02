from PyQt4.QtCore import QThread, pyqtSignal, QObject, Qt, pyqtSlot
from PyQt4.QtSql import QSqlQuery

from Roadnet.roadnet_dialog import SymbologyDlg
from Roadnet.street_browser.edit import UpdateEsuSymbology

__author__ = 'matthew.walsh'


class UpdateSymbology:
    """
    Update the symbology of the Road Polygon and/or ESU Graphic Layer.
    """

    def __init__(self, db, rdpoly_layer, esu_layer):
        """
        :param db: database connection
        :param rdpoly_layer: road polygon layer
        :param esu_layer: esu graphic layer
        """
        # Set rdpoly layer + feature_count
        self.rdpoly_layer = rdpoly_layer
        self.rdpoly_count = self.rdpoly_layer.featureCount()
        # Set esu layer + feature count
        self.esu_layer = esu_layer
        self.esu_count = self.esu_layer.featureCount()

        self.db = db
        self.rdpoly_worker = None
        # Create dialog instance
        self.symbology_dlg = SymbologyDlg()
        self.symbology_dlg.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.symbology_dlg.setModal(False)
        self.connect_signals()

    def connect_signals(self):
        """
        Connect signals for GUI buttons and custom signals for updating the GUI from the thread.
        """
        self.symbology_dlg.ui.runPushButton.clicked.connect(self.start_update)

    def show_symbology_dlg(self):
        """
        Main run method for the symbology updater.
        """
        self.symbology_dlg.show()

    def start_update(self):
        """
        Start the update on a thread.
        """
        if self.symbology_dlg.ui.runPushButton.text() == "Run":
            esu_checked = self.symbology_dlg.ui.esuCheckBox.isChecked()
            rdpoly_checked = self.symbology_dlg.ui.rdPolyCheckBox.isChecked()
            if esu_checked or rdpoly_checked:
                self.create_thread(rdpoly_checked, esu_checked)
                # else:
                #     self.rdpoly_worker.terminate()
                #     self.rdpoly_worker.wait()
                #     self.update_terminated()

    def create_thread(self, run_rdpoly, run_esu):
        """
        Create and start the thread that does the heavy lifting.
        :param run_rdpoly: bool to update the rdpoly layer
        :param run_esu: bool to update the esu layer
        """
        self.rdpoly_worker = UpdateSymbologyThread(self.db, self.rdpoly_layer, self.esu_layer, run_rdpoly, run_esu)
        self.rdpoly_worker.setTerminationEnabled(True)
        self.rdpoly_worker.signals.task_started.connect(self.task_started)
        self.rdpoly_worker.signals.task_finished.connect(self.task_finished)
        self.rdpoly_worker.signals.update_progress.connect(self.update_progress)
        self.rdpoly_worker.start()

    @pyqtSlot()
    def task_started(self):
        """
        Set the dialog to its initial run state.
        :return: void
        """
        self.symbology_dlg.ui.progressBar.setValue(0)
        # self.symbology_dlg.ui.runPushButton.setText("Abort")
        self.symbology_dlg.ui.runPushButton.setEnabled(False)

    @pyqtSlot()
    def task_finished(self):
        """
        Enable the 'Run' button.
        """
        # self.symbology_dlg.ui.runPushButton.setText("Run")
        self.symbology_dlg.ui.runPushButton.setEnabled(True)

    # def update_terminated(self):
    #     """
    #     Cleanup for a user cancel event. Discards all changes to both layers.
    #     """
    #     self.esu_layer.rollBack()
    #     # Change GUI back to initial state
    #     self.task_finished()

    @pyqtSlot(int, int, int)
    def update_progress(self, percentage, rdpoly_count, esu_count):
        """
        Update the labels on the dialog and update the progressbar.
        :param percentage: % task is complete
        :param rdpoly_count: Number of symbology updates on the rdpoly layer
        :param esu_count: Number of symbology updates on the esu layer
        """
        self.symbology_dlg.ui.progressBar.setValue(percentage)
        features_updated_text = """<html>
                                   <head/>
                                   <body>
                                   <p><span style="font-weight:600;">Updated Features</span></p>
                                   <p>ESU Graphic: {0}/{1}</p>
                                   <p>Road Polygon: {2}/{3}</p>
                                   </body>
                                   </html>""".format(esu_count, self.esu_count, rdpoly_count, self.rdpoly_count)
        self.symbology_dlg.ui.updatedFeaturesLabel.setText(features_updated_text)


class UpdateSymbologyThread(QThread):
    """
    Worker thread to update the symbology of each road polygon feature.
    """

    esu_f_count = 0
    rdpoly_f_count = 0
    rdpoly_change_count = 0
    esu_change_count = 0
    features_complete = 0

    def __init__(self, db, rdpoly_layer, esu_layer, run_rdpoly, run_esu):
        """

        :param db: database connection
        :param rdpoly_layer: road polygon layer
        :param esu_layer: esu layer
        :param run_rdpoly: bool whether to run the rdpoly update
        :param run_esu: bool whether to run the esu update
        """
        QThread.__init__(self)
        self.db = db
        self.rdpoly_layer = rdpoly_layer
        self.esu_layer = esu_layer
        self.run_rdpoly = run_rdpoly
        self.run_esu = run_esu
        self._init_data()
        self.total_f_count = self.calculate_total_feature_count()

    def _init_data(self):
        self.signals = ThreadSignals()
        # Total number of features on each layer
        self.rdpoly_f_count = self.rdpoly_layer.dataProvider().featureCount()
        self.esu_f_count = self.esu_layer.dataProvider().featureCount()

    def run(self):
        """
        Override the QThread main run method (never called directly).
        """
        self.signals.task_started.emit()
        if self.run_esu:
            self.run_esu_update()
        if self.run_rdpoly:
            self.run_rdpoly_update()
        self.signals.task_finished.emit()

    def run_esu_update(self):
        """
        Updates the symbology of the esu graphic layer.
        """
        self.esu_layer.startEditing()
        symbology_update = UpdateEsuSymbology(self.db, self.esu_layer)
        for feat in self.esu_layer.getFeatures():
            self.set_percentage_complete()
            esu_id = feat.attribute('esu_id')
            symbol_value = feat.attribute('symbol')
            # calculate the correct symbology values
            types = symbology_update.street_ref_types(esu_id)
            new_symbol_value = symbology_update.calculate_symbol_no(types)
            if new_symbol_value != symbol_value:
                # Only set if its changed
                feat.setAttribute('symbol', new_symbol_value)
                self.esu_layer.updateFeature(feat)
                self.esu_change_count += 1
        self.esu_layer.commitChanges()

    def run_rdpoly_update(self):
        """
        Updates the symbology of the rdpoly layer.
        """
        self.rdpoly_layer.startEditing()
        for feat in self.rdpoly_layer.getFeatures():
            self.set_percentage_complete()
            rd_pol_id = feat.attribute('rd_pol_id')
            symbol_value = feat.attribute('symbol')
            sql = """SELECT maint_id FROM lnkMAINT_RD_POL
                     WHERE rd_pol_id = {rd_pol_id}
                       AND currency_flag = 0""".format(rd_pol_id=rd_pol_id)
            query = QSqlQuery(sql, self.db)
            linked_maint = list()
            while query.next():
                linked_maint.append(query.value(0))
            new_symbol_value = self.calculate_rdpoly_symbology_value(linked_maint)
            if new_symbol_value != symbol_value:
                # Only set if its changed
                feat.setAttribute('symbol', new_symbol_value)
                self.rdpoly_layer.updateFeature(feat)
                self.rdpoly_change_count += 1
        self.rdpoly_layer.commitChanges()

    def calculate_rdpoly_symbology_value(self, maint_ids):
        """
        Calculates the symbology depending on how many maint records are attached to a rdpoly feature.
        :rtype: int
        :param maint_ids: list of maint id's attached to a road polygon feature
        :return: symbology value
        """
        size = len(maint_ids)
        if size == 0:
            # No records attached to rdpoly
            symbology = 1
        elif size == 1:
            # Single attached record, get the record type by query
            maint_id = maint_ids[0]
            road_status_ref = self.get_road_status_ref(maint_id)
            symbology = road_status_ref + 10
        else:
            # More than one other record attached
            symbology = 2  # 2 = multiple
        return symbology

    def get_road_status_ref(self, maint_id):
        """
        Query database to get road status for given maintenance ID.
        :param maint_id: maintenance ID
        :return: integer road status ref.
        """
        sql = """
            SELECT road_status_ref FROM tblMAINT
            WHERE maint_id = {maint_id}
            AND currency_flag = 0
            ;""".format(maint_id=maint_id)
        query = QSqlQuery(sql, self.db)
        query.seek(0)
        road_status_ref = int(query.value(0))
        self.fail_if_invalid_road_status_ref(maint_id, road_status_ref)
        return road_status_ref

    @staticmethod
    def fail_if_invalid_road_status_ref(maint_id, road_status_ref):
        """
        Raise exeption if road status ref is incorrect
        :param road_status_ref:
        :param maint_id:
        """
        if road_status_ref > 4:
            raise ValueError(
                "Maintenance record {} has invalid road_status_ref".format(
                    maint_id))

    def set_percentage_complete(self):
        """
        Calculate the progress percentage of the entire update.
        """
        self.features_complete += 1
        percentage_complete = (self.features_complete * 100) / self.total_f_count
        self.signals.update_progress.emit(percentage_complete, self.rdpoly_change_count, self.esu_change_count)

    def calculate_total_feature_count(self):
        """
        Calculate the total number of features to be processed (used to calculate percentage).
        """
        total = 0
        if self.run_esu:
            total += self.esu_f_count
        if self.run_rdpoly:
            total += self.rdpoly_f_count
        return total


class ThreadSignals(QObject):
    """
    class that holds the signals emitted from the thread and received by the worker to update gui status.
    """
    task_started = pyqtSignal()
    task_finished = pyqtSignal()
    # Params = % complete, rdpoly change count, esu change count
    update_progress = pyqtSignal(int, int, int)
