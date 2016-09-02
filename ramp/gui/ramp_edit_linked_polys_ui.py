# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramp_edit_linked_polys_ui.ui'
#
# Created: Fri Jun 10 11:38:28 2016
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

class Ui_editLinkedPolysDialog(object):
    def setupUi(self, editLinkedPolysDialog):
        editLinkedPolysDialog.setObjectName(_fromUtf8("editLinkedPolysDialog"))
        editLinkedPolysDialog.setWindowModality(QtCore.Qt.WindowModal)
        editLinkedPolysDialog.resize(250, 267)
        editLinkedPolysDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(editLinkedPolysDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.linkedPolysLabel = QtGui.QLabel(editLinkedPolysDialog)
        self.linkedPolysLabel.setObjectName(_fromUtf8("linkedPolysLabel"))
        self.gridLayout.addWidget(self.linkedPolysLabel, 0, 0, 1, 1)
        self.label = QtGui.QLabel(editLinkedPolysDialog)
        self.label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.linkedPolysListWidget = QtGui.QListWidget(editLinkedPolysDialog)
        self.linkedPolysListWidget.setObjectName(_fromUtf8("linkedPolysListWidget"))
        self.gridLayout.addWidget(self.linkedPolysListWidget, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(editLinkedPolysDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(editLinkedPolysDialog)
        QtCore.QMetaObject.connectSlotsByName(editLinkedPolysDialog)

    def retranslateUi(self, editLinkedPolysDialog):
        editLinkedPolysDialog.setWindowTitle(_translate("editLinkedPolysDialog", "Edit linked polygons", None))
        self.linkedPolysLabel.setText(_translate("editLinkedPolysDialog", "Linked polygons:", None))
        self.label.setText(_translate("editLinkedPolysDialog", "Modify the selection on the map canvas to link/unlink polygons.", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    editLinkedPolysDialog = QtGui.QDialog()
    ui = Ui_editLinkedPolysDialog()
    ui.setupUi(editLinkedPolysDialog)
    editLinkedPolysDialog.show()
    sys.exit(app.exec_())

