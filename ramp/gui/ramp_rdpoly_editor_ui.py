# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramp_rdpoly_editor_ui.ui'
#
# Created: Wed Jun 22 16:15:00 2016
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

class Ui_RdpolyEditorDialog(object):
    def setupUi(self, RdpolyEditorDialog):
        RdpolyEditorDialog.setObjectName(_fromUtf8("RdpolyEditorDialog"))
        RdpolyEditorDialog.resize(589, 437)
        RdpolyEditorDialog.setMinimumSize(QtCore.QSize(589, 437))
        self.gridLayout_8 = QtGui.QGridLayout(RdpolyEditorDialog)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.groupBox = QtGui.QGroupBox(RdpolyEditorDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.mclLineEdit = QtGui.QLineEdit(self.groupBox)
        self.mclLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.mclLineEdit.setReadOnly(True)
        self.mclLineEdit.setObjectName(_fromUtf8("mclLineEdit"))
        self.gridLayout_2.addWidget(self.mclLineEdit, 1, 0, 1, 1)
        self.usrnLineEdit = QtGui.QLineEdit(self.groupBox)
        self.usrnLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.usrnLineEdit.setReadOnly(True)
        self.usrnLineEdit.setObjectName(_fromUtf8("usrnLineEdit"))
        self.gridLayout_2.addWidget(self.usrnLineEdit, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 2)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)
        self.lorDescPlainTextEdit = QtGui.QPlainTextEdit(self.groupBox)
        self.lorDescPlainTextEdit.setMinimumSize(QtCore.QSize(335, 0))
        self.lorDescPlainTextEdit.setMaximumSize(QtCore.QSize(366, 16777215))
        self.lorDescPlainTextEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.lorDescPlainTextEdit.setReadOnly(True)
        self.lorDescPlainTextEdit.setObjectName(_fromUtf8("lorDescPlainTextEdit"))
        self.gridLayout_5.addWidget(self.lorDescPlainTextEdit, 2, 0, 2, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 2, 1, 1, 1)
        self.laneNumberLineEdit = QtGui.QLineEdit(self.groupBox)
        self.laneNumberLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.laneNumberLineEdit.setReadOnly(True)
        self.laneNumberLineEdit.setObjectName(_fromUtf8("laneNumberLineEdit"))
        self.gridLayout_5.addWidget(self.laneNumberLineEdit, 2, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 3, 1, 1, 1)
        self.speedLineEdit = QtGui.QLineEdit(self.groupBox)
        self.speedLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.speedLineEdit.setReadOnly(True)
        self.speedLineEdit.setObjectName(_fromUtf8("speedLineEdit"))
        self.gridLayout_5.addWidget(self.speedLineEdit, 3, 2, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(RdpolyEditorDialog)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 181))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.rdpolyLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.rdpolyLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.rdpolyLineEdit.setReadOnly(True)
        self.rdpolyLineEdit.setObjectName(_fromUtf8("rdpolyLineEdit"))
        self.gridLayout.addWidget(self.rdpolyLineEdit, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.elementComboBox = QtGui.QComboBox(self.groupBox_2)
        self.elementComboBox.setMinimumSize(QtCore.QSize(176, 0))
        self.elementComboBox.setMinimumContentsLength(0)
        self.elementComboBox.setObjectName(_fromUtf8("elementComboBox"))
        self.gridLayout.addWidget(self.elementComboBox, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.offsetComboBox = QtGui.QComboBox(self.groupBox_2)
        self.offsetComboBox.setObjectName(_fromUtf8("offsetComboBox"))
        self.gridLayout.addWidget(self.offsetComboBox, 1, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 1, 4, 1, 1)
        self.lengthLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lengthLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.lengthLineEdit.setReadOnly(True)
        self.lengthLineEdit.setObjectName(_fromUtf8("lengthLineEdit"))
        self.gridLayout.addWidget(self.lengthLineEdit, 1, 5, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)
        self.hierarchyComboBox = QtGui.QComboBox(self.groupBox_2)
        self.hierarchyComboBox.setObjectName(_fromUtf8("hierarchyComboBox"))
        self.gridLayout.addWidget(self.hierarchyComboBox, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.numberLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.numberLineEdit.setObjectName(_fromUtf8("numberLineEdit"))
        self.gridLayout.addWidget(self.numberLineEdit, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 5, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 2)
        self.combinedRefLineEdit = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.combinedRefLineEdit.sizePolicy().hasHeightForWidth())
        self.combinedRefLineEdit.setSizePolicy(sizePolicy)
        self.combinedRefLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.combinedRefLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.combinedRefLineEdit.setReadOnly(True)
        self.combinedRefLineEdit.setObjectName(_fromUtf8("combinedRefLineEdit"))
        self.gridLayout_3.addWidget(self.combinedRefLineEdit, 1, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setBaseSize(QtCore.QSize(0, 50))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RdpolyEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_8.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(RdpolyEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RdpolyEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RdpolyEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RdpolyEditorDialog)
        RdpolyEditorDialog.setTabOrder(self.elementComboBox, self.hierarchyComboBox)
        RdpolyEditorDialog.setTabOrder(self.hierarchyComboBox, self.offsetComboBox)
        RdpolyEditorDialog.setTabOrder(self.offsetComboBox, self.numberLineEdit)
        RdpolyEditorDialog.setTabOrder(self.numberLineEdit, self.lengthLineEdit)
        RdpolyEditorDialog.setTabOrder(self.lengthLineEdit, self.laneNumberLineEdit)
        RdpolyEditorDialog.setTabOrder(self.laneNumberLineEdit, self.combinedRefLineEdit)
        RdpolyEditorDialog.setTabOrder(self.combinedRefLineEdit, self.rdpolyLineEdit)
        RdpolyEditorDialog.setTabOrder(self.rdpolyLineEdit, self.usrnLineEdit)
        RdpolyEditorDialog.setTabOrder(self.usrnLineEdit, self.buttonBox)
        RdpolyEditorDialog.setTabOrder(self.buttonBox, self.speedLineEdit)
        RdpolyEditorDialog.setTabOrder(self.speedLineEdit, self.lorDescPlainTextEdit)
        RdpolyEditorDialog.setTabOrder(self.lorDescPlainTextEdit, self.mclLineEdit)

    def retranslateUi(self, RdpolyEditorDialog):
        RdpolyEditorDialog.setWindowTitle(_translate("RdpolyEditorDialog", "RAMP - Edit Polygon", None))
        self.groupBox.setTitle(_translate("RdpolyEditorDialog", "MCL Attributes", None))
        self.label.setText(_translate("RdpolyEditorDialog", "MCL ID:", None))
        self.label_3.setText(_translate("RdpolyEditorDialog", "USRN:", None))
        self.label_4.setText(_translate("RdpolyEditorDialog", "Description:", None))
        self.label_5.setText(_translate("RdpolyEditorDialog", "No. of Lanes:", None))
        self.label_6.setText(_translate("RdpolyEditorDialog", "Speed:", None))
        self.groupBox_2.setTitle(_translate("RdpolyEditorDialog", "Polygon attributes", None))
        self.label_2.setText(_translate("RdpolyEditorDialog", "Polygon ID:", None))
        self.label_10.setText(_translate("RdpolyEditorDialog", "Element:", None))
        self.label_7.setText(_translate("RdpolyEditorDialog", "desc_2:", None))
        self.label_12.setText(_translate("RdpolyEditorDialog", "Length (m):", None))
        self.label_11.setText(_translate("RdpolyEditorDialog", "Hierarchy:", None))
        self.label_8.setText(_translate("RdpolyEditorDialog", "desc_3:", None))
        self.label_9.setText(_translate("RdpolyEditorDialog", "Combined Ref:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RdpolyEditorDialog = QtGui.QDialog()
    ui = Ui_RdpolyEditorDialog()
    ui.setupUi(RdpolyEditorDialog)
    RdpolyEditorDialog.show()
    sys.exit(app.exec_())

