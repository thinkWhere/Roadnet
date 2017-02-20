# -*- coding: utf-8 -*-
import datetime

from qgis.core import QgsFeatureRequest, QgsFeature, QgsGeometry
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox

from edit_handler import (EditHandler,
                          DatabaseHandler,
                          IntersectionHandler,
                          IntersectionHandlerError)
from Roadnet.generic_functions import ipdb_breakpoint
from Roadnet import config

__author__ = "john.stevenson"


class RdpolyEditHandler(EditHandler):
    """
    Subclass of EditHandler customised to deal with RdPoly layer.
    """
    def __init__(self, iface, vlayer, db, params, handle_intersect_flag):
        super(RdpolyEditHandler, self).__init__(iface, vlayer, db, params,
                                                handle_intersect_flag)
        self.db_handler = RdpolyDatabaseHandler(vlayer, db)
        self.intersection_handler_class = RdpolyIntersectionHandler
        if config.DEBUG_MODE:
            print('DEBUG MODE: RdpolyEditHandler instantiated')

    def feature_deleted(self, fid):
        """
        Check if OK to delete feature (e.g. feature not connected to records).
        If not, show warning and undo deletion.
        """
        if config.DEBUG_MODE:
            print('Feature {} deleted'.format(fid))
        if fid < 0:
            # Ignore temporary features deleted by undo operations
            return
        self.warn_if_linked_maintenance(fid)

    def warn_if_linked_maintenance(self, fid):
        # Check for linked maintenance records
        rd_pol_id = self.db_handler.original_attributes[fid]['rd_pol_id']
        args = {'rd_pol_id': rd_pol_id}
        query = self.db_handler.run_sql('count_maintenance_links', args)
        query.first()
        link_count = int(query.record().value('link_count'))

        if link_count > 0:
            warning = ('Warning: rd_pol_id {} was deleted.  Polygon has '
                       '{} maintenance record link(s). Undo last delete '
                       'to preserve database integrity.'.format(rd_pol_id, link_count))
            msg_box = QMessageBox(QMessageBox.Warning, "roadNet",
                                  warning,
                                  QMessageBox.Ok, None, Qt.CustomizeWindowHint)
            msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            msg_box.exec_()


