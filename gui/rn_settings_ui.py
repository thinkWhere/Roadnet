# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tw-johns/Roadnet/gui/rn_settings_ui.ui'
#
# Created: Tue Jun  7 09:24:20 2016
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

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName(_fromUtf8("settingsDialog"))
        settingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        settingsDialog.resize(342, 226)
        settingsDialog.setMinimumSize(QtCore.QSize(342, 226))
        settingsDialog.setMaximumSize(QtCore.QSize(342, 226))
        self.widget = QtGui.QWidget(settingsDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 323, 211))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ShapeEditing = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShapeEditing.sizePolicy().hasHeightForWidth())
        self.ShapeEditing.setSizePolicy(sizePolicy)
        self.ShapeEditing.setMinimumSize(QtCore.QSize(319, 101))
        self.ShapeEditing.setMaximumSize(QtCore.QSize(319, 101))
        self.ShapeEditing.setObjectName(_fromUtf8("ShapeEditing"))
        self.rdpolyCheckBox = QtGui.QCheckBox(self.ShapeEditing)
        self.rdpolyCheckBox.setGeometry(QtCore.QRect(11, 63, 271, 26))
        self.rdpolyCheckBox.setMaximumSize(QtCore.QSize(271, 26))
        self.rdpolyCheckBox.setChecked(True)
        self.rdpolyCheckBox.setObjectName(_fromUtf8("rdpolyCheckBox"))
        self.esuCheckBox = QtGui.QCheckBox(self.ShapeEditing)
        self.esuCheckBox.setGeometry(QtCore.QRect(11, 31, 261, 26))
        self.esuCheckBox.setChecked(True)
        self.esuCheckBox.setObjectName(_fromUtf8("esuCheckBox"))
        self.verticalLayout.addWidget(self.ShapeEditing)
        self.rampGroupBox = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rampGroupBox.sizePolicy().hasHeightForWidth())
        self.rampGroupBox.setSizePolicy(sizePolicy)
        self.rampGroupBox.setMinimumSize(QtCore.QSize(319, 61))
        self.rampGroupBox.setMaximumSize(QtCore.QSize(319, 61))
        self.rampGroupBox.setObjectName(_fromUtf8("rampGroupBox"))
        self.rampCheckBox = QtGui.QCheckBox(self.rampGroupBox)
        self.rampCheckBox.setGeometry(QtCore.QRect(20, 30, 201, 22))
        self.rampCheckBox.setObjectName(_fromUtf8("rampCheckBox"))
        self.verticalLayout.addWidget(self.rampGroupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem = QtGui.QSpacerItem(228, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtGui.QFormLayout.LabelRole, spacerItem)
        self.okButton = QtGui.QPushButton(self.widget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.okButton)
        self.verticalLayout_2.addLayout(self.formLayout)

        self.retranslateUi(settingsDialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), settingsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(_translate("settingsDialog", "Settings", None))
        self.ShapeEditing.setTitle(_translate("settingsDialog", "Shape editing", None))
        self.rdpolyCheckBox.setText(_translate("settingsDialog", "Prevent overlapping polygons", None))
        self.esuCheckBox.setText(_translate("settingsDialog", "Automatically split ESU\'s", None))
        self.rampGroupBox.setTitle(_translate("settingsDialog", "RAMP settings", None))
        self.rampCheckBox.setText(_translate("settingsDialog", "Enable RAMP", None))
        self.okButton.setText(_translate("settingsDialog", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    settingsDialog = QtGui.QDialog()
    ui = Ui_settingsDialog()
    ui.setupUi(settingsDialog)
    settingsDialog.show()
    sys.exit(app.exec_())

