# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Roadnet
                                 A QGIS plugin
 Roadnet is a plugin used for maintaining a local street gazetteer.
                             -------------------
        begin                : 2014-12-09
        copyright            : (C) 2014 by thinkWhere
        email                : support@thinkwhere.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

import config

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Roadnet class from file Roadnet.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    if config.DEBUG_MODE:
        print('DEBUG_MODE: __init__.py called, plugin attached to QGIS')
    from roadnet import Roadnet
    return Roadnet(iface)
