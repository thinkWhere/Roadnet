# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_srwr_reins_cat_ui.ui'
#
# Created: Wed Dec 02 16:14:11 2015
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

class Ui_srwrReinsCatDialog(object):
    def setupUi(self, srwrReinsCatDialog):
        srwrReinsCatDialog.setObjectName(_fromUtf8("srwrReinsCatDialog"))
        srwrReinsCatDialog.setWindowModality(QtCore.Qt.NonModal)
        srwrReinsCatDialog.resize(372, 438)
        self.gridLayout = QtGui.QGridLayout(srwrReinsCatDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(srwrReinsCatDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.locationLabel = QtGui.QLabel(self.groupBox)
        self.locationLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.locationLabel.setObjectName(_fromUtf8("locationLabel"))
        self.gridLayout_9.addWidget(self.locationLabel, 1, 0, 1, 1)
        self.maintIdLabel = QtGui.QLabel(self.groupBox)
        self.maintIdLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maintIdLabel.setObjectName(_fromUtf8("maintIdLabel"))
        self.gridLayout_9.addWidget(self.maintIdLabel, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.locationTextEdit = QtGui.QTextEdit(self.groupBox)
        self.locationTextEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.locationTextEdit.setReadOnly(True)
        self.locationTextEdit.setObjectName(_fromUtf8("locationTextEdit"))
        self.horizontalLayout.addWidget(self.locationTextEdit)
        self.gridLayout_9.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.notesLabel = QtGui.QLabel(self.groupBox)
        self.notesLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.notesLabel.setObjectName(_fromUtf8("notesLabel"))
        self.gridLayout_9.addWidget(self.notesLabel, 5, 0, 1, 1)
        self.wholeRoadCheckBox = QtGui.QCheckBox(self.groupBox)
        self.wholeRoadCheckBox.setObjectName(_fromUtf8("wholeRoadCheckBox"))
        self.gridLayout_9.addWidget(self.wholeRoadCheckBox, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.entryDateLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entryDateLineEdit.sizePolicy().hasHeightForWidth())
        self.entryDateLineEdit.setSizePolicy(sizePolicy)
        self.entryDateLineEdit.setMinimumSize(QtCore.QSize(40, 0))
        self.entryDateLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.entryDateLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.entryDateLineEdit.setReadOnly(True)
        self.entryDateLineEdit.setObjectName(_fromUtf8("entryDateLineEdit"))
        self.horizontalLayout_3.addWidget(self.entryDateLineEdit)
        self.byLabel = QtGui.QLabel(self.groupBox)
        self.byLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.byLabel.setObjectName(_fromUtf8("byLabel"))
        self.horizontalLayout_3.addWidget(self.byLabel)
        self.byLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.byLineEdit.sizePolicy().hasHeightForWidth())
        self.byLineEdit.setSizePolicy(sizePolicy)
        self.byLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.byLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.byLineEdit.setReadOnly(True)
        self.byLineEdit.setObjectName(_fromUtf8("byLineEdit"))
        self.horizontalLayout_3.addWidget(self.byLineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout_9.addLayout(self.horizontalLayout_3, 4, 1, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.versionLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLineEdit.sizePolicy().hasHeightForWidth())
        self.versionLineEdit.setSizePolicy(sizePolicy)
        self.versionLineEdit.setMaximumSize(QtCore.QSize(30, 16777215))
        self.versionLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.versionLineEdit.setText(_fromUtf8(""))
        self.versionLineEdit.setReadOnly(True)
        self.versionLineEdit.setObjectName(_fromUtf8("versionLineEdit"))
        self.gridLayout_2.addWidget(self.versionLineEdit, 0, 1, 1, 1)
        self.reinsCatIdLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reinsCatIdLineEdit.sizePolicy().hasHeightForWidth())
        self.reinsCatIdLineEdit.setSizePolicy(sizePolicy)
        self.reinsCatIdLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.reinsCatIdLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.reinsCatIdLineEdit.setReadOnly(True)
        self.reinsCatIdLineEdit.setObjectName(_fromUtf8("reinsCatIdLineEdit"))
        self.gridLayout_2.addWidget(self.reinsCatIdLineEdit, 0, 0, 1, 1)
        self.refLabel = QtGui.QLabel(self.groupBox)
        self.refLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.refLabel.setObjectName(_fromUtf8("refLabel"))
        self.gridLayout_2.addWidget(self.refLabel, 0, 2, 1, 1)
        self.refLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refLineEdit.sizePolicy().hasHeightForWidth())
        self.refLineEdit.setSizePolicy(sizePolicy)
        self.refLineEdit.setMaximumSize(QtCore.QSize(30, 16777215))
        self.refLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.refLineEdit.setReadOnly(True)
        self.refLineEdit.setObjectName(_fromUtf8("refLineEdit"))
        self.gridLayout_2.addWidget(self.refLineEdit, 0, 3, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.swaLabel = QtGui.QLabel(self.groupBox)
        self.swaLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.swaLabel.setObjectName(_fromUtf8("swaLabel"))
        self.gridLayout_9.addWidget(self.swaLabel, 3, 0, 1, 1)
        self.entryDateLabel = QtGui.QLabel(self.groupBox)
        self.entryDateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.entryDateLabel.setObjectName(_fromUtf8("entryDateLabel"))
        self.gridLayout_9.addWidget(self.entryDateLabel, 4, 0, 1, 1)
        self.stackedWidget_2 = QtGui.QStackedWidget(self.groupBox)
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.page_9 = QtGui.QWidget()
        self.page_9.setObjectName(_fromUtf8("page_9"))
        self.gridLayout_7 = QtGui.QGridLayout(self.page_9)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.categoryLineEdit = QtGui.QLineEdit(self.page_9)
        self.categoryLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.categoryLineEdit.setReadOnly(True)
        self.categoryLineEdit.setObjectName(_fromUtf8("categoryLineEdit"))
        self.gridLayout_7.addWidget(self.categoryLineEdit, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_9)
        self.page_10 = QtGui.QWidget()
        self.page_10.setObjectName(_fromUtf8("page_10"))
        self.gridLayout_10 = QtGui.QGridLayout(self.page_10)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setMargin(0)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.categoryComboBox = QtGui.QComboBox(self.page_10)
        self.categoryComboBox.setObjectName(_fromUtf8("categoryComboBox"))
        self.gridLayout_10.addWidget(self.categoryComboBox, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_10)
        self.gridLayout_9.addWidget(self.stackedWidget_2, 3, 1, 1, 1)
        self.notesTextEdit = QtGui.QTextEdit(self.groupBox)
        self.notesTextEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.notesTextEdit.setReadOnly(True)
        self.notesTextEdit.setObjectName(_fromUtf8("notesTextEdit"))
        self.gridLayout_9.addWidget(self.notesTextEdit, 5, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.coordinatesGroupBox = QtGui.QGroupBox(srwrReinsCatDialog)
        self.coordinatesGroupBox.setObjectName(_fromUtf8("coordinatesGroupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.coordinatesGroupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_15 = QtGui.QGridLayout()
        self.gridLayout_15.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_15.setVerticalSpacing(6)
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.endXLineEdit = QtGui.QLineEdit(self.coordinatesGroupBox)
        self.endXLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.endXLineEdit.setReadOnly(True)
        self.endXLineEdit.setObjectName(_fromUtf8("endXLineEdit"))
        self.gridLayout_15.addWidget(self.endXLineEdit, 1, 1, 1, 1)
        self.startYLabel = QtGui.QLabel(self.coordinatesGroupBox)
        self.startYLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.startYLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.startYLabel.setObjectName(_fromUtf8("startYLabel"))
        self.gridLayout_15.addWidget(self.startYLabel, 0, 2, 1, 1)
        self.endXLabel = QtGui.QLabel(self.coordinatesGroupBox)
        self.endXLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.endXLabel.setObjectName(_fromUtf8("endXLabel"))
        self.gridLayout_15.addWidget(self.endXLabel, 1, 0, 1, 1)
        self.startYLineEdit = QtGui.QLineEdit(self.coordinatesGroupBox)
        self.startYLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.startYLineEdit.setReadOnly(True)
        self.startYLineEdit.setObjectName(_fromUtf8("startYLineEdit"))
        self.gridLayout_15.addWidget(self.startYLineEdit, 0, 3, 1, 1)
        self.startXLabel = QtGui.QLabel(self.coordinatesGroupBox)
        self.startXLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.startXLabel.setObjectName(_fromUtf8("startXLabel"))
        self.gridLayout_15.addWidget(self.startXLabel, 0, 0, 1, 1)
        self.startXLineEdit = QtGui.QLineEdit(self.coordinatesGroupBox)
        self.startXLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.startXLineEdit.setReadOnly(True)
        self.startXLineEdit.setObjectName(_fromUtf8("startXLineEdit"))
        self.gridLayout_15.addWidget(self.startXLineEdit, 0, 1, 1, 1)
        self.endYLabel = QtGui.QLabel(self.coordinatesGroupBox)
        self.endYLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.endYLabel.setAutoFillBackground(False)
        self.endYLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.endYLabel.setObjectName(_fromUtf8("endYLabel"))
        self.gridLayout_15.addWidget(self.endYLabel, 1, 2, 1, 1)
        self.endYLineEdit = QtGui.QLineEdit(self.coordinatesGroupBox)
        self.endYLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.endYLineEdit.setReadOnly(True)
        self.endYLineEdit.setObjectName(_fromUtf8("endYLineEdit"))
        self.gridLayout_15.addWidget(self.endYLineEdit, 1, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_15, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.editLinkPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.editLinkPushButton.setEnabled(False)
        self.editLinkPushButton.setFlat(False)
        self.editLinkPushButton.setObjectName(_fromUtf8("editLinkPushButton"))
        self.horizontalLayout_4.addWidget(self.editLinkPushButton)
        self.editCoordsPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.editCoordsPushButton.setEnabled(False)
        self.editCoordsPushButton.setObjectName(_fromUtf8("editCoordsPushButton"))
        self.horizontalLayout_4.addWidget(self.editCoordsPushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.mapPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.mapPushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.mapPushButton.setObjectName(_fromUtf8("mapPushButton"))
        self.horizontalLayout_4.addWidget(self.mapPushButton)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.coordinatesGroupBox, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.closePushButton = QtGui.QPushButton(srwrReinsCatDialog)
        self.closePushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.horizontalLayout_5.addWidget(self.closePushButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.retranslateUi(srwrReinsCatDialog)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(srwrReinsCatDialog)

    def retranslateUi(self, srwrReinsCatDialog):
        srwrReinsCatDialog.setWindowTitle(_translate("srwrReinsCatDialog", "Reinstatement Category Record", None))
        self.locationLabel.setText(_translate("srwrReinsCatDialog", "Location", None))
        self.maintIdLabel.setText(_translate("srwrReinsCatDialog", "Reins ID", None))
        self.notesLabel.setText(_translate("srwrReinsCatDialog", "Notes", None))
        self.wholeRoadCheckBox.setText(_translate("srwrReinsCatDialog", "Whole road", None))
        self.byLabel.setText(_translate("srwrReinsCatDialog", "By", None))
        self.refLabel.setText(_translate("srwrReinsCatDialog", "Ref", None))
        self.swaLabel.setText(_translate("srwrReinsCatDialog", "Category", None))
        self.entryDateLabel.setText(_translate("srwrReinsCatDialog", "Entry Date", None))
        self.coordinatesGroupBox.setTitle(_translate("srwrReinsCatDialog", "Coordinates", None))
        self.startYLabel.setText(_translate("srwrReinsCatDialog", "Start Y", None))
        self.endXLabel.setText(_translate("srwrReinsCatDialog", "End X", None))
        self.startXLabel.setText(_translate("srwrReinsCatDialog", "Start X", None))
        self.endYLabel.setText(_translate("srwrReinsCatDialog", "End Y", None))
        self.editLinkPushButton.setText(_translate("srwrReinsCatDialog", "Edit Polygon/Maint Link", None))
        self.editCoordsPushButton.setText(_translate("srwrReinsCatDialog", "Edit Start/End Coordinates", None))
        self.mapPushButton.setText(_translate("srwrReinsCatDialog", "Map", None))
        self.closePushButton.setText(_translate("srwrReinsCatDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    srwrReinsCatDialog = QtGui.QDialog()
    ui = Ui_srwrReinsCatDialog()
    ui.setupUi(srwrReinsCatDialog)
    srwrReinsCatDialog.show()
    sys.exit(app.exec_())

