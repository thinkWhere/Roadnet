# -*- coding: utf-8 -*-
__author__ = 'Alessandro'
import os
from PyQt4.QtGui import QPixmap, QDesktopServices
from PyQt4.QtCore import QUrl
class About:
    """
    class holding the general functions for
    the about window dialog
    """
    def __init__(self, about_dia, plugin_dir):
        self.about_dia = about_dia
        self.plugin_dir = plugin_dir
        self.metadata_file_path = os.path.join(self.plugin_dir, "metadata.txt")
        self.image_file_path = os.path.join(self.plugin_dir,
                                            "image",
                                            "rn_logo_v2.png")
        self.model_navigation()
        self.set_values()

    def model_navigation(self):
        self.about_dia.ui.okButton.clicked.connect(self.close_browser)

    def close_browser(self):
        self.about_dia.close()

    def set_values(self):
        # set labels text and image path
        version = ""
        with open(self.metadata_file_path, 'r') as in_file:
            for line in in_file:
                if line.startswith("version"):
                    version = line.split("=")[1].strip()
        self.about_dia.ui.versionLabel.setText("Version: {0}".format(version))
        self.about_dia.ui.imageLabel.setPixmap(QPixmap(self.image_file_path))
        # sets hyperlinks
        self.about_dia.ui.gnuLicenseLabel.setOpenExternalLinks(True)
        self.about_dia.ui.thinkWhereLinkLabel.setOpenExternalLinks(True)
