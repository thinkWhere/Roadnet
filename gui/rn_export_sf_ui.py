# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_export_sf_ui.ui'
#
# Created: Tue Jul 28 14:28:49 2015
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

class Ui_selectedFeatures(object):
    def setupUi(self, selectedFeatures):
        selectedFeatures.setObjectName(_fromUtf8("selectedFeatures"))
        selectedFeatures.resize(351, 96)
        self.label_2 = QtGui.QLabel(selectedFeatures)
        self.label_2.setGeometry(QtCore.QRect(10, 13, 328, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(selectedFeatures)
        self.line.setGeometry(QtCore.QRect(10, 51, 328, 3))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.layoutWidget = QtGui.QWidget(selectedFeatures)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 328, 32))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okPushButton = QtGui.QPushButton(self.layoutWidget)
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))
        self.horizontalLayout.addWidget(self.okPushButton)
        self.noPushButton = QtGui.QPushButton(self.layoutWidget)
        self.noPushButton.setObjectName(_fromUtf8("noPushButton"))
        self.horizontalLayout.addWidget(self.noPushButton)
        self.cancelPushButton = QtGui.QPushButton(self.layoutWidget)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)

        self.retranslateUi(selectedFeatures)
        QtCore.QMetaObject.connectSlotsByName(selectedFeatures)

    def retranslateUi(self, selectedFeatures):
        selectedFeatures.setWindowTitle(_translate("selectedFeatures", "Selected Features?", None))
        self.label_2.setText(_translate("selectedFeatures", "Do you want to export selected features? ", None))
        self.okPushButton.setText(_translate("selectedFeatures", "Yes", None))
        self.noPushButton.setText(_translate("selectedFeatures", "No", None))
        self.cancelPushButton.setText(_translate("selectedFeatures", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    selectedFeatures = QtGui.QDialog()
    ui = Ui_selectedFeatures()
    ui.setupUi(selectedFeatures)
    selectedFeatures.show()
    sys.exit(app.exec_())

