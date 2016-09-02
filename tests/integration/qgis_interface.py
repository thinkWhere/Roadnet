# -*- coding: utf-8 -*-

"""
This code is based on the testing code for the main QGIS program (__init__)
and mocked.  Details below:
***************************************************************************
    __init__.py
    ---------------------
    Date                 : January 2016
    Copyright            : (C) 2016 by Matthias Kuhn
                           [modified by john.stevenson]
    Email                : matthias@opengis.ch
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

import sys
#  Mock is not from standard library in Python 2.7, but can be installed
#  via pip

import mock

import qgis.core
from qgis.gui import QgisInterface, QgsMapCanvas
from qgis.core import QgsApplication, QgsProviderRegistry

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QSize, QCoreApplication

__author__ = 'Matthias Kuhn'
__date__ = 'January 2016'
__copyright__ = '(C) 2016, Matthias Kuhn'


def start_app(gui_flag=False):
    """
    Will start a QgsApplication and call all initialization code like
    registering the providers and other infrastructure. It will not load
    any plugins.
    You can always get the reference to a running app by calling `QgsApplication.instance()`.
    The initialization will only happen once, so it is safe to call this method repeatedly.
        Returns
        -------
        QgsApplication
        A QgsApplication singleton
    """
    global QGISAPP
    QCoreApplication.setOrganizationName('QGIS')
    QCoreApplication.setApplicationName('QGIS2')
    QgsApplication.setPrefixPath("/usr/share/", True)

    # Note: QGIS_PREFIX_PATH is evaluated in QgsApplication -
    # no need to mess with it here.
    QGISAPP = QgsApplication(sys.argv, gui_flag)
    QGISAPP.initQgis()

    if len(QgsProviderRegistry.instance().providerList()) == 0:
        raise RuntimeError('No data providers available.')

    return QGISAPP


def get_mock_iface():
    """
    Will return a mock QgsInterface object with some methods implemented in a generic way.
    You can further control its behavior
    by using the mock infrastructure. Refer to https://docs.python.org/3/library/unittest.mock.html
    for more details.
        Returns
        -------
        QgisInterface
        A mock QgisInterface
    """
    my_iface = mock.Mock(spec=QgisInterface)
    my_iface.mainWindow.return_value = QMainWindow()

    canvas = QgsMapCanvas(my_iface.mainWindow())
    canvas.resize(QSize(400, 400))
    my_iface.mapCanvas.return_value = canvas

    return my_iface
