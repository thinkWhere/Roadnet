# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_save_record_ui.ui'
#
# Created: Fri Jan 08 15:50:26 2016
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

class Ui_AddRecordDialog(object):
    def setupUi(self, AddRecordDialog):
        AddRecordDialog.setObjectName(_fromUtf8("AddRecordDialog"))
        AddRecordDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AddRecordDialog.resize(257, 114)
        AddRecordDialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(AddRecordDialog)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(AddRecordDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.savePushButton = QtGui.QPushButton(AddRecordDialog)
        self.savePushButton.setObjectName(_fromUtf8("savePushButton"))
        self.horizontalLayout.addWidget(self.savePushButton)
        self.revertPushButton = QtGui.QPushButton(AddRecordDialog)
        self.revertPushButton.setObjectName(_fromUtf8("revertPushButton"))
        self.horizontalLayout.addWidget(self.revertPushButton)
        self.cancelPushButton = QtGui.QPushButton(AddRecordDialog)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AddRecordDialog)
        QtCore.QMetaObject.connectSlotsByName(AddRecordDialog)

    def retranslateUi(self, AddRecordDialog):
        AddRecordDialog.setWindowTitle(_translate("AddRecordDialog", "Save changes", None))
        self.label.setText(_translate("AddRecordDialog", "Save changes to record?", None))
        self.savePushButton.setText(_translate("AddRecordDialog", "Yes", None))
        self.revertPushButton.setText(_translate("AddRecordDialog", "No", None))
        self.cancelPushButton.setText(_translate("AddRecordDialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AddRecordDialog = QtGui.QDialog()
    ui = Ui_AddRecordDialog()
    ui.setupUi(AddRecordDialog)
    AddRecordDialog.show()
    sys.exit(app.exec_())

