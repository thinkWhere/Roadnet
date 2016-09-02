# -*- coding: utf-8 -*-
import datetime

from qgis.core import QgsFeatureRequest, QgsFeature, QgsGeometry
from qgis.gui import QgsMessageBar
from Roadnet.geometry.edit_handler import (EditHandler,
                                           DatabaseHandler,
                                           IntersectionHandler)
from Roadnet.generic_functions import ipdb_breakpoint
import Roadnet.config as config

__author__ = "john.stevenson"


class MclEditHandler(EditHandler):
    """
    Subclass of EditHandler customised to deal with MCL layer.
    """
    def __init__(self, iface, vlayer, db, params, handle_intersect_flag):
        super(MclEditHandler, self).__init__(iface, vlayer, db, params,
                                             handle_intersect_flag)
        self.db_handler = MclDatabaseHandler(vlayer, db)
        if config.DEBUG_MODE:
            print('DEBUG MODE: MclEditHandler instantiated')

    def warn_if_intersections(self, fid):
        """
        Show warning message if feature intersects another.
        """
        if self.check_for_intersections(fid) is False:
            return

        # Intersection with uncommitted feature is critical
        warning = ('Intersecting MCL features are not permitted.\n\n'
                   'Undo last change before continuing.')
        self.iface.messageBar().pushMessage('roadNet',
                                            warning,
                                            QgsMessageBar.CRITICAL,
                                            9)


class MclDatabaseHandler(DatabaseHandler):
    """
    Subclass of DatabaseHandler customised to deal with MCL layer.
    """
    def __init__(self, vlayer, db):
        super(MclDatabaseHandler, self).__init__(vlayer, db)
        self.mcl_ref_generator = self.init_mcl_ref_generator()

    def init_mcl_ref_generator(self):
        """
        A generator function that yields a unique mcl for newly added
        features.
        """
        # Get initial max mcl_ref
        query = self.run_sql('mcl_get_max_mcl_ref')
        query.first()
        try:
            max_mcl_ref = int(query.record().value('max_mcl_ref'))
        except (ValueError, TypeError):
            # Throws if table is empty
            max_mcl_ref = 0

        # Use value from rdpoly table if that is higher
        query = self.run_sql('rdpoly_get_max_mcl_ref')
        query.first()
        try:
            rdpoly_max_mcl_ref = int(query.record().value('max_mcl_ref'))
        except (ValueError, TypeError):
            # Throws if table is empty
            rdpoly_max_mcl_ref = 0
        query = None  # clear query otherwise it locks connection to database

        if rdpoly_max_mcl_ref > max_mcl_ref:
            max_mcl_ref = rdpoly_max_mcl_ref

        while True:  # Generator yields new max_mcl_ids as needed.
            max_mcl_ref += 1
            yield max_mcl_ref

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
            'mcl_get_max_mcl_ref': """
                SELECT MAX(mcl_ref) AS max_mcl_ref FROM mcl
                ;""",
            'rdpoly_get_max_mcl_ref': """
                SELECT MAX(mcl_cref) AS max_mcl_ref FROM rdpoly
                ;""",
            'mcl_new_feature': """
                UPDATE mcl SET mcl_ref = {mcl_ref}, entry_date = '{entry_date}'
                WHERE PK_UID IS {pk_uid};""",
            }

    def add_feature(self, feature):
        # Collect input data
        mcl_ref = self.mcl_ref_generator.next()
        today = datetime.datetime.now().strftime("%Y%m%d")
        args = {'mcl_ref': mcl_ref,
                'entry_date': today,
                'pk_uid': feature.id()}

        # Run queries
        query = self.run_sql('mcl_new_feature', args)

