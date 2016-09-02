# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_quick_find_ui.ui'
#
# Created: Thu Jul 16 13:26:32 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt
import os

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

class Ui_quickFindDialog(object):
    def setupUi(self, quickFindDialog):
        quickFindDialog.setObjectName(_fromUtf8("quickFindDialog"))
        quickFindDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        quickFindDialog.resize(361, 66)
        quickFindDialog.setModal(True)
        quickFindDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        quickFindDialog.setWindowIcon(QtGui.QIcon())
        rn_icon = QtGui.QIcon()
        app_root = os.path.dirname(os.path.dirname(__file__))
        rn_icon.addPixmap(QtGui.QPixmap(os.path.join(app_root,
                                                     "image",
                                                     "rn_logo_v2.png")))
        quickFindDialog.setWindowIcon(rn_icon)
        self.gridLayout = QtGui.QGridLayout(quickFindDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.usrnLabel = QtGui.QLabel(quickFindDialog)
        self.usrnLabel.setObjectName(_fromUtf8("usrnLabel"))
        self.horizontalLayout.addWidget(self.usrnLabel)
        self.usrnLineEdit = QtGui.QLineEdit(quickFindDialog)
        self.usrnLineEdit.setObjectName(_fromUtf8("usrnLineEdit"))
        self.horizontalLayout.addWidget(self.usrnLineEdit)
        self.goPushButton = QtGui.QPushButton(quickFindDialog)
        self.goPushButton.setObjectName(_fromUtf8("goPushButton"))
        self.horizontalLayout.addWidget(self.goPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(quickFindDialog)
        QtCore.QMetaObject.connectSlotsByName(quickFindDialog)

    def retranslateUi(self, quickFindDialog):
        quickFindDialog.setWindowTitle(_translate("quickFindDialog", "Quick Find Record", None))
        self.usrnLabel.setText(_translate("quickFindDialog", "Enter USRN:", None))
        self.goPushButton.setText(_translate("quickFindDialog", "Go", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    quickFindDialog = QtGui.QDialog()
    ui = Ui_quickFindDialog()
    ui.setupUi(quickFindDialog)
    quickFindDialog.show()
    sys.exit(app.exec_())

