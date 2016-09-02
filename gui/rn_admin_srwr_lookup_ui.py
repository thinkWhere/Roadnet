# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_admin_srwr_lookup_ui.ui'
#
# Created: Sun Aug 16 11:54:17 2015
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

class Ui_srwrLookupDialog(object):
    def setupUi(self, srwrLookupDialog):
        srwrLookupDialog.setObjectName(_fromUtf8("srwrLookupDialog"))
        srwrLookupDialog.resize(372, 293)
        srwrLookupDialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout_2 = QtGui.QGridLayout(srwrLookupDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.typeDescLineEdit = QtGui.QLineEdit(srwrLookupDialog)
        self.typeDescLineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.typeDescLineEdit.setObjectName(_fromUtf8("typeDescLineEdit"))
        self.gridLayout.addWidget(self.typeDescLineEdit, 0, 2, 1, 1)
        self.itemsListView = QtGui.QListView(srwrLookupDialog)
        self.itemsListView.setObjectName(_fromUtf8("itemsListView"))
        self.gridLayout.addWidget(self.itemsListView, 1, 0, 1, 3)
        self.typeNoSpinBox = QtGui.QSpinBox(srwrLookupDialog)
        self.typeNoSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.typeNoSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.typeNoSpinBox.setMinimum(0)
        self.typeNoSpinBox.setMaximum(999)
        self.typeNoSpinBox.setObjectName(_fromUtf8("typeNoSpinBox"))
        self.gridLayout.addWidget(self.typeNoSpinBox, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.addButton = QtGui.QPushButton(srwrLookupDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.removeButton = QtGui.QPushButton(srwrLookupDialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout_2.addWidget(self.removeButton)
        self.amendButton = QtGui.QPushButton(srwrLookupDialog)
        self.amendButton.setObjectName(_fromUtf8("amendButton"))
        self.verticalLayout_2.addWidget(self.amendButton)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.closeButton = QtGui.QPushButton(srwrLookupDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout_2.addWidget(self.closeButton)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(srwrLookupDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.desRadioButton = QtGui.QRadioButton(self.groupBox)
        self.desRadioButton.setObjectName(_fromUtf8("desRadioButton"))
        self.horizontalLayout.addWidget(self.desRadioButton)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.reinsRadioButton = QtGui.QRadioButton(self.groupBox)
        self.reinsRadioButton.setObjectName(_fromUtf8("reinsRadioButton"))
        self.horizontalLayout.addWidget(self.reinsRadioButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.statRadioButton = QtGui.QRadioButton(self.groupBox)
        self.statRadioButton.setObjectName(_fromUtf8("statRadioButton"))
        self.horizontalLayout.addWidget(self.statRadioButton)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(srwrLookupDialog)
        QtCore.QMetaObject.connectSlotsByName(srwrLookupDialog)

    def retranslateUi(self, srwrLookupDialog):
        srwrLookupDialog.setWindowTitle(_translate("srwrLookupDialog", "Edit SRWR Lookup", None))
        self.addButton.setText(_translate("srwrLookupDialog", "Add", None))
        self.removeButton.setText(_translate("srwrLookupDialog", "Remove", None))
        self.amendButton.setText(_translate("srwrLookupDialog", "Amend", None))
        self.closeButton.setText(_translate("srwrLookupDialog", "Close", None))
        self.groupBox.setTitle(_translate("srwrLookupDialog", "Lookup Table:", None))
        self.desRadioButton.setText(_translate("srwrLookupDialog", "Special Designation", None))
        self.reinsRadioButton.setText(_translate("srwrLookupDialog", "Reinstatement", None))
        self.statRadioButton.setText(_translate("srwrLookupDialog", "Road Status", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    srwrLookupDialog = QtGui.QDialog()
    ui = Ui_srwrLookupDialog()
    ui.setupUi(srwrLookupDialog)
    srwrLookupDialog.show()
    sys.exit(app.exec_())

