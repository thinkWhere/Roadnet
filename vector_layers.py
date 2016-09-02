import sqlite3
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox
from qgis.core import (QgsCoordinateReferenceSystem,
                       QgsMapLayerRegistry,
                       QgsVectorLayer,
                       QgsDataSourceURI)
import roadnet_exceptions as rn_except


def add_styled_spatialite_layer(vlayer_name, display_name, db_path,
                                iface, style=None):
    """
    Load layer to QGIS, apply style and refresh display
    :param vlayer_name: Name of db table containing layer
    :param display_name: Name to appear in QGIS legend
    :param db_path: Path to spatialite file
    :param iface: QGIS iface instance
    :param style: Override style (usually display_name.lower() used)
    :return vlayer: QgsVectorLayer
    """
    vlayer = load_spatialite_layer(vlayer_name, display_name, db_path)
    if not vlayer.isValid():
        msg = "Layer: {0} is not valid".format(vlayer.name())
        raise rn_except.InvalidLayerPopupError(msg)

    set_crs_and_register(vlayer)

    if style is None:
        style = display_name.lower()
    try:
        # Styling fails if no style found
        apply_layer_style(vlayer, style, db_path)
    except rn_except.InvalidStylePopupError:
        # Allow unstyled layer; user is warned by exception
        pass

    refresh_display(iface)
    return vlayer


def load_spatialite_layer(vlayer_name, display_name, db_path):
    """
    Load layer into QGIS and add to canvas
    :param vlayer_name: db table name for vector layer
    :param display_name: name as displayed on the legend
    :param db_path: path of spatialite database file
    """
    # Add spatialite layer to canvas
    uri = QgsDataSourceURI()
    uri.setDatabase(db_path)
    schema = ''
    geom_column = 'geometry'
    uri.setDataSource(schema, vlayer_name, geom_column)
    vlayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
    return vlayer


def set_crs_and_register(vlayer):
    """
    Check validity of vector layer and register with QGIS
    :param vlayer: QgsVectorLayer
    """
    vlayer.setCrs(QgsCoordinateReferenceSystem(
        27700, QgsCoordinateReferenceSystem.EpsgCrsId), False)
    QgsMapLayerRegistry.instance().addMapLayer(vlayer)


def apply_layer_style(vlayer, style, db_path):
    """
    Apply a style from the database to aa layer.
    :param vlayer: QgsVectorLayer
    :param style: name of style
    :param db_path: location of database table
    """
    style_qml = get_style_qml(style, db_path)
    vlayer.applyNamedStyle(style_qml)


def get_style_qml(style, db_path):
    """
    Get the QML styling information for named style.
    :param style: styleName in the database
    :param db_path: Open roadNet QSqlDatabase
    :return: style ID
    """
    sql = """SELECT styleQML FROM layer_styles
                 WHERE styleName = '{}'
                 ORDER BY update_time DESC
                 ;""".format(style)  # Ordering ensures most recent used.
    with sqlite3.connect(db_path) as conn:
        curs = conn.cursor()
        curs.execute(sql)
        result = curs.fetchone()

    # Catch error and warn user when style file isn't found
    try:
        style_qml = result[0]
    except TypeError:
        msg = "No style named '{}' in {}".format(style, db_path)
        raise rn_except.InvalidStylePopupError(msg)
    return style_qml


def remove_spatialite_layer(vlayer, iface):
    """
    Removes the spatialite layers from QGIS Map Layer Registry and refreshes the display.
    :param vlayer: QgsVectorLayer
    :param iface: QGIS iface instance
    """
    registry = QgsMapLayerRegistry.instance()
    try:
        registry.removeMapLayer(vlayer.id())
    except:
        # QGIS throws an error if you try to remove a layer that doesn't exist
        msg = "Attempted to remove layer that is not in QgsMapLayerRegistry"
        raise rn_except.RemoveNonExistentLayerPopupError(msg)
    refresh_display(iface)


def refresh_display(iface):
    """
    Refresh the QGIS display to show changes
    :param iface:
    """
    iface.mapCanvas().clearCache()
    iface.mapCanvas().refresh()

