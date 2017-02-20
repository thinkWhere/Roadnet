# -*- coding: utf-8 -*-
import pprint
from PyQt4.QtSql import QSqlQuery

from qgis.core import QgsFeatureRequest, QGis
from qgis.gui import QgsMessageBar
from Roadnet.generic_functions import ipdb_breakpoint
import Roadnet.config as config

__author__ = "john.stevenson"


class EditHandler(object):
    """
    Listen for geometry edit signals on vector layer 'vlayer' and call helpers
    to process database updates and feature intersections.
    """

    _edit_buffer = None

    def __init__(self, iface, vlayer, db, params, handle_intersect_flag):
        """
        Class is instantiated at beginning of editing session, and also after
        each time that user saves changes.
        """
        self.iface = iface
        self.vlayer = vlayer
        self.db_handler = DatabaseHandler(vlayer, db)
        self.params = params
        self.handle_intersect_flag = handle_intersect_flag

        self.node_tool = iface.actionNodeTool()
        if self.node_tool.isChecked():
            self.node_tool.toggle()

        self.connect_eb_signals()
        self.connect_commits_signals()
        self.intersection_handler_class = IntersectionHandler
        self.current_edits_include_intersection = False
        if config.DEBUG_MODE:
            print('DEBUG MODE: Generic EditHandler instantiated.')

    @property
    def edit_buffer(self):
        if self._edit_buffer is None:
            self._edit_buffer = self.vlayer.editBuffer()
        return self._edit_buffer

    def connect_eb_signals(self):
        """
        Connect signals for real-time editing events
        """
        try:
            self.edit_buffer.featureAdded.connect(self.feature_added)
            self.edit_buffer.geometryChanged.connect(self.geometry_changed)
            self.edit_buffer.featureDeleted.connect(self.feature_deleted)
            self.vlayer.beforeCommitChanges.connect(self.disconnect_eb_signals)
            self.vlayer.beforeRollBack.connect(self.disconnect_eb_signals)
            self.node_tool.toggled.connect(self.warn_if_node_tool)
        except AttributeError:
            # Catches exceptions thrown by the Symbology update tool
            pass

    def connect_commits_signals(self):
        """
        Connect signals for committed editing events.
        """
        self.vlayer.committedFeaturesAdded.connect(self.adds_committed)
        self.vlayer.committedGeometriesChanges.connect(self.changes_committed)
        self.vlayer.committedFeaturesRemoved.connect(self.deletes_committed)

    def adds_committed(self, layer_id, added_features):
        """
        Coordinate database and updates when added geometries are committed.
        :param layer_id: Layer ID is passed by committed adds signal
        :param added_features: Passed by committed adds signal
        """
        if config.DEBUG_MODE:
            print('Committed features added to layer {}.'.format(layer_id))
        for feature in added_features:
            fid = feature.id()
            if self.handle_intersect_flag is False or \
                    self.check_for_intersections(fid) is False:
                self.db_handler.add_feature(feature)
                continue

            # Handle features added and deleted by intersection
            if config.DEBUG_MODE:
                print('Handling intersections for committed added feature')
            try:
                self.handle_intersections(fid, is_modify=False)
            except IntersectionHandlerError as e:
                # Log error and continue.  Database should be unchanged at this point.
                if config.DEBUG_MODE:
                    print e.args[0]

    def changes_committed(self, layer_id, changed_geometries):
        """
        Coordinate database and updates when changes in geometry are committed.
        :param layer_id: Layer ID is passed by committed changes signal
        :param changed_geometries: Passed by committed changes signal
        """
        if config.DEBUG_MODE:
            print('Committed geometries changed in layer {}.'.format(layer_id))
        for fid in changed_geometries:
            feature = self.vlayer.getFeatures(
                QgsFeatureRequest().setFilterFid(fid)).next()

            # Just update database if intersections are ignored
            if self.handle_intersect_flag is False:
                self.db_handler.change_geometry(fid, feature.geometry())
                continue

            # Just update database if there are no intersections
            if self.check_for_intersections(feature.id()) is False:
                self.db_handler.change_geometry(fid, feature.geometry())
                continue

            # Handle features added and deleted by intersection
            if config.DEBUG_MODE:
                print('Handling intersections for committed changed feature')
            try:
                self.handle_intersections(fid, is_modify=True)
            except IntersectionHandlerError as e:
                # Log error and continue.  Database should be unchanged at this point.
                if config.DEBUG_MODE:
                    print e.args[0]

    def handle_intersections(self, fid, is_modify=False):
        """
        Launch an intersect handler to process feature by id.  Performs
        database updates for newly created/deleted features.
        :param fid: ID of feature to process
        :param is_modify: boolean.  Set True if intersection cause by
            geometry change.
        :return:
        """
        # Launch intersection handler and get changed features
        intersect_handler = self.intersection_handler_class(
            self.iface, self.vlayer, fid)
        intersect_handler.handle_intersections()
        added_features = intersect_handler.get_added_features()
        deleted_feature_ids = intersect_handler.get_deleted_feature_ids()

        # For a modification, the 'new' feature is actually an old one.
        if is_modify:
            if config.DEBUG_MODE:
                print('DEBUG MODE: setting {} as parent of "new"'.format(fid))
            added_features[fid] = added_features['new']
            del added_features['new']
            deleted_feature_ids.append(fid)

        # Process newly added features
        for parent_fid in added_features.keys():
            if parent_fid == 'new':
                # Features derived from a newly added feature
                for added_feature in added_features[parent_fid]:
                    self.db_handler.add_feature(added_feature)
            else:
                # Features derived from pre-existing features.
                for added_feature in added_features[parent_fid]:
                    self.db_handler.add_feature_parent(added_feature, parent_fid)

        # Process deleted features
        for deleted_fid in deleted_feature_ids:
            self.db_handler.delete_feature(deleted_fid)

    def deletes_committed(self, layer_id, deleted_fids):
        """
        Coordinate database and updates when deletions are committed.
        :param layer_id: Layer ID is passed by committed deletes signal
        :param deleted_fids: Passed by committed deletes signal
        """
        if config.DEBUG_MODE:
            print('Committed features deleted from layer {}.'.format(layer_id))
        for fid in deleted_fids:
            self.db_handler.delete_feature(fid)

    def feature_added(self, fid):
        """
        Check new feature for intersections and warn if found.
        :param fid: Feature ID
        """
        if config.DEBUG_MODE:
            print('Feature {} added'.format(fid))
        if self.handle_intersect_flag is True:
            self.warn_if_intersections(fid)

    def geometry_changed(self, fid, geometry):
        """
        Check changed feature for intersections and warn if found.
        :param fid: Feature ID
        :param geometry: QgsGeometry for changed feature
        """
        if config.DEBUG_MODE:
            print('Feature {} geometry changed. {}'.format(fid, geometry))
        if self.handle_intersect_flag is True:
            self.warn_if_intersections(fid)

    def warn_if_intersections(self, fid):
        """
        Show warning message if feature intersects another.
        """
        if self.check_for_intersections(fid) is False:
            return

        # Intersection with uncommitted feature is critical warning
        if self.has_uncommitted_victims(fid):
            warning = ('Intersections with unsaved features cannot be '
                       'processed correctly. Intersecting features should '
                       'be added one at a time, then saved. '
                       'Undo last change before continuing.')
            self.iface.messageBar().pushMessage('roadNet',
                                                warning,
                                                QgsMessageBar.CRITICAL,
                                                9)
            return

        # Intersection multiple times without saving is asking for trouble
        if self.current_edits_include_intersection is True:
            warning = ('Current edit session includes multiple intersecting '
                       'features. Intersecting features should '
                       'be added one at a time, then saved. '
                       'Undo last change before continuing.')
            self.iface.messageBar().pushMessage('roadNet',
                                                warning,
                                                QgsMessageBar.WARNING,
                                                8)
            return

        # Intersection with existing feature is more common
        self.current_edits_include_intersection = True
        warning = ('Intersection detected. Intersecting features should '
                   'be added one at a time.  Save changes to update '
                   'database before further edits, or undo last change.')
        self.iface.messageBar().pushMessage('roadNet',
                                            warning,
                                            QgsMessageBar.INFO,
                                            5)

    def check_for_intersections(self, fid):
        """
        Check if new / changed feature intersects existing features.
        :param fid: Feature ID
        :return boolean:
        """
        if config.DEBUG_MODE:
            print('DEBUG_MODE: Checking for intersections on '
                  'feature {}'.format(fid))
        my_feature = self.vlayer.getFeatures(
            QgsFeatureRequest().setFilterFid(fid)).next()
        victims = find_intersections(my_feature, self.vlayer)

        if len(victims) > 0:
            return True
        else:
            return False

    def has_uncommitted_victims(self, fid):
        """
        Checks if intersections are with features that haven't
        been committed yet.
        :param fid: Feature ID
        """
        my_feature = self.vlayer.getFeatures(
            QgsFeatureRequest().setFilterFid(fid)).next()
        if config.DEBUG_MODE:
            print("DEBUG_MODE: Checking for uncommitted victims.")
        victims = find_intersections(my_feature, self.vlayer)

        # Set warning flag for intersection with uncommitted victims
        uncommitted_victims = [v for v in victims if v.id() < 0]

        if len(uncommitted_victims) > 0:
            return True
        else:
            return False

    def feature_deleted(self, fid):
        """
        Check if OK to delete feature (e.g. feature not connected to records).
        If not, show warning and undo deletion.
        :param fid: Feature ID
        """
        if config.DEBUG_MODE:
            print('Feature {} deleted'.format(fid))

    def disconnect_eb_signals(self):
        """
        Disconnect signals for real time editing events
        """
        self.edit_buffer.featureAdded.disconnect()
        self.edit_buffer.geometryChanged.disconnect()
        self.edit_buffer.featureDeleted.disconnect()
        self.vlayer.beforeCommitChanges.disconnect()
        self.vlayer.beforeRollBack.disconnect()

    def disconnect_commits_signals(self):
        """
        Disconnect signals for committed editing events.
        """
        self.vlayer.committedFeaturesAdded.disconnect()
        self.vlayer.committedGeometriesChanges.disconnect()
        self.vlayer.committedFeaturesRemoved.disconnect()

    def warn_if_node_tool(self, toggle_state):
        """
        Show warning if node tool is used in QGIS 2.8.  Using it can cause hard crashes
        when editing already edited features.
        :param toggle_state: boolean sent by the signal.
        """
        if QGis.QGIS_VERSION_INT > 20900:
            # Problem doesn't affect new versions
            return

        if self.params['session_includes_edits'] is False:
            # Problem doesn't arise until changes have been saved
            return

        if toggle_state is False:
            # Don't warn when leaving node tool
            return

        # This section allows demonstration of disabled tool
        disable_node_tool = False
        if disable_node_tool:
            self.node_tool.setDisabled(True)

        warning = ('QGIS 2.8 node tool is unstable.\n\nEditing features '
                   'created or changed in this roadNet session WILL CAUSE '
                   'QGIS TO CRASH.\n\nLog out and log in before editing '
                   'nodes in these features.  This bug will be fixed in QGIS '
                   '2.14.')
        self.iface.messageBar().pushMessage('roadNet',
                                            warning,
                                            QgsMessageBar.CRITICAL,
                                            9)
        return


