# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_edit_esu_link_ui.ui'
#
# Created: Tue Nov 17 16:52:02 2015
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

class Ui_editEsuLinkDialog(object):
    def setupUi(self, editEsuLinkDialog):
        editEsuLinkDialog.setObjectName(_fromUtf8("editEsuLinkDialog"))
        editEsuLinkDialog.setWindowModality(QtCore.Qt.WindowModal)
        editEsuLinkDialog.resize(213, 267)
        editEsuLinkDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(editEsuLinkDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.usrnLabel = QtGui.QLabel(editEsuLinkDialog)
        self.usrnLabel.setObjectName(_fromUtf8("usrnLabel"))
        self.gridLayout.addWidget(self.usrnLabel, 0, 0, 1, 1)
        self.label = QtGui.QLabel(editEsuLinkDialog)
        self.label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okPushButton = QtGui.QPushButton(editEsuLinkDialog)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(editEsuLinkDialog)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.esuLinkListWidget = QtGui.QListWidget(editEsuLinkDialog)
        self.esuLinkListWidget.setObjectName(_fromUtf8("esuLinkListWidget"))
        self.gridLayout.addWidget(self.esuLinkListWidget, 1, 0, 1, 2)

        self.retranslateUi(editEsuLinkDialog)
        QtCore.QMetaObject.connectSlotsByName(editEsuLinkDialog)

    def retranslateUi(self, editEsuLinkDialog):
        editEsuLinkDialog.setWindowTitle(_translate("editEsuLinkDialog", "Edit ESU/Street Links", None))
        self.usrnLabel.setText(_translate("editEsuLinkDialog", "USRN:", None))
        self.label.setText(_translate("editEsuLinkDialog", "Modify the selection on the map canvas to add/remove ESU\'s.", None))
        self.okPushButton.setText(_translate("editEsuLinkDialog", "OK", None))
        self.cancelPushButton.setText(_translate("editEsuLinkDialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    editEsuLinkDialog = QtGui.QDialog()
    ui = Ui_editEsuLinkDialog()
    ui.setupUi(editEsuLinkDialog)
    editEsuLinkDialog.show()
    sys.exit(app.exec_())

