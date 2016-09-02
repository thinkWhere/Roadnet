# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt, QByteArray, QDate
from PyQt4.QtGui import QProgressDialog, QMessageBox
from PyQt4.QtSql import QSqlQuery
from qgis.core import (
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsGeometry,
    QgsFeature,
    QgsVectorFileWriter,
    QgsFields,
    QGis)
from qgis.gui import *
from Roadnet import config

__author__ = 'matthew.bradley'


class ExportPolyShapes(QtCore.QObject):
    # finished = QtCore.pyqtSignal(object)
    # error = QtCore.pyqtSignal(Exception, basestring)
    progress = QtCore.pyqtSignal(float)

    def __init__(self, iface, public_only, unassigned, export_path, db):
        QtCore.QObject.__init__(self)
        self.killed = False
        self.iface = iface
        self.db = db
        self.unassigned = unassigned
        self.public_only = public_only
        self.export_path = export_path
        self.prepare_sql_queries()
        self.percent_complete = None

        self.progresswin = QProgressDialog("Exporting Shapefile...", "Abort", 0, 100)
        self.progresswin.setWindowModality(Qt.WindowModal)
        self.progresswin.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.progresswin.setWindowModality(Qt.WindowModal)

    def kill_export(self):
        self.killed = True

    def export_polys(self):
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
        selected_poly_ids = list()
        if count > 0:
            selectedfeats = clayer.selectedFeatures()
            for feat in selectedfeats:
                selected_poly_ids.append(int(feat.attribute('rd_pol_id')))
            feature_count = clayer.selectedFeatureCount()
            self.warn_about_selected_features(feature_count)

        # Prepare sql query
        if self.unassigned:
            polyexportsql = self.sql_queries['export_all']
        else:
            polyexportsql = self.sql_queries['export_assigned_only']

        # SQL to filter out unselected and/or public road records
        if count > 0:
            polyexportsql += " WHERE rd_pol_id IN ({})".format(
                ', '.join(map(str, selected_poly_ids)))
        else:
            polyexportsql += " WHERE rd_pol_id IS NOT NULL"
        if self.public_only:
            polyexportsql += " AND is_public = 1"

        # Setup database temporary tables
        for table in ['maint_records']:
            # Drop tables if left behind from last export
            args = {'table': table}
            query = self.run_sql('drop_table', args)
        query = self.run_sql('create_maint_records')

        # Run the main query
        if config.DEBUG_MODE:
            print(polyexportsql)
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        query.exec_(polyexportsql)
        if query.isActive() is False:
            raise StandardError('Database query problem: {}'.format(
                query.lastError().text()))

        # create layer
        vlayer = QgsVectorLayer("multipolygon?crs=EPSG:27700", "temp", "memory")
        vlayer.setCrs(QgsCoordinateReferenceSystem(27700, QgsCoordinateReferenceSystem.EpsgCrsId))
        provider = vlayer.dataProvider()

        # add fields
        self.fields = [QgsField("poly_id", QVariant.String),
                       QgsField("RefNo", QVariant.LongLong),
                       QgsField("rec_type", QVariant.Int),
                       QgsField("desctxt", QVariant.String),
                       QgsField("Locality", QVariant.String),
                       QgsField("Town", QVariant.String),
                       QgsField("LocTxt", QVariant.String),
                       QgsField("RdStatus", QVariant.LongLong),
                       QgsField("Swa_org", QVariant.String),
                       QgsField("Adopt_Date", QVariant.Date),
                       QgsField("Entry_Date", QVariant.Date),
                       QgsField("lor_no", QVariant.Int),
                       QgsField("route", QVariant.String)]
        provider.addAttributes(self.fields)
        vlayer.updateFields()

        # Exit if output file path is invalid
        if len(str(self.export_path)) < 0:
            return False
        if self.check_if_export_file_in_use():
            return False

        # Run through SQL results creating features from records
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
            self.percent_complete = (i / float(diff)) * 100
            self.progresswin.setValue(self.percent_complete)

        if self.killed:
            # Show message and exit if killed
            export_error_msg_box = QMessageBox(QMessageBox.Warning, " ", "An error occurred while exporting the"
                                                                         "shapefile", QMessageBox.Ok, None)
            export_error_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            export_error_msg_box.exec_()
            return False

        vlayer.updateExtents()
        result = QgsVectorFileWriter.writeAsVectorFormat(vlayer, self.export_path, "utf-8", None, "ESRI Shapefile")

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

        feature.setAttributes([record.value('poly_id'),
                               record.value('RefNo'),
                               record.value('rec_type'),
                               record.value('desctxt'),
                               record.value('locality'),
                               record.value('town'),
                               record.value('LocTxt'),
                               record.value('RdStatus'),
                               record.value('Swa_org'),
                               QDate().fromString(str(record.value('Adopt_Date')), 'yyyyMMdd'),
                               QDate().fromString(str(record.value('Entry_Date')), 'yyyyMMdd'),
                               record.value('lor_no'),
                               record.value('route')])
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
            'create_maint_records': """
                CREATE TEMP TABLE maint_records AS
                    SELECT lnkmaint_rd_pol.rd_pol_id   AS poly_id,
                           tblmaint.usrn               AS usrn,
                           tblmaint.reference_no       AS RefNo,
                           tblstreet.street_ref_type   AS rec_type,
                           tblstreet.description       AS descTxt,
                           tlkplocality.NAME           AS locality,
                           tlkptown.NAME               AS town,
                           tblmaint.location_text      AS LocTxt,
                           tlkproad_status.description AS RdStatus,
                           tlkporg.description         AS Swa_org,
                           tblmaint.adoption_date      AS Adopt_Date,
                           tblmaint.entry_date         AS Entry_Date,
                           tblmaint.lor_no             AS lor_no,
                           tblmaint.route              AS route,
                           tblmaint.road_status_ref    AS is_public
                    FROM lnkmaint_rd_pol
                             INNER JOIN (tblmaint
                                 INNER JOIN tlkproad_status
                                     ON tblmaint.road_status_ref = tlkproad_status.road_status_ref
                                 INNER JOIN tlkporg
                                     ON tblmaint.swa_org_ref = tlkporg.swa_org_ref)
                                 ON lnkmaint_rd_pol.maint_id = tblmaint.maint_id
                         INNER JOIN tblstreet
                             ON tblmaint.usrn = tblstreet.usrn
                         INNER JOIN tlkplocality
                             ON tblstreet.loc_ref = tlkplocality.loc_ref
                         INNER JOIN tlkptown
                             ON tblstreet.town_ref = tlkptown.town_ref
                    WHERE lnkmaint_rd_pol.currency_flag = 0
                        AND tblmaint.currency_flag = 0
                        AND tblstreet.currency_flag = 0
                        """,
            'export_assigned_only': """
                SELECT Asbinary(rdpoly.geometry) AS geom,
                       poly_id, usrn, RefNo, rec_type, descTxt, locality, town,
                       LocTxt, RdStatus, Swa_org, Adopt_Date, Entry_Date, lor_no,
                       route
                FROM maint_records
                    LEFT JOIN rdpoly
                        ON maint_records.poly_id = rdpoly.rd_pol_id
                        """,
            'export_all': """
                SELECT Asbinary(rdpoly.geometry) AS geom,
                       poly_id, usrn, RefNo, rec_type, descTxt, locality, town,
                       LocTxt, RdStatus, Swa_org, Adopt_Date, Entry_Date, lor_no,
                       route
                FROM rdpoly
                    LEFT JOIN maint_records
                        ON maint_records.poly_id = rdpoly.rd_pol_id
                        """}