class DatabaseHandler(object):
    """
    Run SQL commands to update database tables following edits.
    """

    def __init__(self, vlayer, db):
        self.vlayer = vlayer
        self.db = db
        self.original_attributes = self.get_original_attributes()
        self.sql_queries = {}
        self.prepare_sql_queries()

    def get_original_attributes(self):
        """
        Create dictionary of attributes as found at start of editing.  This is
        used to retrieve information about deleted features via:

        self.original_attributes[fid][attribute_col]
        """
        original_attributes = {}
        attribute_cols = [f.name() for f in self.vlayer.pendingFields()]
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

        for feature in self.vlayer.getFeatures(request):
            attributes = feature.attributes()
            attribute_dict = {attribute_cols[i]: attributes[i]
                              for i in range(len(attributes))}
            original_attributes[feature.id()] = attribute_dict

        return original_attributes

    def add_feature(self, feature):
        if config.DEBUG_MODE:
            print('SQL for added feature {}'.format(feature.id()))

    def add_feature_parent(self, feature, parent_fid):
        if config.DEBUG_MODE:
            print('SQL for added feature {} with parent {}'.format(
                feature.id(), parent_fid))

    def change_geometry(self, fid, geometry):
        if config.DEBUG_MODE:
            print('SQL for changed geometry {}'.format(fid))

    def delete_feature(self, fid):
        if config.DEBUG_MODE:
            print('SQL for deleted feature {}'.format(fid))

    def update_statistics(self):
        """
        Update spatialite database statistics.  QGIS <2.12 (and more?)
        don't do this automatically.
        """
        if config.DEBUG_MODE:
            print('Updating database internal statistics.')
        query = self.run_sql('invalidate_old_statistics')
        query = self.run_sql('update_statistics')

    def prepare_sql_queries(self):
        """
        Populates internal dictionary of sql queries.  Override this method to
        change the queries depending on the layer.  Queries should use named
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
            'check_db': """SELECT * FROM sqlite_master;""",
            'check_table': """SELECT * FROM {table};"""}

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


class IntersectionHandler(object):
    """
    Splits features that intersect a given feature and stores information on
    the deleted and newly-added features.
    """
    def __init__(self, iface, vlayer, fid, is_modify=False):
        """
        Class is instantiated for each feature that has intersections with
        another feature in its layer.  fid is ID of my_feature.
        """
        self.iface = iface
        self.vlayer = vlayer
        self.is_modify = is_modify
        self.edit_buffer = self.vlayer.editBuffer()
        self.my_feature = self.vlayer.getFeatures(
            QgsFeatureRequest().setFilterFid(fid)).next()
        self.victims = []
        self.added_features = {}  # New feature lists, with parents as keys
        self.deleted_feature_ids = []

    def handle_intersections(self):
        """
        Main method of class used to process the intersections.
        """
        if config.DEBUG_MODE:
            print("DEBUG MODE: Populating list of intersections to handle.")
        self.victims = find_intersections(self.my_feature, self.vlayer)
        self.handle_my_feature()
        self.handle_victims()
        if config.DEBUG_MODE:
            print('Added features from {}:'.format(self.my_feature.id()))
            pprint.pprint(self.added_features)
            print('Deleted feature_ids from {}:'.format(self.my_feature.id()))
            pprint.pprint(self.deleted_feature_ids)

    def handle_my_feature(self):
        """
        Handle intersection and populate list of children derived from the
        original features.
        """
        fid = self.my_feature.id()
        my_geometry = self.my_feature.geometry()
        if config.DEBUG_MODE:
            print('Modifying my_feature {}'.format(fid))

    def update_my_feature_geometry(self, geometry):
        """
        Change the geometry by interaction with victims.
        :param geometry: geometry to be updated
        :return geometry: updated geometry
        """
        return geometry

    def handle_victims(self):
        """
        Handle intersection and populate list of children derived from the
        victims.
        """
        for victim in self.victims:
            if config.DEBUG_MODE:
                print('Modifying victim {}'.format(victim.id()))
            pass

    def update_victim_geometry(self, geometry):
        """
        Change the geometry by interaction with my_feature.
        :param geometry: geometry to be updated
        :return geometry: updated geometry
        """
        my_geometry = self.my_feature.geometry()
        return geometry

    def get_added_features(self):
        """
        Return list of added features.
        """
        return self.added_features

    def get_deleted_feature_ids(self):
        """
        Return list of deleted features.
        """
        return self.deleted_feature_ids


def find_intersections(my_feature, vlayer):
    """
    Populate list of victim features that intersect with my feature.

    :param my_feature: QgsFeature to test against layer
    :param vlayer: QgsVectorLayer containing features to intersect
    :rtype : List of QgsFeatures
    :return: Intersecting features
    """
    # Get all features within bbox of new feature
    geometry = my_feature.geometry()
    bbox = geometry.boundingBox()
    bbox_victims = [f for f in vlayer.getFeatures(
        QgsFeatureRequest().setFilterRect(bbox))]

    # Select features that pass a stricter test
    strict_victims = []
    POINT, LINE, POLYGON = range(3)  # Enum-like reference for geometry types
    for victim in bbox_victims:
        # Don't include yourself or former self
        # Compare against geometry because committed features get new ids
        if geometry.equals(victim.geometry()):
            continue

        # More precise checks on intersection
        overlaps, crosses, touches, contains = (False, False, False, False)
        if geometry.type() == LINE:
            crosses = geometry.crosses(victim.geometry())
            if geometry.touches(victim.geometry()):
                if touch_is_ends_only(geometry, victim.geometry()):
                    touches = False
                else:
                    touches = True

        if geometry.type() == POLYGON:
            overlaps = geometry.overlaps(victim.geometry())
            contains = geometry.contains(victim.geometry())

        if (overlaps or crosses or touches or contains) is True:
            # Stricter test has been passed
            strict_victims.append(victim)

        if config.DEBUG_MODE:
            msg = 'DEBUG_MODE: {} vs {}: '.format(my_feature.id(), victim.id())
            if overlaps:
                msg += 'overlaps'
            if crosses:
                msg += 'crosses'
            if touches:
                msg += 'touches'
            if contains:
                msg += 'contains'
            print(msg)

    return strict_victims


def touch_is_ends_only(my_geometry, victim_geometry):
    """
    Check if intersecting points are the ends of victim features.
    Intersection only counts as touching if middle points are
    shared.
    This routine assumes victim geometry is multipolyline type, but with just
     one part.
    :param my_geometry: QgsGeometry for new feature
    :param victim_geometry: QgsGeometry for victim feature
    :return: Boolean
    """
    feature_start_point = convert_to_points_list(my_geometry)[0]
    feature_end_point = convert_to_points_list(my_geometry)[-1]
    victim_internal_points = convert_to_points_list(victim_geometry)[1:-1]

    for point in [feature_start_point, feature_end_point]:
        if point in victim_internal_points:
            return False

    return True


def convert_to_points_list(geometry):
    """
    Convert geometry to list of points, accounting for single or multipart
    geometry.
    :param geometry: QgsGeometry for feature
    :return: list of QgsPoints
    """
    if geometry.isMultipart():
        return geometry.asMultiPolyline()[0]
    else:
        return geometry.asPolyline()


class IntersectionHandlerError(Exception):
    pass
