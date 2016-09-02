# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_admin_street_reports_alert_ui.ui'
#
# Created: Thu Jul 30 14:35:27 2015
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

class Ui_strtAdminAlert(object):
    def setupUi(self, strtAdminAlert):
        strtAdminAlert.setObjectName(_fromUtf8("strtAdminAlert"))
        strtAdminAlert.resize(258, 81)
        strtAdminAlert.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout = QtGui.QGridLayout(strtAdminAlert)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(strtAdminAlert)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelPushButton = QtGui.QPushButton(strtAdminAlert)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(strtAdminAlert)
        QtCore.QMetaObject.connectSlotsByName(strtAdminAlert)

    def retranslateUi(self, strtAdminAlert):
        strtAdminAlert.setWindowTitle(_translate("strtAdminAlert", " ", None))
        self.label_2.setText(_translate("strtAdminAlert", "Please Select an Addtional Table", None))
        self.cancelPushButton.setText(_translate("strtAdminAlert", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    strtAdminAlert = QtGui.QDialog()
    ui = Ui_strtAdminAlert()
    ui.setupUi(strtAdminAlert)
    strtAdminAlert.show()
    sys.exit(app.exec_())

