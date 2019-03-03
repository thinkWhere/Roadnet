# -*- coding: utf-8 -*-
import datetime

from qgis.core import QgsFeatureRequest, QgsFeature, QgsGeometry
from Roadnet.geometry.edit_handler import EditHandler, DatabaseHandler, IntersectionHandler
from Roadnet.generic_functions import ipdb_breakpoint
import Roadnet.config as config

__author__ = "john.stevenson"


class EsuEditHandler(EditHandler):
    """
    Subclass of EditHandler customised to deal with ESU layer.
    """
    def __init__(self, iface, vlayer, db, params, handle_intersect_flag):
        super(EsuEditHandler, self).__init__(iface, vlayer, db, params,
                                             handle_intersect_flag)
        self.db_handler = EsuDatabaseHandler(vlayer, db)
        self.intersection_handler_class = EsuIntersectionHandler
        if config.DEBUG_MODE:
            print('DEBUG MODE: EsuEditHandler instantiated')


class EsuDatabaseHandler(DatabaseHandler):
    """
    Subclass of DatabaseHandler customised to deal with ESU layer.
    """
    def __init__(self, vlayer, db):
        super(EsuDatabaseHandler, self).__init__(vlayer, db)
        self.esu_id_generator = self.init_esu_id_generator()

    def init_esu_id_generator(self):
        """
        A generator function that yields a unique esu for newly added
        features.
        """
        # Get initial max esu_id
        query = self.run_sql('esu_get_max_esu_id')
        query.first()
        try:
            max_esu_id = int(query.record().value('max_esu_id'))
        except (ValueError, TypeError):
            # Throws if table is empty
            max_esu_id = 0

        # Use value from rdpoly table if that is higher
        query = self.run_sql('tblESU_get_max_esu_id')
        query.first()
        try:
            tbl_esu_max_esu_id = int(query.record().value('max_esu_id'))
        except (ValueError, TypeError):
            # Throws if table is empty
            tbl_esu_max_esu_id = 0
        query = None  # clear query otherwise it locks connection to database

        if tbl_esu_max_esu_id > max_esu_id:
            max_esu_id = tbl_esu_max_esu_id

        while True:  # Generator yields new max_esu_ids as needed.
            max_esu_id += 1
            yield max_esu_id

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
            'tblESU_get_max_esu_id': """
                SELECT MAX(esu_id) AS max_esu_id FROM tblESU
                ;""",
            'esu_get_max_esu_id': """
                SELECT MAX(esu_id) AS max_esu_id FROM esu
                ;""",
            'esu_new_feature': """
                UPDATE esu SET esu_id = {esu_id}, symbol = {symbol}
                WHERE PK_UID IS {pk_uid};""",
            'esu_update_with_parent_symbol': """
                UPDATE esu SET symbol = {parent_symbol}
                WHERE esu_id IS {esu_id};""",
            'tblESU_new_record': """
                INSERT INTO tblESU (esu_id, version_no, currency_flag, xref,
                    yref, entry_date, start_xref, start_yref, end_xref,
                    end_yref, tolerance, parent_esu_id, start_date,
                    update_date)
                VALUES ({esu_id}, 1, 0, {xref}, {yref}, {entry_date}, {startx},
                    {starty}, {endx}, {endy}, 10, NULL, {start_date},
                    {update_date})
                ;""",
            'tblESU_new_record_with_parent': """
                INSERT INTO tblESU (esu_id, version_no, currency_flag, xref,
                    yref, entry_date, start_xref, start_yref, end_xref,
                    end_yref, tolerance, parent_esu_id, start_date,
                    update_date)
                VALUES ({esu_id}, 1, 0, {xref}, {yref}, {entry_date}, {startx},
                    {starty}, {endx}, {endy}, 10, {parent_esu_id}, {start_date},
                    {update_date})
                ;""",
            'tblESU_close_record': """
                UPDATE tblESU
                SET currency_flag = 1, closure_date = {closure_date}
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'tblESU_get_version_no': """
                SELECT version_no FROM tblESU
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'tblESU_copy_skeleton': """
                INSERT INTO tblESU (esu_id, version_no, currency_flag, xref,
                   yref, entry_date, closure_date, start_xref, start_yref,
                   end_xref, end_yref, tolerance, parent_esu_id, gqc, lor_no,
                   private, comments, start_date, update_date)
                SELECT esu_id, NULL, NULL, xref, yref, entry_date,
                   closure_date, NULL, NULL, NULL, NULL, tolerance,
                   parent_esu_id, gqc, lor_no, private, comments, start_date,
                   NULL
                   FROM tblESU
                   WHERE esu_id IS {esu_id}
                   AND currency_flag IS 0
                   ;""",
            'tblESU_make_uncurrent': """
                UPDATE tblESU SET currency_flag = 1
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'tblESU_fill_skeleton': """
                UPDATE tblESU SET version_no = {version_no}, currency_flag = 0,
                    start_xref = {startx}, start_yref = {starty},
                    end_xref = {endx}, end_yref = {endy},
                    update_date = '{update_date}'
                WHERE esu_id IS {esu_id}
                AND currency_flag IS NULL
                ;""",
            'tblESU_unique_midpoint': """
                SELECT COUNT() FROM tblESU
                WHERE xref = {xref} AND yref = {yref}
                ;""",
            'lnkESU_STREET_close_records': """
                UPDATE lnkESU_STREET
                SET currency_flag = 1, closure_date = {closure_date}
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'lnkESU_STREET_get_version_no': """
                SELECT esu_version_no FROM lnkESU_STREET
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'lnkESU_STREET_get_usrn_list': """
                SELECT DISTINCT usrn FROM lnkESU_STREET
                WHERE esu_id IS {parent_esu_id}
                AND esu_version_no IS (SELECT MAX(esu_version_no)
                                       FROM lnkESU_STREET
                                       WHERE esu_id IS {parent_esu_id})
                AND currency_flag IS 0
                ;""",
            'lnkESU_STREET_count_parent_records': """
                SELECT COUNT(esu_id) AS 'parent_record_count'
                FROM lnkESU_STREET
                WHERE esu_id IS {parent_esu_id}
                ;""",
            'lnkESU_STREET_get_parent_record': """
                SELECT esu_id, usrn, esu_version_no,
                      usrn_version_no, currency_flag, entry_date, update_date,
                      closure_date
                FROM lnkESU_STREET
                WHERE esu_id IS {parent_esu_id}
                AND usrn IS {usrn}
                AND esu_version_no IS (SELECT MAX(esu_version_no)
                                       FROM lnkESU_STREET
                                       WHERE esu_id IS {parent_esu_id}
                                       AND usrn IS {usrn})
                AND usrn_version_no IS (SELECT MAX(usrn_version_no)
                                       FROM lnkESU_STREET
                                       WHERE esu_id IS {parent_esu_id}
                                       AND usrn IS {usrn})
                ;""",
            'lnkESU_STREET_close_parent_record': """
                UPDATE lnkESU_STREET SET currency_flag = 1,
                      closure_date = {closure_date}
                WHERE esu_id IS {parent_esu_id}
                AND usrn IS {usrn}
                AND esu_version_no IS {esu_version_no}
                AND usrn_version_no IS {usrn_version_no}
                ;""",
            'lnkESU_STREET_new_record_with_parent': """
                INSERT INTO lnkESU_STREET (esu_id, usrn, esu_version_no,
                      usrn_version_no, currency_flag, entry_date, update_date,
                      closure_date)
                VALUES ({esu_id}, {usrn}, 1, {usrn_version_no}, 0,
                      {entry_date}, {update_date}, NULL)
                      ;""",
            'lnkESU_STREET_copy_skeleton': """
                INSERT INTO lnkESU_STREET (esu_id, usrn, esu_version_no,
                       usrn_version_no, currency_flag, entry_date, update_date,
                       closure_date)
                SELECT esu_id, usrn, NULL, usrn_version_no, NULL,
                       entry_date, NULL, closure_date
                       FROM lnkESU_STREET
                       WHERE esu_id IS {esu_id}
                       AND currency_flag IS 0
                       ;""",
            'lnkESU_STREET_make_uncurrent': """
                UPDATE lnkESU_STREET SET currency_flag = 1
                WHERE esu_id IS {esu_id}
                AND currency_flag IS 0
                ;""",
            'lnkESU_STREET_fill_skeleton': """
                UPDATE lnkESU_STREET SET esu_version_no = {esu_version_no},
                    currency_flag = 0, update_date = '{update_date}'
                WHERE esu_id IS {esu_id}
                AND currency_flag IS NULL
                ;"""
            }

    def add_feature(self, feature):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        esu_id = self.esu_id_generator.next()
        symbol = 0
        (startx, starty), (endx, endy) = self.get_start_end_xy(feature)
        xref, yref = self.get_unique_midpoint(feature)

        args = {'esu_id': esu_id, 'xref': xref, 'yref': yref,
                'entry_date': today, 'startx': startx, 'starty': starty,
                'endx': endx, 'endy': endy, 'start_date': today,
                'update_date': today, 'symbol': symbol,
                'pk_uid': feature.id()}

        # Run queries
        self.run_sql('esu_new_feature', args)
        self.run_sql('tblESU_new_record', args)

    def add_feature_parent(self, feature, parent_fid):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        esu_id = self.esu_id_generator.next()
        parent_esu_id = self.original_attributes[parent_fid]['esu_id']
        parent_symbol = self.original_attributes[parent_fid]['symbol']
        symbol = 0
        (startx, starty), (endx, endy) = self.get_start_end_xy(feature)
        xref, yref = self.get_unique_midpoint(feature)

        args = {'esu_id': esu_id, 'xref': xref, 'yref': yref,
                'entry_date': today, 'startx': startx, 'starty': starty,
                'endx': endx, 'endy': endy, 'start_date': today,
                'update_date': today, 'symbol': symbol,
                'pk_uid': feature.id(), 'parent_esu_id': parent_esu_id,
                'parent_symbol': parent_symbol, 'closure_date': today}

        # Check if parent has records in lnkESU_STREET
        query = self.run_sql('lnkESU_STREET_count_parent_records', args)
        query.first()
        parent_record_count = int(query.record().value('parent_record_count'))
        if parent_record_count > 0:
            lnk_esu_street_records_exist = True
        else:
            lnk_esu_street_records_exist = False

        # Run queries
        self.run_sql('esu_new_feature', args)
        self.run_sql('tblESU_new_record_with_parent', args)
        if lnk_esu_street_records_exist:
            self.update_lnk_esu_street_records_with_parents(args)
            self.run_sql('esu_update_with_parent_symbol', args)

    def update_lnk_esu_street_records_with_parents(self, args):
        """
        Find all USRNs linked to ESU, then update with parents.
        :param args: Dictionary of arguments for SQL queries.
        """
        # Find usrns linked to ESU
        query = self.run_sql('lnkESU_STREET_get_usrn_list', args)
        usrns = []
        while query.next():
            record = query.record()
            usrns.append(int(record.value('usrn')))

        for usrn in usrns:
            # Get updated arguments
            args.update({'usrn': usrn})
            query = self.run_sql('lnkESU_STREET_get_parent_record', args)
            query.first()
            esu_version_no = int(query.record().value('esu_version_no'))
            usrn_version_no = int(query.record().value('usrn_version_no'))
            try:
                entry_date = int(query.record().value('entry_date'))
            except TypeError:
                # Throws if entry date not set in database
                entry_date = 'NULL'
            extra_args = {'esu_version_no': esu_version_no,
                          'usrn_version_no': usrn_version_no,
                          'entry_date': entry_date}
            args.update(extra_args)

            # Update database
            self.run_sql('lnkESU_STREET_new_record_with_parent', args)

    def change_geometry(self, fid, geometry):
        # Collect input data
        feature = self.vlayer.getFeatures(
            QgsFeatureRequest().setFilterFid(fid)).next()
        today = datetime.datetime.now().strftime("%Y%m%d")
        (startx, starty), (endx, endy) = self.get_start_end_xy(feature)
        esu_id = self.original_attributes[fid]['esu_id']
        args = {'esu_id': esu_id}

        query = self.run_sql('tblESU_get_version_no', args)
        query.first()
        version_no = int(query.record().value('version_no'))

        query = self.run_sql('lnkESU_STREET_get_version_no', args)
        query.first()
        try:
            esu_version_no = int(query.record().value('esu_version_no'))
            lnk_esu_street_record_exists = True
        except TypeError:
            # If ESU has no records yet, e.g is new, esu_version_no is empty
            lnk_esu_street_record_exists = False
            esu_version_no = 0  # dummy value that isn't used

        args = {'version_no': version_no + 1,
                'esu_version_no': esu_version_no + 1,
                'startx': startx, 'starty': starty,
                'endx': endx, 'endy': endy, 'update_date': today,
                'closure_date': today, 'esu_id': esu_id}

        # Run queries
        self.run_sql('tblESU_copy_skeleton', args)
        self.run_sql('tblESU_make_uncurrent', args)
        self.run_sql('tblESU_fill_skeleton', args)
        if lnk_esu_street_record_exists:
            self.run_sql('lnkESU_STREET_copy_skeleton', args)
            self.run_sql('lnkESU_STREET_make_uncurrent', args)
            self.run_sql('lnkESU_STREET_fill_skeleton', args)

    def delete_feature(self, fid):
        # Collect input data
        today = datetime.datetime.now().strftime("%Y%m%d")
        args = {'esu_id': self.original_attributes[fid]['esu_id'],
                'closure_date': today}
        # Run queries
        self.run_sql('tblESU_close_record', args)
        self.run_sql('lnkESU_STREET_close_records', args)

    @staticmethod
    def get_start_end_xy(feature):
        """
        Return the start and end coordinates for a MultiPolyLine geometry
        :param feature: QgsFeature
        :return: (startx, starty), (endx, endy)
        """
        geometry = feature.geometry()
        # Check for multipart as geom is dealt with differently
        if geometry.isMultipart():
            multipolyline = geometry.asMultiPolyline()
            start = multipolyline[0][0]
            end = multipolyline[0][-1]
        else:
            linegeom = geometry.asPolyline()
            start = linegeom[0]
            end = linegeom[1]
        startx, starty = [round(coord, 2) for coord in start]
        endx, endy = [round(coord, 2) for coord in end]
        return (startx, starty), (endx, endy)

    def get_unique_midpoint(self, feature):
        """
        Get the midpoint of a line, which must be different from others within
        the table as it is used as an id.
        :param feature: QgsFeature
        :rtype : int int
        :return: Unique xref and yref (midpoint)
        """
        # Get actual midpoint
        centroid = feature.geometry().centroid()
        x, y = [int(round(coord)) for coord in centroid.asPoint()]

        # Increment coordinates by 1 metre until combination is unique.
        while True:
            args = {'xref': x, 'yref': y}
            query = self.run_sql('tblESU_unique_midpoint', args)
            query.first()
            if int(query.value(0)) == 0:  # No matching records found
                query = None     # clear query otherwise it locks connection to database
                break
            else:
                x += 1
                y += 1
        return x, y


class EsuIntersectionHandler(IntersectionHandler):
    """
    Splits features that intersect a given feature and stores information on
    the deleted and newly-added features.  Customised for ESUs.
    """
    def __init__(self, iface, vlayer, fid):
        """
        Class is instantiated for each feature that has intersections with
        another feature in its layer.  fid is ID of my_feature.
        """
        super(EsuIntersectionHandler, self).__init__(iface, vlayer,
                                                     fid)
        if config.DEBUG_MODE:
            print('DEBUG MODE: EsuIntersectionHandler instantiated')

    def handle_my_feature(self):
        """
        Handle intersection and populate list of children derived from the
        original features.
        """
        fid = self.my_feature.id()
        my_geometry = QgsGeometry(self.my_feature.geometry())
        if config.DEBUG_MODE:
            print('Modifying my_feature {} '
                  'with original length {}'.format(fid, my_geometry.length()))

        # Delete user-drawn feature
        provider = self.vlayer.dataProvider()
        result = provider.deleteFeatures([fid])
        if not result:
            raise Exception('Could not delete feature.')

        # Split my geometry into parts around intersections
        parts = self.update_my_feature_geometry(my_geometry)

        # Create new features from parts
        future_features = []
        for part in parts:
            future_feature = QgsFeature(self.vlayer.pendingFields())
            future_feature.setGeometry(part)
            future_features.append(future_feature)

        # Add new features to layer
        result, new_features = provider.addFeatures(future_features)
        self.added_features['new'] = new_features

    def update_my_feature_geometry(self, my_geometry):
        """
        Change the geometry by interaction with victims.
        :param my_geometry: geometry to be updated
        :return parts: list of QgsGeometry objects
        """
        victim_geometries = [v.geometry() for v in self.victims]
        parts = self.split_line(my_geometry, victim_geometries)
        return parts

    def handle_victims(self):
        """
        Handle intersection and populate list of children derived from the
        victims.
        """
        provider = self.vlayer.dataProvider()
        for victim in self.victims:
            if config.DEBUG_MODE:
                print('Modifying victim {}'.format(victim.id()))

            # Delete original feature
            fid = victim.id()
            result = provider.deleteFeatures([fid])
            if not result:
                raise Exception('Could not delete feature.')
            self.deleted_feature_ids.append(fid)

            # Create future features from parts
            victim_geometry = victim.geometry()
            parts = self.update_victim_geometry(victim_geometry)
            future_features = []

            for part in parts:
                future_feature = QgsFeature(self.vlayer.pendingFields())
                future_feature.setGeometry(part)
                # Copy attributes from victim feature
                field_map = provider.fieldNameMap()
                for key in field_map:
                    if key != 'PK_UID':
                        future_feature[key] = victim[key]
                future_features.append(future_feature)

            # Add new features to layer
            result, new_features = provider.addFeatures(future_features)
            self.added_features[fid] = new_features

    def update_victim_geometry(self, victim_geometry):
        """
        Change the geometry by interaction with my_feature.
        :param victim_geometry: geometry to be updated
        :return parts: updated geometry
        """
        # Use QgsGeometry to make a separate copy of the feature geometry
        my_geometry = QgsGeometry(self.my_feature.geometry())
        parts = self.split_line(victim_geometry, [my_geometry])
        return parts

    @staticmethod
    def split_line(my_geometry, other_line_geometries):
        """

        Split a line geometry into multiple parts at intersections
        with other lines.

        :param my_geometry: QgsGeometry to split
        :param other_line_geometries: List of QgsGeometries to split against
        :return parts: list of QgsGeometry objects
        """
        def to_points(geometry):
            # Function is defined here so that method can be static without
            # any reference to self.
            if geometry.isMultipart():
                points = []
                lines = geometry.asMultiPolyline()
                for line in lines:
                    points.extend(line)
            else:
                points = geometry.asPolyline()
            return points

        parts = [my_geometry]
        while len(other_line_geometries) > 0:
            other_line_geometry = other_line_geometries.pop()

            for part in parts:
                (result, new_parts, topology_points) = part.splitGeometry(
                    to_points(other_line_geometry), False)

                if result == 0:
                    # 0 is success. Skip to next part if splitting failed
                    parts.extend(new_parts)

        # Strip out tiny parts that are sometimes created.
        parts = [part for part in parts if part.length() > 0.01]

        return parts
