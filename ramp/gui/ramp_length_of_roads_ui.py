# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramp_length_of_roads_ui.ui'
#
# Created: Wed May 25 11:35:51 2016
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

class Ui_RampLengthOfRoadsDialog(object):
    def setupUi(self, RampLengthOfRoadsDialog):
        RampLengthOfRoadsDialog.setObjectName(_fromUtf8("RampLengthOfRoadsDialog"))
        RampLengthOfRoadsDialog.resize(494, 727)
        RampLengthOfRoadsDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RampLengthOfRoadsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(RampLengthOfRoadsDialog)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RampLengthOfRoadsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(RampLengthOfRoadsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RampLengthOfRoadsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RampLengthOfRoadsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RampLengthOfRoadsDialog)

    def retranslateUi(self, RampLengthOfRoadsDialog):
        RampLengthOfRoadsDialog.setWindowTitle(_translate("RampLengthOfRoadsDialog", "RAMP - Length of Roads", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RampLengthOfRoadsDialog = QtGui.QDialog()
    ui = Ui_RampLengthOfRoadsDialog()
    ui.setupUi(RampLengthOfRoadsDialog)
    RampLengthOfRoadsDialog.show()
    sys.exit(app.exec_())

