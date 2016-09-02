# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_edit_coords_ui.ui'
#
# Created: Thu Jan 07 00:50:21 2016
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

class Ui_editCoordsDialog(object):
    def setupUi(self, editCoordsDialog):
        editCoordsDialog.setObjectName(_fromUtf8("editCoordsDialog"))
        editCoordsDialog.setWindowModality(QtCore.Qt.WindowModal)
        editCoordsDialog.resize(277, 165)
        editCoordsDialog.setModal(True)
        self.gridLayout_2 = QtGui.QGridLayout(editCoordsDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okPushButton = QtGui.QPushButton(editCoordsDialog)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout.addWidget(self.okPushButton)
        self.cancelPushButton = QtGui.QPushButton(editCoordsDialog)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.startPushButton = QtGui.QPushButton(editCoordsDialog)
        self.startPushButton.setCheckable(True)
        self.startPushButton.setObjectName(_fromUtf8("startPushButton"))
        self.gridLayout.addWidget(self.startPushButton, 1, 0, 1, 1)
        self.startXLineEdit = QtGui.QLineEdit(editCoordsDialog)
        self.startXLineEdit.setMaxLength(10)
        self.startXLineEdit.setObjectName(_fromUtf8("startXLineEdit"))
        self.gridLayout.addWidget(self.startXLineEdit, 1, 1, 1, 1)
        self.endPushButton = QtGui.QPushButton(editCoordsDialog)
        self.endPushButton.setCheckable(True)
        self.endPushButton.setObjectName(_fromUtf8("endPushButton"))
        self.gridLayout.addWidget(self.endPushButton, 2, 0, 1, 1)
        self.endXLineEdit = QtGui.QLineEdit(editCoordsDialog)
        self.endXLineEdit.setMaxLength(10)
        self.endXLineEdit.setObjectName(_fromUtf8("endXLineEdit"))
        self.gridLayout.addWidget(self.endXLineEdit, 2, 1, 1, 1)
        self.startYLineEdit = QtGui.QLineEdit(editCoordsDialog)
        self.startYLineEdit.setMaxLength(10)
        self.startYLineEdit.setObjectName(_fromUtf8("startYLineEdit"))
        self.gridLayout.addWidget(self.startYLineEdit, 1, 2, 1, 1)
        self.endYLineEdit = QtGui.QLineEdit(editCoordsDialog)
        self.endYLineEdit.setMaxLength(10)
        self.endYLineEdit.setObjectName(_fromUtf8("endYLineEdit"))
        self.gridLayout.addWidget(self.endYLineEdit, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(editCoordsDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(editCoordsDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.usrnLabel = QtGui.QLabel(editCoordsDialog)
        self.usrnLabel.setObjectName(_fromUtf8("usrnLabel"))
        self.gridLayout_2.addWidget(self.usrnLabel, 0, 1, 1, 1)

        self.retranslateUi(editCoordsDialog)
        QtCore.QMetaObject.connectSlotsByName(editCoordsDialog)

    def retranslateUi(self, editCoordsDialog):
        editCoordsDialog.setWindowTitle(_translate("editCoordsDialog", "Edit start/end coordinates", None))
        self.okPushButton.setText(_translate("editCoordsDialog", "OK", None))
        self.cancelPushButton.setText(_translate("editCoordsDialog", "Cancel", None))
        self.startPushButton.setText(_translate("editCoordsDialog", "Start", None))
        self.endPushButton.setText(_translate("editCoordsDialog", "End", None))
        self.label_2.setText(_translate("editCoordsDialog", "X", None))
        self.label_3.setText(_translate("editCoordsDialog", "Y", None))
        self.usrnLabel.setText(_translate("editCoordsDialog", "USRN:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    editCoordsDialog = QtGui.QDialog()
    ui = Ui_editCoordsDialog()
    ui.setupUi(editCoordsDialog)
    editCoordsDialog.show()
    sys.exit(app.exec_())

