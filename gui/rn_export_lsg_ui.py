# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_export_lsg_ui.ui'
#
# Created: Wed Dec 02 13:52:52 2015
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

class Ui_exportLsgDialog(object):
    def setupUi(self, exportLsgDialog):
        exportLsgDialog.setObjectName(_fromUtf8("exportLsgDialog"))
        exportLsgDialog.resize(453, 193)
        exportLsgDialog.setMinimumSize(QtCore.QSize(0, 193))
        exportLsgDialog.setMaximumSize(QtCore.QSize(16777215, 193))
        exportLsgDialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout_3 = QtGui.QGridLayout(exportLsgDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fileLabel = QtGui.QLabel(exportLsgDialog)
        self.fileLabel.setObjectName(_fromUtf8("fileLabel"))
        self.horizontalLayout_2.addWidget(self.fileLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileLineEdit = QtGui.QLineEdit(exportLsgDialog)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.openPushButton = QtGui.QPushButton(exportLsgDialog)
        self.openPushButton.setText(_fromUtf8(""))
        self.openPushButton.setObjectName(_fromUtf8("openPushButton"))
        self.horizontalLayout.addWidget(self.openPushButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(exportLsgDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dtf63RadioButton = QtGui.QRadioButton(self.groupBox)
        self.dtf63RadioButton.setObjectName(_fromUtf8("dtf63RadioButton"))
        self.gridLayout.addWidget(self.dtf63RadioButton, 0, 0, 1, 1)
        self.dtf71RadioButton = QtGui.QRadioButton(self.groupBox)
        self.dtf71RadioButton.setObjectName(_fromUtf8("dtf71RadioButton"))
        self.gridLayout.addWidget(self.dtf71RadioButton, 1, 0, 1, 1)
        self.sdtfRadioButton = QtGui.QRadioButton(self.groupBox)
        self.sdtfRadioButton.setChecked(True)
        self.sdtfRadioButton.setObjectName(_fromUtf8("sdtfRadioButton"))
        self.gridLayout.addWidget(self.sdtfRadioButton, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.asdCheckBox = QtGui.QCheckBox(self.groupBox)
        self.asdCheckBox.setEnabled(False)
        self.asdCheckBox.setObjectName(_fromUtf8("asdCheckBox"))
        self.gridLayout.addWidget(self.asdCheckBox, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 2)
        self.closedStreetsCheckBox = QtGui.QCheckBox(exportLsgDialog)
        self.closedStreetsCheckBox.setObjectName(_fromUtf8("closedStreetsCheckBox"))
        self.gridLayout_3.addWidget(self.closedStreetsCheckBox, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.okPushButton = QtGui.QPushButton(exportLsgDialog)
        self.okPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout_3.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(exportLsgDialog)
        self.cancelPushButton.setMaximumSize(QtCore.QSize(94, 16777215))
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)

        self.retranslateUi(exportLsgDialog)
        QtCore.QMetaObject.connectSlotsByName(exportLsgDialog)

    def retranslateUi(self, exportLsgDialog):
        exportLsgDialog.setWindowTitle(_translate("exportLsgDialog", "Export LSG", None))
        self.fileLabel.setText(_translate("exportLsgDialog", "Export To", None))
        self.dtf63RadioButton.setText(_translate("exportLsgDialog", "DTF 6.3", None))
        self.dtf71RadioButton.setText(_translate("exportLsgDialog", "DTF 7.1", None))
        self.sdtfRadioButton.setText(_translate("exportLsgDialog", "SDTF 1.0", None))
        self.asdCheckBox.setText(_translate("exportLsgDialog", "Include ASD?", None))
        self.closedStreetsCheckBox.setText(_translate("exportLsgDialog", "Include Closed Streets", None))
        self.okPushButton.setText(_translate("exportLsgDialog", "OK", None))
        self.cancelPushButton.setText(_translate("exportLsgDialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    exportLsgDialog = QtGui.QDialog()
    ui = Ui_exportLsgDialog()
    ui.setupUi(exportLsgDialog)
    exportLsgDialog.show()
    sys.exit(app.exec_())

