# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_street_selector_ui.ui'
#
# Created: Thu Dec 10 12:14:13 2015
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_streetSelectorDialog(object):
    def setupUi(self, streetSelectorDialog):
        streetSelectorDialog.setObjectName(_fromUtf8("streetSelectorDialog"))
        streetSelectorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        streetSelectorDialog.resize(320, 236)
        streetSelectorDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(streetSelectorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okPushButton = QtGui.QPushButton(streetSelectorDialog)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(streetSelectorDialog)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.esuLabel = QtGui.QLabel(streetSelectorDialog)
        self.esuLabel.setObjectName(_fromUtf8("esuLabel"))
        self.gridLayout.addWidget(self.esuLabel, 0, 0, 1, 1)
        self.usrnTableWidget = QtGui.QTableWidget(streetSelectorDialog)
        self.usrnTableWidget.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.usrnTableWidget.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked)
        self.usrnTableWidget.setAlternatingRowColors(True)
        self.usrnTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.usrnTableWidget.setWordWrap(False)
        self.usrnTableWidget.setObjectName(_fromUtf8("usrnTableWidget"))
        self.usrnTableWidget.setColumnCount(3)
        self.usrnTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.usrnTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.usrnTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.usrnTableWidget.setHorizontalHeaderItem(2, item)
        self.usrnTableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.usrnTableWidget.horizontalHeader().setStretchLastSection(True)
        self.usrnTableWidget.verticalHeader().setVisible(False)
        self.usrnTableWidget.verticalHeader().setDefaultSectionSize(30)
        self.usrnTableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.usrnTableWidget, 1, 0, 1, 1)

        self.retranslateUi(streetSelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(streetSelectorDialog)

    def retranslateUi(self, streetSelectorDialog):
        streetSelectorDialog.setWindowTitle(_translate("streetSelectorDialog", "Street Selector", None))
        self.okPushButton.setText(_translate("streetSelectorDialog", "OK", None))
        self.cancelPushButton.setText(_translate("streetSelectorDialog", "Cancel", None))
        self.esuLabel.setText(_translate("streetSelectorDialog", "ESU:", None))
        item = self.usrnTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("streetSelectorDialog", "USRN", None))
        item = self.usrnTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("streetSelectorDialog", "Street Type", None))
        item = self.usrnTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("streetSelectorDialog", "Description", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    streetSelectorDialog = QtGui.QDialog()
    ui = Ui_streetSelectorDialog()
    ui.setupUi(streetSelectorDialog)
    streetSelectorDialog.show()
    sys.exit(app.exec_())

