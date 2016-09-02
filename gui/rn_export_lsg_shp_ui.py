# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_export_lsg_shp_ui.ui'
#
# Created: Tue Dec 15 11:14:30 2015
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

class Ui_exportLsgShpDialog(object):
    def setupUi(self, exportLsgShpDialog):
        exportLsgShpDialog.setObjectName(_fromUtf8("exportLsgShpDialog"))
        exportLsgShpDialog.resize(454, 115)
        exportLsgShpDialog.setMinimumSize(QtCore.QSize(0, 0))
        exportLsgShpDialog.setMaximumSize(QtCore.QSize(16777215, 193))
        self.gridLayout = QtGui.QGridLayout(exportLsgShpDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fileLabel = QtGui.QLabel(exportLsgShpDialog)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.horizontalLayout_2.addWidget(self.fileLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileLineEdit = QtGui.QLineEdit(exportLsgShpDialog)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.selectFilePushButton = QtGui.QPushButton(exportLsgShpDialog)
        self.selectFilePushButton.setText(_fromUtf8(""))
        self.selectFilePushButton.setObjectName(_fromUtf8("selectFilePushButton"))
        self.horizontalLayout.addWidget(self.selectFilePushButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.unassignedEsuCheckBox = QtGui.QCheckBox(exportLsgShpDialog)
        self.unassignedEsuCheckBox.setObjectName(_fromUtf8("unassignedEsuCheckBox"))
        self.horizontalLayout_3.addWidget(self.unassignedEsuCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.okPushButton = QtGui.QPushButton(exportLsgShpDialog)
        self.okPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_3.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(exportLsgShpDialog)
        self.cancelPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(exportLsgShpDialog)
        QtCore.QMetaObject.connectSlotsByName(exportLsgShpDialog)

    def retranslateUi(self, exportLsgShpDialog):
        exportLsgShpDialog.setWindowTitle(_translate("exportLsgShpDialog", "Export LSG to Shapefile", None))
        self.fileLabel.setText(_translate("exportLsgShpDialog", "Export to", None))
        self.unassignedEsuCheckBox.setText(_translate("exportLsgShpDialog", "Include unassigned ESU\'s", None))
        self.okPushButton.setText(_translate("exportLsgShpDialog", "OK", None))
        self.cancelPushButton.setText(_translate("exportLsgShpDialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exportLsgShpDialog = QtGui.QDialog()
    ui = Ui_exportLsgShpDialog()
    ui.setupUi(exportLsgShpDialog)
    exportLsgShpDialog.show()
    sys.exit(app.exec_())

