# -*- coding: utf-8 -*-
"""
Functions to export shapefiles from RAMP for WDM.
"""
import os
from qgis.core import (
    QGis,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsVectorFileWriter,
    QgsVectorLayer)
from PyQt4.QtCore import QVariant
from PyQt4.QtSql import QSqlQuery

import Roadnet.roadnet_exceptions as rn_except
from Roadnet import config


ELEMENT_CODE_MAP = {'ACARPK': 'Adopted Carpark',
                    'CARPK': 'Parking',
                    'CGWAY': 'Carriageway',
                    'CRESERVE': 'Central Reserve',
                    'CYCLE': 'Cycleway/Path',
                    'FPATH': 'Footpath',
                    'FTWAY': 'Footway',
                    'LSHARD': 'Landscaping (Hard)',
                    'LSSOFT': 'Landscaping (Soft)',
                    'SSTRIP': 'Service Strip',
                    'VERGE': 'Verge'}


def export(element_type, db, output_directory):
    """
    Export RAMP data to output directory as series of shapefiles.
    :param element_type: String to filter element column e.g. FTWAY
    :param db: open QSqlDatabase object
    :param output_directory: Directory for output files
    """
    features_query = query_db_for_features(element_type, db)
    vlayer = create_temp_layer_in_memory()
    try:
        add_features_to_vlayer(features_query, vlayer)
    except rn_except.NoFeaturesFoundException:
        if config.DEBUG_MODE:
            print("DEBUG MODE: No features for {}".format(element_type))
    write_temp_layer_to_shapefile(element_type, vlayer, output_directory)


def query_db_for_features(element_type, db):
    """
    Get features from database for given element
    :param element_type: String to filter element column e.g. FTWAY
    :param db: Open QSqlDatabase object
    :return: Active QSqlQuery containing feature information
    """

    sql = create_sql_command(element_type)
    features_query = QSqlQuery(sql, db)

    return features_query


def create_sql_command(element_type):
    """
    Create the sql query to use, depending on the element requested.
    :param element_type: String to filter element column e.g. FTWAY
    :return: sql command (str)
    """

    # For CGWAY and FPATH, the geometry is calculated from the associated MCL
    if element_type in ('CGWAY', 'FPATH'):
        length_expression = "GLength(mcl.geometry) AS feature_length"
    else:
        length_expression = "feature_length"

    sql = """
        SELECT AsBinary(rdpoly.geometry) AS geometry, rd_pol_id, element, hierarchy,
        desc_2, desc_3, ref_3, currency_flag, {feature_length}, r_usrn,
        mcl_ref, usrn, lor_ref_1, lor_ref_2, lor_desc, lane_number,
        speed_limit, rural_urban_id, street_classification, carriageway
        FROM rdpoly
        LEFT OUTER JOIN mcl
        ON rdpoly.mcl_cref = mcl.mcl_ref
        WHERE element = "{element}"
        AND rdpoly.symbol IN (11, 12);""".format(element=element_type,
                                                 feature_length=length_expression)

    return sql


def create_temp_layer_in_memory():
    """
    Create a QGIS memory layer with appropriate geometry, fields and CRS
    :return: QgsVectorLayer in memory
    """
    # Create layer
    vlayer = QgsVectorLayer('MultiPolygon?crs=epsg:27700', 'wdm_export', 'memory')
    # Add attribute fields
    provider = vlayer.dataProvider()
    provider.addAttributes([QgsField('rd_pol_id', QVariant.Int),
                            QgsField('element', QVariant.String),
                            QgsField('hierarchy', QVariant.String),
                            QgsField('desc_2', QVariant.String),
                            QgsField('desc_3', QVariant.Int),
                            QgsField('ref_3', QVariant.Int),
                            QgsField('feature_length', QVariant.Double),
                            QgsField('mcl_ref', QVariant.Int),
                            QgsField('usrn', QVariant.Int),
                            QgsField('lor_ref_1', QVariant.String),
                            QgsField('lor_ref_2', QVariant.Int),
                            QgsField('lor_desc', QVariant.String),
                            QgsField('lane_number', QVariant.Int),
                            QgsField('speed_limit', QVariant.String),
                            QgsField('rural_urban_id', QVariant.String),
                            QgsField('street_classification', QVariant.String),
                            QgsField('carriageway', QVariant.String)])
    vlayer.updateFields()

    return vlayer


