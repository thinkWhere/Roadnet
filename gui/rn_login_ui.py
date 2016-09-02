# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rn_login_ui.ui'
#
# Created: Thu Oct 15 13:58:07 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_loginDialog(object):
    def setupUi(self, loginDialog):
        loginDialog.setObjectName(_fromUtf8("loginDialog"))
        loginDialog.resize(250, 147)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loginDialog.sizePolicy().hasHeightForWidth())
        loginDialog.setSizePolicy(sizePolicy)
        loginDialog.setMinimumSize(QtCore.QSize(250, 147))
        loginDialog.setMaximumSize(QtCore.QSize(250, 147))
        loginDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        font = QtGui.QFont()
        font.setPointSize(12)
        loginDialog.setFont(font)
        self.verticalLayout_2 = QtGui.QVBoxLayout(loginDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(loginDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.usrLineEdit = QtGui.QLineEdit(loginDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usrLineEdit.sizePolicy().hasHeightForWidth())
        self.usrLineEdit.setSizePolicy(sizePolicy)
        self.usrLineEdit.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.usrLineEdit.setFont(font)
        self.usrLineEdit.setText(_fromUtf8(""))
        self.usrLineEdit.setObjectName(_fromUtf8("usrLineEdit"))
        self.horizontalLayout.addWidget(self.usrLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(loginDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pwdLineEdit = QtGui.QLineEdit(loginDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pwdLineEdit.sizePolicy().hasHeightForWidth())
        self.pwdLineEdit.setSizePolicy(sizePolicy)
        self.pwdLineEdit.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pwdLineEdit.setFont(font)
        self.pwdLineEdit.setText(_fromUtf8(""))
        self.pwdLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.pwdLineEdit.setObjectName(_fromUtf8("pwdLineEdit"))
        self.horizontalLayout_2.addWidget(self.pwdLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.okCancelButton = QtGui.QDialogButtonBox(loginDialog)
        self.okCancelButton.setMaximumSize(QtCore.QSize(195, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.okCancelButton.setFont(font)
        self.okCancelButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.okCancelButton.setObjectName(_fromUtf8("okCancelButton"))
        self.verticalLayout_2.addWidget(self.okCancelButton)

        self.retranslateUi(loginDialog)
        QtCore.QMetaObject.connectSlotsByName(loginDialog)

    def retranslateUi(self, loginDialog):
        loginDialog.setWindowTitle(_translate("loginDialog", "Login", None))
        self.label.setText(_translate("loginDialog", "User Name:", None))
        self.label_2.setText(_translate("loginDialog", "Password:", None))

