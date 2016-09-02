# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramp_mcl_editor_ui.ui'
#
# Created: Tue Jun 21 13:13:02 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MclEditorDialog(object):
    def setupUi(self, MclEditorDialog):
        MclEditorDialog.setObjectName(_fromUtf8("MclEditorDialog"))
        MclEditorDialog.resize(694, 473)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MclEditorDialog.sizePolicy().hasHeightForWidth())
        MclEditorDialog.setSizePolicy(sizePolicy)
        MclEditorDialog.setMinimumSize(QtCore.QSize(562, 473))
        MclEditorDialog.setMaximumSize(QtCore.QSize(694, 473))
        self.buttonBox = QtGui.QDialogButtonBox(MclEditorDialog)
        self.buttonBox.setGeometry(QtCore.QRect(480, 440, 211, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox_2 = QtGui.QGroupBox(MclEditorDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 362, 80))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 2, 1, 1)
        self.mclLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.mclLineEdit.setAutoFillBackground(False)
        self.mclLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.mclLineEdit.setReadOnly(True)
        self.mclLineEdit.setObjectName(_fromUtf8("mclLineEdit"))
        self.gridLayout_2.addWidget(self.mclLineEdit, 1, 0, 1, 1)
        self.combinedRefLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.combinedRefLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.combinedRefLineEdit.setReadOnly(True)
        self.combinedRefLineEdit.setObjectName(_fromUtf8("combinedRefLineEdit"))
        self.gridLayout_2.addWidget(self.combinedRefLineEdit, 1, 1, 1, 1)
        self.lengthLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lengthLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.lengthLineEdit.setReadOnly(True)
        self.lengthLineEdit.setObjectName(_fromUtf8("lengthLineEdit"))
        self.gridLayout_2.addWidget(self.lengthLineEdit, 1, 2, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(MclEditorDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 100, 551, 321))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.widget = QtGui.QWidget(self.groupBox_3)
        self.widget.setGeometry(QtCore.QRect(19, 27, 271, 170))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_3 = QtGui.QFormLayout(self.widget)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setMargin(0)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.usrnLineEdit = QtGui.QLineEdit(self.widget)
        self.usrnLineEdit.setObjectName(_fromUtf8("usrnLineEdit"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.usrnLineEdit)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.ref1LineEdit = QtGui.QLineEdit(self.widget)
        self.ref1LineEdit.setObjectName(_fromUtf8("ref1LineEdit"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.ref1LineEdit)
        self.label_8 = QtGui.QLabel(self.widget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.ref2LineEdit = QtGui.QLineEdit(self.widget)
        self.ref2LineEdit.setObjectName(_fromUtf8("ref2LineEdit"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.ref2LineEdit)
        self.streetClassComboBox = QtGui.QComboBox(self.widget)
        self.streetClassComboBox.setObjectName(_fromUtf8("streetClassComboBox"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.streetClassComboBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout_3.setItem(4, QtGui.QFormLayout.FieldRole, spacerItem)
        self.sectionDescriptionPlainTextEdit = QtGui.QPlainTextEdit(self.groupBox_3)
        self.sectionDescriptionPlainTextEdit.setGeometry(QtCore.QRect(19, 240, 521, 78))
        self.sectionDescriptionPlainTextEdit.setObjectName(_fromUtf8("sectionDescriptionPlainTextEdit"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(19, 210, 119, 19))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.widget1 = QtGui.QWidget(self.groupBox_3)
        self.widget1.setGeometry(QtCore.QRect(299, 27, 241, 201))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.formLayout_2 = QtGui.QFormLayout(self.widget1)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_13 = QtGui.QLabel(self.widget1)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_13)
        self.label_10 = QtGui.QLabel(self.widget1)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_10)
        self.label_11 = QtGui.QLabel(self.widget1)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_11)
        self.label_12 = QtGui.QLabel(self.widget1)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_12)
        self.label_14 = QtGui.QLabel(self.widget1)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_14)
        self.laneNumberComboBox = QtGui.QComboBox(self.widget1)
        self.laneNumberComboBox.setObjectName(_fromUtf8("laneNumberComboBox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.laneNumberComboBox)
        self.carriagewayComboBox = QtGui.QComboBox(self.widget1)
        self.carriagewayComboBox.setObjectName(_fromUtf8("carriagewayComboBox"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.carriagewayComboBox)
        self.ruralUrbanComboBox = QtGui.QComboBox(self.widget1)
        self.ruralUrbanComboBox.setObjectName(_fromUtf8("ruralUrbanComboBox"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.ruralUrbanComboBox)
        self.speedLimitComboBox = QtGui.QComboBox(self.widget1)
        self.speedLimitComboBox.setObjectName(_fromUtf8("speedLimitComboBox"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.speedLimitComboBox)
        self.sectionTypeComboBox = QtGui.QComboBox(self.widget1)
        self.sectionTypeComboBox.setObjectName(_fromUtf8("sectionTypeComboBox"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.sectionTypeComboBox)
        self.groupBox = QtGui.QGroupBox(MclEditorDialog)
        self.groupBox.setGeometry(QtCore.QRect(570, 100, 111, 261))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.editLinksPushButton = QtGui.QPushButton(self.groupBox)
        self.editLinksPushButton.setObjectName(_fromUtf8("editLinksPushButton"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.editLinksPushButton)
        self.linkedPolygonsListWidget = QtGui.QListWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linkedPolygonsListWidget.sizePolicy().hasHeightForWidth())
        self.linkedPolygonsListWidget.setSizePolicy(sizePolicy)
        self.linkedPolygonsListWidget.setMinimumSize(QtCore.QSize(85, 192))
        self.linkedPolygonsListWidget.setMaximumSize(QtCore.QSize(85, 192))
        self.linkedPolygonsListWidget.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.linkedPolygonsListWidget.setObjectName(_fromUtf8("linkedPolygonsListWidget"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.linkedPolygonsListWidget)

        self.retranslateUi(MclEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MclEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MclEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MclEditorDialog)
        MclEditorDialog.setTabOrder(self.usrnLineEdit, self.streetClassComboBox)
        MclEditorDialog.setTabOrder(self.streetClassComboBox, self.ref1LineEdit)
        MclEditorDialog.setTabOrder(self.ref1LineEdit, self.ref2LineEdit)
        MclEditorDialog.setTabOrder(self.ref2LineEdit, self.laneNumberComboBox)
        MclEditorDialog.setTabOrder(self.laneNumberComboBox, self.carriagewayComboBox)
        MclEditorDialog.setTabOrder(self.carriagewayComboBox, self.ruralUrbanComboBox)
        MclEditorDialog.setTabOrder(self.ruralUrbanComboBox, self.speedLimitComboBox)
        MclEditorDialog.setTabOrder(self.speedLimitComboBox, self.sectionTypeComboBox)
        MclEditorDialog.setTabOrder(self.sectionTypeComboBox, self.sectionDescriptionPlainTextEdit)
        MclEditorDialog.setTabOrder(self.sectionDescriptionPlainTextEdit, self.editLinksPushButton)
        MclEditorDialog.setTabOrder(self.editLinksPushButton, self.linkedPolygonsListWidget)
        MclEditorDialog.setTabOrder(self.linkedPolygonsListWidget, self.mclLineEdit)
        MclEditorDialog.setTabOrder(self.mclLineEdit, self.combinedRefLineEdit)
        MclEditorDialog.setTabOrder(self.combinedRefLineEdit, self.lengthLineEdit)
        MclEditorDialog.setTabOrder(self.lengthLineEdit, self.buttonBox)

    def retranslateUi(self, MclEditorDialog):
        MclEditorDialog.setWindowTitle(_translate("MclEditorDialog", "RAMP - Edit MCL", None))
        self.groupBox_2.setTitle(_translate("MclEditorDialog", "Fixed Attributes", None))
        self.label.setText(_translate("MclEditorDialog", "MCL ID:", None))
        self.label_4.setText(_translate("MclEditorDialog", "Combined Ref:", None))
        self.label_7.setText(_translate("MclEditorDialog", "Length (m):", None))
        self.groupBox_3.setTitle(_translate("MclEditorDialog", "Editable Attributes", None))
        self.label_2.setText(_translate("MclEditorDialog", "USRN:", None))
        self.label_5.setText(_translate("MclEditorDialog", "Street Class:", None))
        self.label_6.setText(_translate("MclEditorDialog", "Ref 1:", None))
        self.label_8.setText(_translate("MclEditorDialog", "Ref 2:", None))
        self.label_3.setText(_translate("MclEditorDialog", "Section Desciption:", None))
        self.label_13.setText(_translate("MclEditorDialog", "Carriageway:", None))
        self.label_10.setText(_translate("MclEditorDialog", "Rural / Urban:", None))
        self.label_11.setText(_translate("MclEditorDialog", "Speed Limit:", None))
        self.label_12.setText(_translate("MclEditorDialog", "Section Type:", None))
        self.label_14.setText(_translate("MclEditorDialog", "Number of Lanes:", None))
        self.groupBox.setTitle(_translate("MclEditorDialog", "Linked Polygons", None))
        self.editLinksPushButton.setText(_translate("MclEditorDialog", "Edit Links", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MclEditorDialog = QtGui.QDialog()
    ui = Ui_MclEditorDialog()
    ui.setupUi(MclEditorDialog)
    MclEditorDialog.show()
    sys.exit(app.exec_())

