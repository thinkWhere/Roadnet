# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_export_poly_pr_shp_ui.ui'
#
# Created: Tue Dec 15 12:50:49 2015
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

class Ui_exportPolyShpDialog(object):
    def setupUi(self, exportPolyShpDialog):
        exportPolyShpDialog.setObjectName(_fromUtf8("exportPolyShpDialog"))
        exportPolyShpDialog.resize(483, 115)
        exportPolyShpDialog.setMinimumSize(QtCore.QSize(0, 0))
        exportPolyShpDialog.setMaximumSize(QtCore.QSize(16777215, 193))
        self.gridLayout = QtGui.QGridLayout(exportPolyShpDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fileLabel = QtGui.QLabel(exportPolyShpDialog)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.horizontalLayout_2.addWidget(self.fileLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileLineEdit = QtGui.QLineEdit(exportPolyShpDialog)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.selectFilePushButton = QtGui.QPushButton(exportPolyShpDialog)
        self.selectFilePushButton.setText(_fromUtf8(""))
        self.selectFilePushButton.setObjectName(_fromUtf8("selectFilePushButton"))
        self.horizontalLayout.addWidget(self.selectFilePushButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.publicRecordsCheckBox = QtGui.QCheckBox(exportPolyShpDialog)
        self.publicRecordsCheckBox.setObjectName(_fromUtf8("publicRecordsCheckBox"))
        self.horizontalLayout_3.addWidget(self.publicRecordsCheckBox)
        self.unassignedPolyCheckBox = QtGui.QCheckBox(exportPolyShpDialog)
        self.unassignedPolyCheckBox.setObjectName(_fromUtf8("unassignedPolyCheckBox"))
        self.horizontalLayout_3.addWidget(self.unassignedPolyCheckBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.okPushButton = QtGui.QPushButton(exportPolyShpDialog)
        self.okPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_3.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(exportPolyShpDialog)
        self.cancelPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(exportPolyShpDialog)
        QtCore.QMetaObject.connectSlotsByName(exportPolyShpDialog)

    def retranslateUi(self, exportPolyShpDialog):
        exportPolyShpDialog.setWindowTitle(_translate("exportPolyShpDialog", "Export Maintenance Polygons to Shapefile", None))
        self.fileLabel.setText(_translate("exportPolyShpDialog", "Export to", None))
        self.publicRecordsCheckBox.setText(_translate("exportPolyShpDialog", "Public records only", None))
        self.unassignedPolyCheckBox.setText(_translate("exportPolyShpDialog", "Include unassigned polygons", None))
        self.okPushButton.setText(_translate("exportPolyShpDialog", "OK", None))
        self.cancelPushButton.setText(_translate("exportPolyShpDialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exportPolyShpDialog = QtGui.QDialog()
    ui = Ui_exportPolyShpDialog()
    ui.setupUi(exportPolyShpDialog)
    exportPolyShpDialog.show()
    sys.exit(app.exec_())

