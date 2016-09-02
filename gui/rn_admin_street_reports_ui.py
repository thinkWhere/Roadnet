# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_admin_street_reports_ui.ui'
#
# Created: Thu Nov 05 16:57:19 2015
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

class Ui_streetreports(object):
    def setupUi(self, streetreports):
        streetreports.setObjectName(_fromUtf8("streetreports"))
        streetreports.resize(453, 278)
        streetreports.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout = QtGui.QGridLayout(streetreports)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(streetreports)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setContentsMargins(27, 5, 3, 3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblsRadioButton = QtGui.QRadioButton(streetreports)
        self.tblsRadioButton.setObjectName(_fromUtf8("tblsRadioButton"))
        self.gridLayout_3.addWidget(self.tblsRadioButton, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.tblsComboBox = QtGui.QComboBox(streetreports)
        self.tblsComboBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblsComboBox.sizePolicy().hasHeightForWidth())
        self.tblsComboBox.setSizePolicy(sizePolicy)
        self.tblsComboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.tblsComboBox.setObjectName(_fromUtf8("tblsComboBox"))
        self.tblsComboBox.addItem(_fromUtf8(""))
        self.tblsComboBox.addItem(_fromUtf8(""))
        self.tblsComboBox.addItem(_fromUtf8(""))
        self.tblsComboBox.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.tblsComboBox, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.csvCheckBox = QtGui.QCheckBox(streetreports)
        self.csvCheckBox.setObjectName(_fromUtf8("csvCheckBox"))
        self.horizontalLayout_3.addWidget(self.csvCheckBox)
        spacerItem1 = QtGui.QSpacerItem(214, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.okPushButton = QtGui.QPushButton(streetreports)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_3.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(streetreports)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(27, 5, 3, 3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.changedStsRadioButton = QtGui.QRadioButton(streetreports)
        self.changedStsRadioButton.setChecked(True)
        self.changedStsRadioButton.setObjectName(_fromUtf8("changedStsRadioButton"))
        self.gridLayout_2.addWidget(self.changedStsRadioButton, 0, 0, 1, 1)
        self.label = QtGui.QLabel(streetreports)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.dateEdit = QtGui.QDateEdit(streetreports)
        self.dateEdit.setAcceptDrops(False)
        self.dateEdit.setFrame(True)
        self.dateEdit.setAccelerated(False)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.gridLayout_2.addWidget(self.dateEdit, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileLabel = QtGui.QLabel(streetreports)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.horizontalLayout.addWidget(self.fileLabel)
        self.fileLineEdit = QtGui.QLineEdit(streetreports)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.fileOpenPushButton = QtGui.QPushButton(streetreports)
        self.fileOpenPushButton.setText(_fromUtf8(""))
        self.fileOpenPushButton.setObjectName(_fromUtf8("fileOpenPushButton"))
        self.horizontalLayout.addWidget(self.fileOpenPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidget = QtGui.QListWidget(streetreports)
        self.listWidget.setEnabled(False)
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.retranslateUi(streetreports)
        QtCore.QMetaObject.connectSlotsByName(streetreports)

    def retranslateUi(self, streetreports):
        streetreports.setWindowTitle(_translate("streetreports", "Street Reports", None))
        self.tblsRadioButton.setText(_translate("streetreports", "Additional Tables", None))
        self.tblsComboBox.setItemText(0, _translate("streetreports", "Select a Table", None))
        self.tblsComboBox.setItemText(1, _translate("streetreports", "Maintenance", None))
        self.tblsComboBox.setItemText(2, _translate("streetreports", "Reinstatement", None))
        self.tblsComboBox.setItemText(3, _translate("streetreports", "Special Designation", None))
        self.csvCheckBox.setText(_translate("streetreports", "CSV Formatted", None))
        self.okPushButton.setText(_translate("streetreports", "OK", None))
        self.cancelPushButton.setText(_translate("streetreports", "Cancel", None))
        self.changedStsRadioButton.setText(_translate("streetreports", "Changed Streets", None))
        self.label.setText(_translate("streetreports", "Changes Since:", None))
        self.fileLabel.setText(_translate("streetreports", "Export To", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    streetreports = QtGui.QDialog()
    ui = Ui_streetreports()
    ui.setupUi(streetreports)
    streetreports.show()
    sys.exit(app.exec_())

