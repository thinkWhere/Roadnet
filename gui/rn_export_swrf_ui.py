# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_export_swrf_ui.ui'
#
# Created: Wed Nov 11 15:57:07 2015
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

class Ui_exportSWRF(object):
    def setupUi(self, exportSWRF):
        exportSWRF.setObjectName(_fromUtf8("exportSWRF"))
        exportSWRF.resize(400, 128)
        exportSWRF.setMinimumSize(QtCore.QSize(276, 128))
        exportSWRF.setMaximumSize(QtCore.QSize(400, 128))
        exportSWRF.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout = QtGui.QGridLayout(exportSWRF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(214, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.okPushButton = QtGui.QPushButton(exportSWRF)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_3.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(exportSWRF)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileLabel = QtGui.QLabel(exportSWRF)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.horizontalLayout.addWidget(self.fileLabel)
        self.fileLineEdit = QtGui.QLineEdit(exportSWRF)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.openPushButton = QtGui.QPushButton(exportSWRF)
        self.openPushButton.setText(_fromUtf8(""))
        self.openPushButton.setObjectName(_fromUtf8("openPushButton"))
        self.horizontalLayout.addWidget(self.openPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.closedStreetsCheckBox = QtGui.QCheckBox(exportSWRF)
        self.closedStreetsCheckBox.setObjectName(_fromUtf8("closedStreetsCheckBox"))
        self.gridLayout.addWidget(self.closedStreetsCheckBox, 1, 0, 1, 1)

        self.retranslateUi(exportSWRF)
        QtCore.QMetaObject.connectSlotsByName(exportSWRF)

    def retranslateUi(self, exportSWRF):
        exportSWRF.setWindowTitle(_translate("exportSWRF", "ASD Export", None))
        self.okPushButton.setText(_translate("exportSWRF", "OK", None))
        self.cancelPushButton.setText(_translate("exportSWRF", "Cancel", None))
        self.fileLabel.setText(_translate("exportSWRF", "Export To STDF 1.0", None))
        self.closedStreetsCheckBox.setText(_translate("exportSWRF", "Include Closed Streets", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exportSWRF = QtGui.QDialog()
    ui = Ui_exportSWRF()
    ui.setupUi(exportSWRF)
    exportSWRF.show()
    sys.exit(app.exec_())

