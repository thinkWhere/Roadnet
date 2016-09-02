# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_db_path_ui.ui'
#
# Created: Wed Dec 02 16:38:25 2015
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

class Ui_newDbPathDialog(object):
    def setupUi(self, newDbPathDialog):
        newDbPathDialog.setObjectName(_fromUtf8("newDbPathDialog"))
        newDbPathDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        newDbPathDialog.resize(700, 120)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(newDbPathDialog.sizePolicy().hasHeightForWidth())
        newDbPathDialog.setSizePolicy(sizePolicy)
        newDbPathDialog.setMinimumSize(QtCore.QSize(700, 120))
        newDbPathDialog.setMaximumSize(QtCore.QSize(900, 120))
        newDbPathDialog.setModal(True)
        newDbPathDialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.gridLayout = QtGui.QGridLayout(newDbPathDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.applyButton = QtGui.QPushButton(newDbPathDialog)
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.horizontalLayout_2.addWidget(self.applyButton)
        self.cancelButton = QtGui.QPushButton(newDbPathDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_2.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.newLabel = QtGui.QLabel(newDbPathDialog)
        self.newLabel.setObjectName(_fromUtf8("newLabel"))
        self.horizontalLayout_3.addWidget(self.newLabel)
        spacerItem1 = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.newPathLineEdit = QtGui.QLineEdit(newDbPathDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newPathLineEdit.sizePolicy().hasHeightForWidth())
        self.newPathLineEdit.setSizePolicy(sizePolicy)
        self.newPathLineEdit.setMinimumSize(QtCore.QSize(389, 0))
        self.newPathLineEdit.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.newPathLineEdit.setStyleSheet(_fromUtf8(""))
        self.newPathLineEdit.setReadOnly(False)
        self.newPathLineEdit.setObjectName(_fromUtf8("newPathLineEdit"))
        self.horizontalLayout_3.addWidget(self.newPathLineEdit)
        self.openButton = QtGui.QPushButton(newDbPathDialog)
        self.openButton.setText(_fromUtf8(""))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout_3.addWidget(self.openButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.currLabel = QtGui.QLabel(newDbPathDialog)
        self.currLabel.setObjectName(_fromUtf8("currLabel"))
        self.horizontalLayout_5.addWidget(self.currLabel)
        spacerItem2 = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.currPathLineEdit = QtGui.QLineEdit(newDbPathDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currPathLineEdit.sizePolicy().hasHeightForWidth())
        self.currPathLineEdit.setSizePolicy(sizePolicy)
        self.currPathLineEdit.setMinimumSize(QtCore.QSize(380, 0))
        self.currPathLineEdit.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.currPathLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.currPathLineEdit.setReadOnly(True)
        self.currPathLineEdit.setObjectName(_fromUtf8("currPathLineEdit"))
        self.horizontalLayout_5.addWidget(self.currPathLineEdit)
        spacerItem3 = QtGui.QSpacerItem(45, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.retranslateUi(newDbPathDialog)
        QtCore.QMetaObject.connectSlotsByName(newDbPathDialog)

    def retranslateUi(self, newDbPathDialog):
        newDbPathDialog.setWindowTitle(_translate("newDbPathDialog", "Change Database Location", None))
        self.applyButton.setText(_translate("newDbPathDialog", "Apply", None))
        self.cancelButton.setText(_translate("newDbPathDialog", "Cancel", None))
        self.newLabel.setText(_translate("newDbPathDialog", "New Database Path: ", None))
        self.currLabel.setText(_translate("newDbPathDialog", "Current Database Path:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    newDbPathDialog = QtGui.QDialog()
    ui = Ui_newDbPathDialog()
    ui.setupUi(newDbPathDialog)
    newDbPathDialog.show()
    sys.exit(app.exec_())