def add_features_to_vlayer(features_query, vlayer):
    """
    Parse the query output and append as features to vector layer.
    :param features_query: Active QSqlQuery containing feature information
    :param vlayer: QgsVectorLayer in memory
    """
    new_features = []

    while True:
        features_boolean = features_query.next()
        if features_boolean is False:
            break

        record = features_query.record()
        try:
            feature = create_feature_from_record(record, vlayer)
        except rn_except.RdPolyNullGeometryError, e:
            if config.DEBUG_MODE:
                print("DEBUG_MODE: " + e.args[0])
            continue

        # Add to list
        new_features.append(feature)

    if new_features:
        provider = vlayer.dataProvider()
        provider.addFeatures(new_features)
        vlayer.updateExtents()
    else:
        raise rn_except.NoFeaturesFoundException()


def create_feature_from_record(record, vlayer):
    """
    Create a QgsFeature from the database record.
    :param record: QSqlRecord
    :param vlayer: QgsVectorLayer
    :return: QgsFeature
    """
    feature = QgsFeature()
    geometry = get_geometry_from_record(record)
    feature.setGeometry(geometry)

    fields = vlayer.fields()
    set_feature_attributes_from_record(feature, record, fields)

    return feature


def get_geometry_from_record(record):
    geometry = QgsGeometry()
    wkb = record.value('geometry')
    if wkb.isNull():
        msg = "rd_pol_id {} has NULL geometry".format(record.value('rd_pol_id'))
        raise rn_except.RdPolyNullGeometryError(msg)
    geometry.fromWkb(str(wkb))  # Convert variant to string
    return geometry


def set_feature_attributes_from_record(feature, record, fields):
    """
    Modify feature in place to set attributes
    :param feature:
    :param record:
    :param fields:
    :return:
    """
    # Set attribute values
    field_names = [f.name() for f in fields]
    feature.setFields(fields)

    for field_name in field_names:
        feature.setAttribute(field_name, record.value(field_name))


def write_temp_layer_to_shapefile(element_type, vlayer, output_directory):
    """
    Write temporary vector layer to disk as shapefile
    :param element_type: String with element name used to create filename
    :param vlayer:  QgsVectorLayer in memory
    :param output_directory: Directory for output files
    """
    # Open writer with empty shapefile
    filename = prepare_filename(ELEMENT_CODE_MAP[element_type])
    shapefile_path = os.path.join(output_directory, filename)
    writer = open_shapefile_writer(vlayer, shapefile_path)

    # Add features to shapefile
    for feature in vlayer.getFeatures():
        writer.addFeature(feature)

    # This triggers writer to write all the features to disk before it is
    # deleted
    del writer


def open_shapefile_writer(vlayer, shapefile_path):
    # Prepare inputs
    fields = vlayer.fields()

    # Create writer
    writer = QgsVectorFileWriter(
        shapefile_path, "utf-8", fields, QGis.WKBMultiPolygon,
        QgsCoordinateReferenceSystem(27700, QgsCoordinateReferenceSystem.EpsgCrsId),
        'ESRI Shapefile')

    if writer.hasError() != QgsVectorFileWriter.NoError:
        msg = "Error when creating shapefile: {}".format(writer.errorMessage())
        raise rn_except.CannotOpenShapefilePopupError(msg)

    return writer


def prepare_filename(text):
    """
    Strip spaces and brackets from text to make into suitable filename
    :param text: input text string
    :return: filename
    """
    text = text.replace(' ', '_')
    text = text.replace('/', '_')
    text = text.replace('(', '')
    text = text.replace(')', '')
    return 'RAMPEXPORT_' + text + '.shp'