class RdpolyDatabaseHandler(DatabaseHandler):
    """
    Subclass of DatabaseHandler customised to deal with RdPoly layer.
    """
    def __init__(self, vlayer, db):
        super(RdpolyDatabaseHandler, self).__init__(vlayer, db)
        self.rd_pol_id_generator = self.init_rd_pol_id_generator()

    def init_rd_pol_id_generator(self):

        """
        A generator function that yields a unique rd_poly for newly added
        features.
        """
        # Set initial max rd_pol_id
        query = self.run_sql('tblRD_POL_get_max_rd_pol_id')
        query.first()
        try:
            max_rd_pol_id = int(query.record().value('max_rd_pol_id'))
        except (ValueError, TypeError):
            # Error throws if table is empty
            max_rd_pol_id = 0

        # Use value from rdpoly table if that is higher
        query = self.run_sql('rdpoly_get_max_rd_pol_id')
        query.first()
        try:
            rdpoly_max_rd_pol_id = int(query.record().value('max_rd_pol_id'))
        except (ValueError, TypeError):
            # Error throws if table is empty
            rdpoly_max_rd_pol_id = 0
        query = None  # clear query otherwise it locks connection to database

        if rdpoly_max_rd_pol_id > max_rd_pol_id:
            max_rd_pol_id = rdpoly_max_rd_pol_id

        while True:  # Generator yields new rd_pol_ids as needed.
            max_rd_pol_id += 1
            yield max_rd_pol_id

    def delete_feature(self, fid):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        rd_pol_id = self.original_attributes[fid]['rd_pol_id']
        args = {'today': today, 'rd_pol_id': rd_pol_id}

        # Run query
        query = self.run_sql('tblRD_POL_delete_feature', args)

    def add_feature(self, feature):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        rd_pol_id = self.rd_pol_id_generator.next()
        symbol = 'NULL'  # Default symbol for unassigned
        args = {'rd_pol_id': rd_pol_id, 'symbol': symbol,
                'pk_uid': feature.id(), 'entry_date': today}

        # Run query
        query = self.run_sql('rdpoly_new_feature', args)
        query = self.run_sql('tblRD_POL_new_feature', args)

    def add_feature_parent(self, feature, parent_fid):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        rd_pol_id = self.rd_pol_id_generator.next()
        parent_rd_pol_id = self.original_attributes[parent_fid]['rd_pol_id']
        symbol = 'NULL'  # Default symbol for unassigned
        args = {'rd_pol_id': rd_pol_id, 'symbol': symbol,
                'parent_rd_pol_id': parent_rd_pol_id,
                'pk_uid': feature.id(), 'entry_date': today}

        # Run query
        query = self.run_sql('rdpoly_new_feature', args)
        query = self.run_sql('tblRD_POL_new_feature_parent', args)

    def change_geometry(self, fid, geometry):
        # Collect input data
        feature = self.vlayer.getFeatures(
            QgsFeatureRequest().setFilterFid(fid)).next()
        rd_pol_id = feature['rd_pol_id']
        args = {'rd_pol_id': rd_pol_id}

        query = self.run_sql('tblRD_POL_get_version_no', args)
        query.first()
        version_no = int(query.record().value('version_no'))

        args = {'rd_pol_id': rd_pol_id,
                'version_no': version_no + 1}

        # Run query
        query = self.run_sql('tblRD_POL_copy_skeleton', args)
        query = self.run_sql('tblRD_POL_make_uncurrent', args)
        query = self.run_sql('tblRD_POL_fill_skeleton', args)

    def prepare_sql_queries(self):
        """
        Populates internal dictionary of sql queries.  Queries should use named
        string.format() type fields that are populated via a dictionary when
        used.
        """
        self.sql_queries = {
            'invalidate_old_statistics': """
                UPDATE geometry_columns_statistics SET last_verified = 0
                ;""",
            'update_statistics': """
                SELECT UpdateLayerStatistics()
                ;""",
            'tblRD_POL_get_max_rd_pol_id': """
                SELECT MAX(rd_pol_id) AS max_rd_pol_id FROM tblRD_POL;""",
            'rdpoly_get_max_rd_pol_id': """
                SELECT MAX(rd_pol_id) AS max_rd_pol_id FROM rdpoly;""",
            'tblRD_POL_delete_feature': """
                UPDATE tblRD_POL
                SET currency_flag=1, closure_date={today}
                WHERE rd_pol_id = {rd_pol_id}
                AND currency_flag = 0""",
            'count_maintenance_links': """
                SELECT COUNT(maint_id) AS link_count FROM lnkMAINT_RD_POL
                WHERE rd_pol_id = {rd_pol_id} AND currency_flag = 0;""",
            'rdpoly_new_feature': """
                UPDATE rdpoly SET rd_pol_id = {rd_pol_id}, symbol = {symbol},
                currency_flag = 0
                WHERE PK_UID IS {pk_uid};""",
            'tblRD_POL_new_feature': """
                INSERT INTO tblRD_POL (rd_pol_id, currency_flag, entry_date,
                    version_no)
                VALUES ({rd_pol_id}, 0, {entry_date}, 1);""",
            'tblRD_POL_new_feature_parent': """
                INSERT INTO tblRD_POL (rd_pol_id, currency_flag, entry_date,
                    version_no, parent_rd_pol_id)
                VALUES ({rd_pol_id}, 0, {entry_date}, 1, {parent_rd_pol_id})
                ;""",
            'tblRD_POL_copy_skeleton': """
                INSERT INTO tblRD_POL (rd_pol_id, xref, yref, currency_flag,
                    entry_date, version_no, parent_rd_pol_id, comments,
                    closure_date)
                SELECT rd_pol_id, NULL, NULL, NULL, entry_date, NULL,
                    parent_rd_pol_id, comments, closure_date
                FROM tblRD_POL
                WHERE rd_pol_id IS {rd_pol_id}
                AND currency_flag IS 0
                ;""",
            'tblRD_POL_make_uncurrent': """
                UPDATE tblRD_POL SET currency_flag = 1
                WHERE rd_pol_id IS {rd_pol_id}
                AND currency_flag IS 0
                ;""",
            'tblRD_POL_fill_skeleton': """
                UPDATE tblRD_POL SET version_no = {version_no},
                    currency_flag = 0
                WHERE rd_pol_id IS {rd_pol_id}
                AND currency_flag IS NULL
                ;""",
            'tblRD_POL_get_version_no': """
                SELECT version_no FROM tblRD_POL
                WHERE rd_pol_id IS {rd_pol_id}
                AND currency_flag IS 0
                ;"""}


