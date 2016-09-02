# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_roadnet_password_ui.ui'
#
# Created: Wed Oct 28 16:22:12 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt

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

class Ui_chPasswordDlg(object):
    def setupUi(self, chPasswordDlg):
        chPasswordDlg.setObjectName(_fromUtf8("chPasswordDlg"))
        chPasswordDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        chPasswordDlg.resize(342, 180)
        chPasswordDlg.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(chPasswordDlg.sizePolicy().hasHeightForWidth())
        chPasswordDlg.setSizePolicy(sizePolicy)
        chPasswordDlg.setMinimumSize(QtCore.QSize(342, 180))
        chPasswordDlg.setMaximumSize(QtCore.QSize(342, 180))
        chPasswordDlg.setModal(True)
        self.gridLayout = QtGui.QGridLayout(chPasswordDlg)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(chPasswordDlg)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.oldPwdLineEdit = QtGui.QLineEdit(chPasswordDlg)
        self.oldPwdLineEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.oldPwdLineEdit.setObjectName(_fromUtf8("oldPwdLineEdit"))
        self.horizontalLayout_3.addWidget(self.oldPwdLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(chPasswordDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(37, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pwdLineEdit = QtGui.QLineEdit(chPasswordDlg)
        self.pwdLineEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.pwdLineEdit.setObjectName(_fromUtf8("pwdLineEdit"))
        self.horizontalLayout.addWidget(self.pwdLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(chPasswordDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.confirmLineEdit = QtGui.QLineEdit(chPasswordDlg)
        self.confirmLineEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.confirmLineEdit.setObjectName(_fromUtf8("confirmLineEdit"))
        self.horizontalLayout_2.addWidget(self.confirmLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.okCancelButton = QtGui.QDialogButtonBox(chPasswordDlg)
        self.okCancelButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.okCancelButton.setObjectName(_fromUtf8("okCancelButton"))
        self.gridLayout.addWidget(self.okCancelButton, 1, 0, 1, 1)

        self.retranslateUi(chPasswordDlg)
        QtCore.QMetaObject.connectSlotsByName(chPasswordDlg)

    def retranslateUi(self, chPasswordDlg):
        chPasswordDlg.setWindowTitle(_translate("chPasswordDlg", "Change Password", None))
        self.label_3.setText(_translate("chPasswordDlg", "Current Password: ", None))
        self.label.setText(_translate("chPasswordDlg", "New Password: ", None))
        self.label_2.setText(_translate("chPasswordDlg", "Confirm New Password:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    chPasswordDlg = QtGui.QDialog()
    ui = Ui_chPasswordDlg()
    ui.setupUi(chPasswordDlg)
    chPasswordDlg.show()
    sys.exit(app.exec_())

