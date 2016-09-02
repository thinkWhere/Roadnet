# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_admin_metadata_ui.ui'
#
# Created: Wed Dec 02 16:49:56 2015
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

class Ui_metadataDialog(object):
    def setupUi(self, metadataDialog):
        metadataDialog.setObjectName(_fromUtf8("metadataDialog"))
        metadataDialog.resize(342, 483)
        metadataDialog.setSizeGripEnabled(False)
        metadataDialog.setModal(False)
        metadataDialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.verticalLayout = QtGui.QVBoxLayout(metadataDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(metadataDialog)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.mailLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.mailLineEdit.setObjectName(_fromUtf8("mailLineEdit"))
        self.gridLayout_8.addWidget(self.mailLineEdit, 4, 1, 1, 2)
        self.classLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.classLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.classLineEdit.setReadOnly(True)
        self.classLineEdit.setObjectName(_fromUtf8("classLineEdit"))
        self.gridLayout_8.addWidget(self.classLineEdit, 8, 1, 1, 2)
        self.custLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.custLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.custLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.custLineEdit.setText(_fromUtf8(""))
        self.custLineEdit.setReadOnly(True)
        self.custLineEdit.setObjectName(_fromUtf8("custLineEdit"))
        self.gridLayout_8.addWidget(self.custLineEdit, 12, 1, 1, 1)
        self.stateLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.stateLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.stateLineEdit.setReadOnly(True)
        self.stateLineEdit.setObjectName(_fromUtf8("stateLineEdit"))
        self.gridLayout_8.addWidget(self.stateLineEdit, 9, 1, 1, 2)
        self.custLbl = QtGui.QLabel(self.groupBox_2)
        self.custLbl.setObjectName(_fromUtf8("custLbl"))
        self.gridLayout_8.addWidget(self.custLbl, 12, 0, 1, 1)
        self.gazLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.gazLineEdit.setObjectName(_fromUtf8("gazLineEdit"))
        self.gridLayout_8.addWidget(self.gazLineEdit, 3, 1, 1, 2)
        self.scopeLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.scopeLineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.scopeLineEdit.setObjectName(_fromUtf8("scopeLineEdit"))
        self.gridLayout_8.addWidget(self.scopeLineEdit, 1, 1, 1, 2)
        self.terrLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.terrLineEdit.setObjectName(_fromUtf8("terrLineEdit"))
        self.gridLayout_8.addWidget(self.terrLineEdit, 2, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 0, 2, 1, 1)
        self.stateLbl = QtGui.QLabel(self.groupBox_2)
        self.stateLbl.setObjectName(_fromUtf8("stateLbl"))
        self.gridLayout_8.addWidget(self.stateLbl, 9, 0, 1, 1)
        self.classLbl = QtGui.QLabel(self.groupBox_2)
        self.classLbl.setObjectName(_fromUtf8("classLbl"))
        self.gridLayout_8.addWidget(self.classLbl, 8, 0, 1, 1)
        self.charLbl = QtGui.QLabel(self.groupBox_2)
        self.charLbl.setObjectName(_fromUtf8("charLbl"))
        self.gridLayout_8.addWidget(self.charLbl, 11, 0, 1, 1)
        self.langLbl = QtGui.QLabel(self.groupBox_2)
        self.langLbl.setObjectName(_fromUtf8("langLbl"))
        self.gridLayout_8.addWidget(self.langLbl, 10, 0, 1, 1)
        self.charCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.charCheckBox.setObjectName(_fromUtf8("charCheckBox"))
        self.gridLayout_8.addWidget(self.charCheckBox, 11, 1, 1, 1)
        self.langCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.langCheckBox.setObjectName(_fromUtf8("langCheckBox"))
        self.gridLayout_8.addWidget(self.langCheckBox, 10, 1, 1, 1)
        self.metaLbl = QtGui.QLabel(self.groupBox_2)
        self.metaLbl.setObjectName(_fromUtf8("metaLbl"))
        self.gridLayout_8.addWidget(self.metaLbl, 7, 0, 1, 1)
        self.unitsLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.unitsLineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.unitsLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.unitsLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.unitsLineEdit.setText(_fromUtf8(""))
        self.unitsLineEdit.setReadOnly(True)
        self.unitsLineEdit.setObjectName(_fromUtf8("unitsLineEdit"))
        self.gridLayout_8.addWidget(self.unitsLineEdit, 6, 1, 1, 1)
        self.metaLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.metaLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.metaLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.metaLineEdit.setText(_fromUtf8(""))
        self.metaLineEdit.setReadOnly(True)
        self.metaLineEdit.setObjectName(_fromUtf8("metaLineEdit"))
        self.gridLayout_8.addWidget(self.metaLineEdit, 7, 1, 1, 1)
        self.nameLbl = QtGui.QLabel(self.groupBox_2)
        self.nameLbl.setObjectName(_fromUtf8("nameLbl"))
        self.gridLayout_8.addWidget(self.nameLbl, 0, 0, 1, 1)
        self.nameLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.nameLineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.nameLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout_8.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.scopeLbl = QtGui.QLabel(self.groupBox_2)
        self.scopeLbl.setObjectName(_fromUtf8("scopeLbl"))
        self.gridLayout_8.addWidget(self.scopeLbl, 1, 0, 1, 1)
        self.emailLbl = QtGui.QLabel(self.groupBox_2)
        self.emailLbl.setObjectName(_fromUtf8("emailLbl"))
        self.gridLayout_8.addWidget(self.emailLbl, 4, 0, 1, 1)
        self.gazLbl = QtGui.QLabel(self.groupBox_2)
        self.gazLbl.setObjectName(_fromUtf8("gazLbl"))
        self.gridLayout_8.addWidget(self.gazLbl, 3, 0, 1, 1)
        self.coordLbl = QtGui.QLabel(self.groupBox_2)
        self.coordLbl.setObjectName(_fromUtf8("coordLbl"))
        self.gridLayout_8.addWidget(self.coordLbl, 5, 0, 1, 1)
        self.terrLbl = QtGui.QLabel(self.groupBox_2)
        self.terrLbl.setObjectName(_fromUtf8("terrLbl"))
        self.gridLayout_8.addWidget(self.terrLbl, 2, 0, 1, 1)
        self.unitsLbl = QtGui.QLabel(self.groupBox_2)
        self.unitsLbl.setObjectName(_fromUtf8("unitsLbl"))
        self.gridLayout_8.addWidget(self.unitsLbl, 6, 0, 1, 1)
        self.coordLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.coordLineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.coordLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.coordLineEdit.setReadOnly(True)
        self.coordLineEdit.setObjectName(_fromUtf8("coordLineEdit"))
        self.gridLayout_8.addWidget(self.coordLineEdit, 5, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(metadataDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_17 = QtGui.QLabel(self.groupBox)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_3.addWidget(self.label_17)
        self.lsgLineEdit = QtGui.QLineEdit(self.groupBox)
        self.lsgLineEdit.setMinimumSize(QtCore.QSize(80, 20))
        self.lsgLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lsgLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.lsgLineEdit.setReadOnly(True)
        self.lsgLineEdit.setObjectName(_fromUtf8("lsgLineEdit"))
        self.horizontalLayout_3.addWidget(self.lsgLineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_18 = QtGui.QLabel(self.groupBox)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_3.addWidget(self.label_18)
        self.asdLineEdit = QtGui.QLineEdit(self.groupBox)
        self.asdLineEdit.setMinimumSize(QtCore.QSize(80, 20))
        self.asdLineEdit.setMaximumSize(QtCore.QSize(80, 20))
        self.asdLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.asdLineEdit.setReadOnly(True)
        self.asdLineEdit.setObjectName(_fromUtf8("asdLineEdit"))
        self.horizontalLayout_3.addWidget(self.asdLineEdit)
        self.gridLayout_9.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(metadataDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(metadataDialog)
        QtCore.QMetaObject.connectSlotsByName(metadataDialog)

    def retranslateUi(self, metadataDialog):
        metadataDialog.setWindowTitle(_translate("metadataDialog", "Metadata", None))
        self.custLbl.setText(_translate("metadataDialog", "Custodian Code:", None))
        self.stateLbl.setText(_translate("metadataDialog", "State Coding Scheme:", None))
        self.classLbl.setText(_translate("metadataDialog", "Classification Scheme:", None))
        self.charLbl.setText(_translate("metadataDialog", "Character Set: ", None))
        self.langLbl.setText(_translate("metadataDialog", "Language:", None))
        self.charCheckBox.setText(_translate("metadataDialog", "Contains Gaelic Character?", None))
        self.langCheckBox.setText(_translate("metadataDialog", "Contains Gaelic?", None))
        self.metaLbl.setText(_translate("metadataDialog", "Metadata Date:", None))
        self.nameLbl.setText(_translate("metadataDialog", "Name:", None))
        self.scopeLbl.setText(_translate("metadataDialog", "Scope:", None))
        self.emailLbl.setText(_translate("metadataDialog", "Custodian Email:", None))
        self.gazLbl.setText(_translate("metadataDialog", "Gazetter Owner:", None))
        self.coordLbl.setText(_translate("metadataDialog", "Cordinate System:", None))
        self.terrLbl.setText(_translate("metadataDialog", "Territory of use:", None))
        self.unitsLbl.setText(_translate("metadataDialog", "Units:", None))
        self.groupBox.setTitle(_translate("metadataDialog", "Latest Changes", None))
        self.label_17.setText(_translate("metadataDialog", "LSG: ", None))
        self.label_18.setText(_translate("metadataDialog", "ASD:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    metadataDialog = QtGui.QDialog()
    ui = Ui_metadataDialog()
    ui.setupUi(metadataDialog)
    metadataDialog.show()
    sys.exit(app.exec_())

