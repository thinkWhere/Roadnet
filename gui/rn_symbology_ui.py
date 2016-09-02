# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_symbology_ui.ui'
#
# Created: Thu Jan 07 12:04:15 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_symbologyDialog(object):
    def setupUi(self, symbologyDialog):
        symbologyDialog.setObjectName(_fromUtf8("symbologyDialog"))
        symbologyDialog.setWindowModality(QtCore.Qt.NonModal)
        symbologyDialog.resize(418, 141)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(symbologyDialog.sizePolicy().hasHeightForWidth())
        symbologyDialog.setSizePolicy(sizePolicy)
        symbologyDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(symbologyDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = QtGui.QProgressBar(symbologyDialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.runPushButton = QtGui.QPushButton(symbologyDialog)
        self.runPushButton.setObjectName(_fromUtf8("runPushButton"))
        self.horizontalLayout.addWidget(self.runPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.updatedFeaturesLabel = QtGui.QLabel(symbologyDialog)
        self.updatedFeaturesLabel.setObjectName(_fromUtf8("updatedFeaturesLabel"))
        self.verticalLayout_2.addWidget(self.updatedFeaturesLabel)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(symbologyDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.esuCheckBox = QtGui.QCheckBox(symbologyDialog)
        self.esuCheckBox.setObjectName(_fromUtf8("esuCheckBox"))
        self.verticalLayout.addWidget(self.esuCheckBox)
        self.rdPolyCheckBox = QtGui.QCheckBox(symbologyDialog)
        self.rdPolyCheckBox.setObjectName(_fromUtf8("rdPolyCheckBox"))
        self.verticalLayout.addWidget(self.rdPolyCheckBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(symbologyDialog)
        QtCore.QMetaObject.connectSlotsByName(symbologyDialog)

    def retranslateUi(self, symbologyDialog):
        symbologyDialog.setWindowTitle(_translate("symbologyDialog", "Update Symbology", None))
        self.runPushButton.setText(_translate("symbologyDialog", "Run", None))
        self.updatedFeaturesLabel.setText(_translate("symbologyDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Updated Features</span></p><p>ESU Graphic:</p><p>Road Polygon:</p></body></html>", None))
        self.label.setText(_translate("symbologyDialog", "Select layers to update:", None))
        self.esuCheckBox.setText(_translate("symbologyDialog", "ESU Graphic", None))
        self.rdPolyCheckBox.setText(_translate("symbologyDialog", "Road Polygon", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    symbologyDialog = QtGui.QDialog()
    ui = Ui_symbologyDialog()
    ui.setupUi(symbologyDialog)
    symbologyDialog.show()
    sys.exit(app.exec_())

