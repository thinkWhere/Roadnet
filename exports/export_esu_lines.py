# -*- coding: utf-8 -*-
import os
from multiprocessing.pool import ThreadPool

from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog, QProgressDialog, QMessageBox
from PyQt4.QtCore import QVariant, Qt, QByteArray

from qgis.core import (
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsGeometry,
    QgsFeature,
    QgsVectorFileWriter,
    QGis,
    QgsFields)

from qgis.gui import *
from Roadnet import config
from Roadnet.generic_functions import ipdb_breakpoint

__author__ = 'matthew.bradley'


def thread(func):
    """
    Applying to methods that you want to block while permitting GUI threads to process Qgis events
    :param func:
    :return:
    """
    def wrap(*args, **kwargs):
        pool = ThreadPool(processes=1)
        async = pool.apply(func, args, kwargs)
        return async
    return wrap


class ExportESUShapes:
    """
    Class handling the exports of ESUs to lines sahpefiles
    """
    progress = QtCore.pyqtSignal(float)

    def __init__(self, iface, db, unassigned, export_path):
        self.killed = False
        self.iface = iface
        self.db = db
        self.unassigned = unassigned
        self.export_path = export_path
        self.prepare_sql_queries()

        self.progresswin = QProgressDialog("Exporting Shapefile...", "Abort", 0, 100)
        self.progresswin.setWindowModality(Qt.WindowModal)
        self.progresswin.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.progresswin.setWindowTitle(" ")

    def kill_export(self):
        self.killed = True

    # @thread
    def export_esu_line(self):
        """
        Export ESUs
        :return:
        """

        canvas = self.iface.mapCanvas()
        clayer = canvas.currentLayer()
        # will return 0 if none selected
        count = clayer.selectedFeatureCount()

        feature_count = clayer.featureCount()

        # Get list of selected features
        selected_esu_ids = list()
        if count > 0:
            selectedfeats = clayer.selectedFeatures()
            for feat in selectedfeats:
                selected_esu_ids.append(int(feat.attribute('esu_id')))
            feature_count = clayer.selectedFeatureCount()
            self.warn_about_selected_features(feature_count)

        # Prepare sql query
        if self.unassigned:
            nsgexportsql = self.sql_queries['export_all']
        else:
            nsgexportsql = self.sql_queries['export_assigned_only']

        # SQL to filter out selected records
        if count > 0:
            nsgexportsql += " WHERE esu.esu_id IN ({})".format(
                ', '.join(map(str, selected_esu_ids)))

        # Setup database temporary tables
        for table in ['qryType12', 'qryType3', 'qryType4']:
            # Drop tables if left behind from last export
            args = {'table': table}
            query = self.run_sql('drop_table', args)
        query = self.run_sql('create_qryType12')
        query = self.run_sql('create_qryType3')
        query = self.run_sql('create_qryType4')

        # Run the main query
        if config.DEBUG_MODE:
            print(nsgexportsql)
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        query.exec_(nsgexportsql)
        if query.isActive() is False:
            raise StandardError('Database query problem: {}'.format(
                query.lastError().text()))

        # create layer
        vlayer = QgsVectorLayer("multilinestring?crs=EPSG:27700", "temp", "memory")
        vlayer.setCrs(QgsCoordinateReferenceSystem(27700, QgsCoordinateReferenceSystem.EpsgCrsId))
        provider = vlayer.dataProvider()

        # add fields
        self.fields = [QgsField("esu_id", QVariant.String),
                       QgsField("USRN", QVariant.LongLong),
                       QgsField("Rec_type", QVariant.Int),
                       QgsField("DescTxt", QVariant.String),
                       QgsField("Locality", QVariant.String),
                       QgsField("Town", QVariant.String),
                       QgsField("Entry_date", QVariant.Date),
                       QgsField("Type_3_USRN", QVariant.LongLong),
                       QgsField("Type_3_Desc", QVariant.String),
                       QgsField("Type_4_USRN", QVariant.LongLong),
                       QgsField("Type_4_Desc", QVariant.String)]
        provider.addAttributes(self.fields)
        vlayer.updateFields()

        # Exit if output file path is invalid
        if len(str(self.export_path)) < 0:
            return False
        if self.check_if_export_file_in_use():
            return False

        # Run through SQL results creating features from rows
        self.progresswin.show()
        i = 0
        while query.next():
            if self.progresswin.wasCanceled():
                self.kill_export()
                break

            record = query.record()
            new_feature = self.create_feature_from_record(record)
            provider.addFeatures([new_feature])

            # Update progress bar
            i += 1
            diff = feature_count + (i - feature_count) if i > feature_count else feature_count
            percent_complete = (i / float(diff)) * 100
            self.progresswin.setValue(percent_complete)

        if self.killed:
            # Show message and exit if killed
            export_error_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                               "An error occurred while exporting shapefile",
                                               QMessageBox.Ok, None)
            export_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            export_error_msg_box.exec_()
            return False

        vlayer.updateExtents()
        result = QgsVectorFileWriter.writeAsVectorFormat(vlayer, self.export_path, "utf-8",
                                                         None, "ESRI Shapefile")
        # checks for completed export
        if result == 0:
            self.progresswin.close()
            if config.DEBUG_MODE:
                print('DEBUG_MODE: {} features exported'.format(vlayer.featureCount()))
            return True

    def check_if_export_file_in_use(self):
        """
        Attempts to write to export file, to check if in use. Warns if so.
        This check only works in Windows.
        :return: boolean
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Checking if output file in use.')
        field_map = QgsFields()
        for field in self.fields:
            field_map.append(field)

        writer = QgsVectorFileWriter(str(self.export_path), "utf-8", field_map,
                                     QGis.WKBMultiLineString, None, "ESRI Shapefile")
        if writer.hasError() != QgsVectorFileWriter.NoError:
            file_open_msg_box = QMessageBox(QMessageBox.Warning, " ", "The file {} is already open "
                                                                      "(possibly in another application).\n"
                                                                      "Close the file and try again".format(str(self.export_path)),
                                            QMessageBox.Ok, None)
            file_open_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            file_open_msg_box.exec_()
            return True
        return False

    def create_feature_from_record(self, record):
        """
        Create feature in temporary layer from record returned from query.
        :param record: QSqlQuery record describing feature
        """
        feature = QgsFeature()
        wkb = record.value('geom')
        if type(wkb) == QByteArray:
            geometry = QgsGeometry()
            geometry.fromWkb(wkb)
            feature.setGeometry(geometry)
        else:
            "NOT a byte"

        feature.setAttributes([record.value('esu_id'),
                               record.value('usrn'),
                               record.value('rec_type'),
                               record.value('desctxt'),
                               record.value('locality'),
                               record.value('town'),
                               record.value('entry_date'),
                               record.value('type_3_usrn'),
                               record.value('type_3_desc'),
                               record.value('type_4_usrn'),
                               record.value('type_4_desc')])
        return feature

    def warn_about_selected_features(self, feature_count):
        """
        Pop a message box if user has selected features.
        :param feature_count: Number of selected features for export
        """
        selection_warning_message = QMessageBox(
            QMessageBox.Information, " ",
            "Exporting from the {} selected ESU features only".format(feature_count),
            QMessageBox.Ok, None)
        selection_warning_message.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        selection_warning_message.exec_()

    def run_sql(self, query, kwargs={}):
        """
        Run SQL query (defined with key 'query' in self.sql_queries) on the
        database.

        return: QSqlQuery object to extract results
        """
        query = self.sql_queries[query]
        sql = query.format(**kwargs)
        if config.DEBUG_MODE:
            print(sql)
        active_query = QSqlQuery(sql, self.db)
        if active_query.isActive() is False:
            raise StandardError('Database query problem: {}'.format(
                active_query.lastError().text()))
        return active_query

    def prepare_sql_queries(self):
        """
        Store the sql queries used in the export.
        """
        self.sql_queries = {
            'drop_table': """
                DROP TABLE IF EXISTS {table}
                    ;""",
            'create_qryType12': """
                CREATE TEMP TABLE qryType12 AS
                    SELECT lnkesu_street.esu_id,
                       tblstreet.usrn,
                       tblstreet.street_ref_type AS Rec_type,
                       tblstreet.description     AS DescTxt,
                       tlkplocality.NAME         AS Locality,
                       tlkptown.NAME             AS Town,
                       tblstreet.entry_date
                    FROM lnkesu_street
                       INNER JOIN tblstreet
                           ON lnkesu_street.usrn_version_no = tblstreet.version_no
                           AND lnkesu_street.usrn = tblstreet.usrn
                       INNER JOIN tlkplocality
                           ON tblstreet.loc_ref = tlkplocality.loc_ref
                       INNER JOIN tlkptown
                           ON tblstreet.town_ref = tlkptown.town_ref
                    WHERE  tblstreet.street_ref_type IN (1, 2)
                       AND lnkesu_street.currency_flag = 0
                       AND tblstreet.currency_flag = 0
                       ;""",
            'create_qryType3': """
                CREATE TEMP TABLE qryType3 AS
                    SELECT lnkesu_street.esu_id,
                           tblstreet.usrn        AS Typ3USRN,
                           tblstreet.description AS Typ3Desc
                    FROM   lnkesu_street
                       INNER JOIN tblstreet
                           ON lnkesu_street.usrn = tblstreet.usrn
                           AND lnkesu_street.usrn_version_no = tblstreet.version_no
                    WHERE lnkesu_street.currency_flag = 0
                           AND tblstreet.street_ref_type = 3
                           AND tblstreet.currency_flag = 0
                           ;""",
            'create_qryType4': """
                CREATE TEMP TABLE qryType4 AS
                    SELECT lnkesu_street.esu_id,
                           tblstreet.usrn        AS Typ4USRN,
                           tblstreet.description AS Typ4Desc
                    FROM   lnkesu_street
                       INNER JOIN tblstreet
                        ON lnkesu_street.usrn_version_no = tblstreet.version_no
                        AND lnkesu_street.usrn = tblstreet.usrn
                    WHERE lnkesu_street.currency_flag = 0
                        AND tblstreet.street_ref_type = 4
                        AND tblstreet.currency_flag = 0
                        ;""",
            'export_all': """
                SELECT Asbinary(esu.geometry) AS geom,
                       qryType12.esu_id       AS esu_id,
                       qryType12.usrn         AS usrn,
                       qryType12.rec_type     AS rec_type,
                       qryType12.desctxt      AS desctxt,
                       qryType12.locality     AS locality,
                       qryType12.town         AS town,
                       qryType12.entry_date   AS entry_date,
                       qryType3.typ3usrn      AS type_3_usrn,
                       qryType3.typ3desc      AS type_3_desc,
                       qryType4.typ4usrn      AS type_3_usrn,
                       qryType4.typ4desc      AS type_4_desc
                FROM esu
                   LEFT JOIN qryType12
                       ON esu.esu_id = qryType12.esu_id
                   LEFT JOIN qryType3
                       ON esu.esu_id = qryType3.esu_id
                   LEFT JOIN qryType4
                       ON esu.esu_id = qryType4.esu_id
                       """,
            'export_assigned_only': """
                SELECT Asbinary(esu.geometry)  AS geom,
                       qryType12.esu_id        AS esu_id,
                       qryType12.usrn          AS usrn,
                       qryType12.rec_type      AS rec_type,
                       qryType12.desctxt       AS desctxt,
                       qryType12.locality      AS locality,
                       qryType12.town          AS town,
                       qryType12.entry_date    AS entry_date,
                       qryType3.typ3usrn       AS type_3_usrn,
                       qryType3.typ3desc       AS type_3_desc,
                       qryType4.typ4usrn       AS type_3_usrn,
                       qryType4.typ4desc       AS type_4_desc
                FROM qryType12
                   LEFT JOIN  qryType3
                       ON qryType12.esu_id = qryType3.esu_id
                   LEFT JOIN qryType4
                       ON qryType12.esu_id = qryType4.esu_id
                   LEFT JOIN esu
                       ON qryType12.esu_id = esu.esu_id
                """}
