# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_export_complete.ui'
#
# Created: Wed Jul 29 12:00:43 2015
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

class Ui_exportComplete(object):
    def setupUi(self, exportComplete):
        exportComplete.setObjectName(_fromUtf8("exportComplete"))
        exportComplete.resize(197, 82)
        exportComplete.resize(197, 82)
        exportComplete.setMinimumSize(QtCore.QSize(197, 82))
        exportComplete.setMaximumSize(QtCore.QSize(197, 82))
        exportComplete.setWindowFlags(Qt.CustomizeWindowHint)
        self.gridLayout = QtGui.QGridLayout(exportComplete)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(exportComplete)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelPushButton = QtGui.QPushButton(exportComplete)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(exportComplete)
        QtCore.QMetaObject.connectSlotsByName(exportComplete)

    def retranslateUi(self, exportComplete):
        exportComplete.setWindowTitle(_translate("exportComplete", " ", None))
        self.label_2.setText(_translate("exportComplete", "Export Complete ", None))
        self.cancelPushButton.setText(_translate("exportComplete", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exportComplete = QtGui.QDialog()
    ui = Ui_exportComplete()
    ui.setupUi(exportComplete)
    exportComplete.show()
    sys.exit(app.exec_())