class RdpolyIntersectionHandler(IntersectionHandler):
    """
    Splits features that intersect a given feature and stores information on
    the deleted and newly-added features.
    """
    def __init__(self, iface, vlayer, fid):
        """
        Class is instantiated for each feature that has intersections with
        another feature in its layer.  fid is ID of my_feature.
        """
        super(RdpolyIntersectionHandler, self).__init__(iface, vlayer,
                                                        fid)
        if config.DEBUG_MODE:
            print('DEBUG MODE: RpolyIntersectionHandler instantiated')

    def handle_my_feature(self):
        """
        Handle intersection and populate list of children derived from the
        original features.  For rdpoly, previously existing features are
        subtracted from my_feature.
        """
        fid = self.my_feature.id()
        my_geometry = self.my_feature.geometry()
        if config.DEBUG_MODE:
            print('Modifying my_feature {} with original area {}'.format(
                  fid, my_geometry.area()))

        # Calculate new geometry
        new_geometry = self.update_my_feature_geometry(my_geometry)

        # Delete user-drawn feature
        provider = self.vlayer.dataProvider()
        result = provider.deleteFeatures([fid])

        # Create new feature
        new_feature = QgsFeature(self.vlayer.pendingFields())
        new_feature.setGeometry(new_geometry)

        # Add new feature
        result, new_features = provider.addFeatures([new_feature])
        self.added_features['new'] = new_features

    def update_my_feature_geometry(self, geometry):
        """
        Change the geometry by interaction with victims.
        :param geometry: geometry to be updated
        """
        for victim in self.victims:
            # Cut out overlaps with victim features
            if config.DEBUG_MODE:
                print('Processing against victim {}'.format(victim.id()))
            geometry = geometry.difference(victim.geometry())

        # Drop tiny geometry parts
        clean_geometry = self.clean_up_geometry(geometry)

        # Don't allow features that have multiple non-tiny parts
        number_of_parts = len(clean_geometry.asMultiPolygon())
        if number_of_parts > 1:
            self.display_multipart_warning()
            fid = self.my_feature.id()
            msg = "Feature {} intersections created multipart geometries".format(fid)
            raise IntersectionHandlerError(msg)

        return clean_geometry

    @staticmethod
    def clean_up_geometry(geometry):
        """
        Convert to multiPolygon geometry with 'tiny' geometries removed
        :param geometry: geometry to be updated
        :return clean_geometry: multipart geometry with tiny parts removed
        """
        geometry.convertToMultiType()  # required by later sections
        parts = geometry.asMultiPolygon()
        non_tiny_parts = []

        # Find parts with non-tiny area
        for part in parts:
            area = QgsGeometry.fromPolygon(part).area()
            if area > 0.01:
                non_tiny_parts.append(part)
            else:
                if config.DEBUG_MODE:
                    print("DEBUG_MODE: discarding tiny geometry ({} m^2)".format(area))

        # Raise error if all parts are tiny
        if len(non_tiny_parts) == 0:
            msg = "Intersections created only tiny geometry"
            raise IntersectionHandlerError(msg)

        # A multiPolygon is just a list of polygons
        clean_geometry = QgsGeometry.fromMultiPolygon(non_tiny_parts)

        return clean_geometry

    def display_multipart_warning(self):
        """
        Show warning about multipart feature, depending of whether created
        as new feature or by modification.
        """
        message = ('Intersection would have created a multipart feature, so was not processed.  '
                   'Please delete feature and redraw.'
                   )
        self.iface.messageBar().pushMessage('roadNet',
                                            message,
                                            QgsMessageBar.CRITICAL,
                                            0)
