# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramp_mcl_auto_numbering_ui.ui'
#
# Created: Mon Jun 27 15:59:50 2016
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

class Ui_mclAutoNumberingDialog(object):
    def setupUi(self, mclAutoNumberingDialog):
        mclAutoNumberingDialog.setObjectName(_fromUtf8("mclAutoNumberingDialog"))
        mclAutoNumberingDialog.setWindowModality(QtCore.Qt.WindowModal)
        mclAutoNumberingDialog.resize(332, 330)
        mclAutoNumberingDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(mclAutoNumberingDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(mclAutoNumberingDialog)
        self.label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.linkedPolysLabel = QtGui.QLabel(mclAutoNumberingDialog)
        self.linkedPolysLabel.setObjectName(_fromUtf8("linkedPolysLabel"))
        self.verticalLayout.addWidget(self.linkedPolysLabel)
        self.mclListWidget = QtGui.QListWidget(mclAutoNumberingDialog)
        self.mclListWidget.setObjectName(_fromUtf8("mclListWidget"))
        self.verticalLayout.addWidget(self.mclListWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 2, 1)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.startValueSpinBox = QtGui.QSpinBox(mclAutoNumberingDialog)
        self.startValueSpinBox.setObjectName(_fromUtf8("startValueSpinBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.startValueSpinBox)
        self.label_3 = QtGui.QLabel(mclAutoNumberingDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.incrementSpinBox = QtGui.QSpinBox(mclAutoNumberingDialog)
        self.incrementSpinBox.setObjectName(_fromUtf8("incrementSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.incrementSpinBox)
        self.label_2 = QtGui.QLabel(mclAutoNumberingDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(mclAutoNumberingDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(mclAutoNumberingDialog)
        QtCore.QMetaObject.connectSlotsByName(mclAutoNumberingDialog)
        mclAutoNumberingDialog.setTabOrder(self.startValueSpinBox, self.incrementSpinBox)
        mclAutoNumberingDialog.setTabOrder(self.incrementSpinBox, self.buttonBox)

    def retranslateUi(self, mclAutoNumberingDialog):
        mclAutoNumberingDialog.setWindowTitle(_translate("mclAutoNumberingDialog", "MCL Auto-numbering Tool", None))
        self.label.setText(_translate("mclAutoNumberingDialog", "Use <ctrl-click> to modify the selection on the map canvas.  Add/remove MCL sections one at a time.", None))
        self.linkedPolysLabel.setText(_translate("mclAutoNumberingDialog", "MCL sections:", None))
        self.label_3.setText(_translate("mclAutoNumberingDialog", "Increment:", None))
        self.label_2.setText(_translate("mclAutoNumberingDialog", "Start value:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mclAutoNumberingDialog = QtGui.QDialog()
    ui = Ui_mclAutoNumberingDialog()
    ui.setupUi(mclAutoNumberingDialog)
    mclAutoNumberingDialog.show()
    sys.exit(app.exec_())

