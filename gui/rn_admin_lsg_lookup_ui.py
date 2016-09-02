# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_admin_lsg_lookup_ui.ui'
#
# Created: Wed Aug 12 18:03:37 2015
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

class Ui_lsgLookupDialog(object):
    def setupUi(self, lsgLookupDialog):
        lsgLookupDialog.setObjectName(_fromUtf8("lsgLookupDialog"))
        lsgLookupDialog.resize(372, 295)
        lsgLookupDialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout_2 = QtGui.QGridLayout(lsgLookupDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonsGroupBox = QtGui.QGroupBox(lsgLookupDialog)
        self.buttonsGroupBox.setObjectName(_fromUtf8("buttonsGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.buttonsGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.locRadioButton = QtGui.QRadioButton(self.buttonsGroupBox)
        self.locRadioButton.setObjectName(_fromUtf8("locRadioButton"))
        self.horizontalLayout.addWidget(self.locRadioButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.townRadioButton = QtGui.QRadioButton(self.buttonsGroupBox)
        self.townRadioButton.setObjectName(_fromUtf8("townRadioButton"))
        self.horizontalLayout.addWidget(self.townRadioButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.countyRadioButton = QtGui.QRadioButton(self.buttonsGroupBox)
        self.countyRadioButton.setObjectName(_fromUtf8("countyRadioButton"))
        self.horizontalLayout.addWidget(self.countyRadioButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_2.addWidget(self.buttonsGroupBox, 0, 0, 1, 2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.itemsListView = QtGui.QListView(lsgLookupDialog)
        self.itemsListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.itemsListView.setProperty("showDropIndicator", True)
        self.itemsListView.setObjectName(_fromUtf8("itemsListView"))
        self.gridLayout.addWidget(self.itemsListView, 1, 0, 1, 2)
        self.addLookupLineEdit = QtGui.QLineEdit(lsgLookupDialog)
        self.addLookupLineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.addLookupLineEdit.setObjectName(_fromUtf8("addLookupLineEdit"))
        self.gridLayout.addWidget(self.addLookupLineEdit, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.addButton = QtGui.QPushButton(lsgLookupDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        spacerItem4 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem4)
        self.removeButton = QtGui.QPushButton(lsgLookupDialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout_2.addWidget(self.removeButton)
        self.amendButton = QtGui.QPushButton(lsgLookupDialog)
        self.amendButton.setObjectName(_fromUtf8("amendButton"))
        self.verticalLayout_2.addWidget(self.amendButton)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.closeButton = QtGui.QPushButton(lsgLookupDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout_2.addWidget(self.closeButton)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.retranslateUi(lsgLookupDialog)
        QtCore.QMetaObject.connectSlotsByName(lsgLookupDialog)

    def retranslateUi(self, lsgLookupDialog):
        lsgLookupDialog.setWindowTitle(_translate("lsgLookupDialog", "Edit LSG Lookup", None))
        self.buttonsGroupBox.setTitle(_translate("lsgLookupDialog", "Lookup Table:", None))
        self.locRadioButton.setText(_translate("lsgLookupDialog", "Locality", None))
        self.townRadioButton.setText(_translate("lsgLookupDialog", "Town", None))
        self.countyRadioButton.setText(_translate("lsgLookupDialog", "County", None))
        self.addButton.setText(_translate("lsgLookupDialog", "Add", None))
        self.removeButton.setText(_translate("lsgLookupDialog", "Remove", None))
        self.amendButton.setText(_translate("lsgLookupDialog", "Amend", None))
        self.closeButton.setText(_translate("lsgLookupDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    lsgLookupDialog = QtGui.QDialog()
    ui = Ui_lsgLookupDialog()
    ui.setupUi(lsgLookupDialog)
    lsgLookupDialog.show()
    sys.exit(app.exec_())

