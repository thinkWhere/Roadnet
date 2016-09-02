# -*- coding: utf-8 -*-
"""
Functions to export Length of Roads report from RAMP.
"""

from collections import OrderedDict
from textwrap import dedent
import qgis.core  # Required to have access to correct QVariants
import PyQt4
from PyQt4.QtSql import QSqlQuery
import re
import Roadnet.roadnet_exceptions as rn_except

# These queries generate a like-for-like with the old roadNet, but note that
# the numbers for Total are wrong as they include NULLs.
LANE_CLAUSES = OrderedDict([
    ("Single Track / two lane", "AND lane_number IN (1, 2) AND Carriageway = 'Single'"),
    ("Three lane", "AND lane_number = 3 AND Carriageway = 'Single'"),
    ("Four lane", "AND lane_number = 4 AND Carriageway = 'Single'"),
    ("Five lane", "AND lane_number = 5 AND Carriageway = 'Single'"),
    ("Six lane", "AND lane_number = 6 AND Carriageway = 'Single'"),
    ("Total", ""),
    ("Of which Dual Carriageway", "AND carriageway = 'Dual'")])

HEADERS = OrderedDict([
    ('A', "A Roads, Urban (<=40 mph), Rural (>40 mph)"),
    ('B', "B Roads, Urban (<=40 mph), Rural (>40 mph)"),
    ('C', "C Roads, Urban (<=40 mph), Rural (>40 mph)"),
    ('U', "Unclassified Roads, Urban (<=40 mph), Rural (>40 mph)")])

CLASSIFICATIONS = ('A', 'B', 'C', 'U')


def get_length_of_roads_text(db):
    """
    Return a string with the Length of Roads output suitable for
    display or writing to file.
    :param db: open QSqlDatabase object
    :return: str length of roads text
    """
    # Check spatialite version before starting. v4.1.1 causes Linux hard crash
    if get_spatialite_version_as_int(db) < 430:
        msg = ("Length of roads export requires Spatialite version 4.3.0 "
               "or higher.\n\nThis means QGIS 2.14 and Ubuntu >= 16.04.")
        raise rn_except.BadSpatialiteVersionError(msg)

    lor_text = ''

    for street_classification in CLASSIFICATIONS:
        lor_text += HEADERS[street_classification] + '\n'

        for lanes_key in LANE_CLAUSES:
            sql_urban = prepare_sql(street_classification, lanes_key, 'U')
            length_urban = get_road_length_from_db(sql_urban, db)
            sql_rural = prepare_sql(street_classification, lanes_key, 'R')
            length_rural = get_road_length_from_db(sql_rural, db)

            lor_text += "{}, {}, {}\n".format(lanes_key, length_urban,
                                              length_rural)
        lor_text += '\n'

    return lor_text


def get_road_length_from_db(sql, db):
    """
    Run pre-prepared sql query on database to get length of road
    :param sql: str sql selecting by road classification etc
    :param db: open QSqlDatabase object
    :return: float length of road
    """
    query = QSqlQuery(sql, db)
    query_success = query.first()

    if query_success is False:
        msg = ("Length of Roads calculation failed running SQL:\n{}\n"
               "Database output: {}".format(sql, query.lastError().text()))
        raise rn_except.LengthOfRoadsCalculationDatabaseError(msg)

    # Get result from query
    record = query.record()
    road_length = record.value('length')
    if isinstance(road_length, PyQt4.QtCore.QPyNullVariant):
        # Replace NULL from database with zero length
        road_length = 0

    return road_length


def prepare_sql(street_classification, lanes_key, rural_urban_id):
    """
    Prepare the SQL query to get length of road from the database.
    :param street_classification: str in (A, B, C, U)
    :param lanes_key: str key from LANE_CLAUSES dictionary
    :param rural_urban_id: str in (U, R)
    :return: str with SQL for calculation
    """
    lane_number_clause = LANE_CLAUSES[lanes_key]

    # Rural urban definition is based on speed limits.  See original ESRI
    # source code for details
    if rural_urban_id == 'U':
        rural_urban_clause = "AND speed_limit IN ('20PT/30', '20PT/40', '20', '30', '40')"
    else:
        rural_urban_clause = "AND speed_limit IN ('50', '60', '70', '20PT/50', '20PT/60')"

    sql = """
    SELECT Round(Sum(GLength(geometry))/1000, 2) AS length
    FROM mcl
    WHERE section_type = 'CW' AND
        street_classification = "{street_classification}"
        {rural_urban_clause}
        {lane_number_clause}
        ;""".format(street_classification=street_classification,
                    rural_urban_clause=rural_urban_clause,
                    lane_number_clause=lane_number_clause)

    return dedent(sql)


def get_spatialite_version_as_int(db):
    """
    Query the database to find spatialite version
    :param db: open QSqlDatabase object
    :return: Integer form of version number e.g. 411
    """
    # Query the database
    sql = "SELECT spatialite_version() AS version;"
    query = QSqlQuery(sql, db)
    query_success = query.first()

    if query_success is False:
        msg = "Cannot get spatialite version.  Database replied: {}".format(
            query.lastError().text())
        raise RuntimeError(msg)

    # Get the version number and convert to int
    record = query.record()
    version = record.value('version')
    version_as_int = int(re.sub('\D', '', version))

    return version_as_int
