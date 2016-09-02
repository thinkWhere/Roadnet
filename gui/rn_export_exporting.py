# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_export_exporting.ui'
#
# Created: Mon Nov 16 10:48:23 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt

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

class Ui_exporteExporting(object):
    def setupUi(self, exporteExporting):
        exporteExporting.setObjectName(_fromUtf8("exporteExporting"))
        exporteExporting.resize(195, 76)
        exporteExporting.setMinimumSize(QtCore.QSize(195, 76))
        exporteExporting.setMaximumSize(QtCore.QSize(195, 76))
        exporteExporting.setSizeIncrement(QtCore.QSize(195, 76))
        exporteExporting.setWindowFlags(Qt.FramelessWindowHint)
        exporteExporting.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(exporteExporting)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(exporteExporting)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)

        self.retranslateUi(exporteExporting)
        QtCore.QMetaObject.connectSlotsByName(exporteExporting)

    def retranslateUi(self, exporteExporting):
        self.label_2.setText(_translate("exporteExporting", "Exporting...", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exporteExporting = QtGui.QDialog()
    ui = Ui_exporteExporting()
    ui.setupUi(exporteExporting)
    exporteExporting.show()
    sys.exit(app.exec_())

