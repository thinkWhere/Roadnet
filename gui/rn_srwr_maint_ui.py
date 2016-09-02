# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\rn_srwr_maint_ui.ui'
#
# Created: Wed Dec 02 16:13:46 2015
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

class Ui_srwrMaintDialog(object):
    def setupUi(self, srwrMaintDialog):
        srwrMaintDialog.setObjectName(_fromUtf8("srwrMaintDialog"))
        srwrMaintDialog.setWindowModality(QtCore.Qt.NonModal)
        srwrMaintDialog.resize(372, 628)
        self.gridLayout_9 = QtGui.QGridLayout(srwrMaintDialog)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.groupBox = QtGui.QGroupBox(srwrMaintDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.notesLabel = QtGui.QLabel(self.groupBox)
        self.notesLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.notesLabel.setObjectName(_fromUtf8("notesLabel"))
        self.gridLayout_6.addWidget(self.notesLabel, 8, 0, 1, 1)
        self.entryDateLabel = QtGui.QLabel(self.groupBox)
        self.entryDateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.entryDateLabel.setObjectName(_fromUtf8("entryDateLabel"))
        self.gridLayout_6.addWidget(self.entryDateLabel, 7, 0, 1, 1)
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
        self.gridLayout_6.addLayout(self.horizontalLayout_3, 7, 1, 1, 1)
        self.stackedWidget_2 = QtGui.QStackedWidget(self.groupBox)
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.page_9 = QtGui.QWidget()
        self.page_9.setObjectName(_fromUtf8("page_9"))
        self.gridLayout_7 = QtGui.QGridLayout(self.page_9)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.swaLineEdit = QtGui.QLineEdit(self.page_9)
        self.swaLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.swaLineEdit.setReadOnly(True)
        self.swaLineEdit.setObjectName(_fromUtf8("swaLineEdit"))
        self.gridLayout_7.addWidget(self.swaLineEdit, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_9)
        self.page_10 = QtGui.QWidget()
        self.page_10.setObjectName(_fromUtf8("page_10"))
        self.gridLayout_10 = QtGui.QGridLayout(self.page_10)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setMargin(0)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.swaComboBox = QtGui.QComboBox(self.page_10)
        self.swaComboBox.setObjectName(_fromUtf8("swaComboBox"))
        self.gridLayout_10.addWidget(self.swaComboBox, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_10)
        self.gridLayout_6.addWidget(self.stackedWidget_2, 3, 1, 1, 1)
        self.lorNoLabel = QtGui.QLabel(self.groupBox)
        self.lorNoLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lorNoLabel.setObjectName(_fromUtf8("lorNoLabel"))
        self.gridLayout_6.addWidget(self.lorNoLabel, 5, 0, 1, 1)
        self.stackedWidget_3 = QtGui.QStackedWidget(self.groupBox)
        self.stackedWidget_3.setObjectName(_fromUtf8("stackedWidget_3"))
        self.page_11 = QtGui.QWidget()
        self.page_11.setObjectName(_fromUtf8("page_11"))
        self.gridLayout_12 = QtGui.QGridLayout(self.page_11)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setMargin(0)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.roadStatLineEdit = QtGui.QLineEdit(self.page_11)
        self.roadStatLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.roadStatLineEdit.setReadOnly(True)
        self.roadStatLineEdit.setObjectName(_fromUtf8("roadStatLineEdit"))
        self.gridLayout_12.addWidget(self.roadStatLineEdit, 0, 0, 1, 1)
        self.stackedWidget_3.addWidget(self.page_11)
        self.page_12 = QtGui.QWidget()
        self.page_12.setObjectName(_fromUtf8("page_12"))
        self.gridLayout_13 = QtGui.QGridLayout(self.page_12)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setMargin(0)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.roadStatComboBox = QtGui.QComboBox(self.page_12)
        self.roadStatComboBox.setObjectName(_fromUtf8("roadStatComboBox"))
        self.gridLayout_13.addWidget(self.roadStatComboBox, 0, 0, 1, 1)
        self.stackedWidget_3.addWidget(self.page_12)
        self.gridLayout_6.addWidget(self.stackedWidget_3, 4, 1, 1, 1)
        self.roadStatLabel = QtGui.QLabel(self.groupBox)
        self.roadStatLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.roadStatLabel.setObjectName(_fromUtf8("roadStatLabel"))
        self.gridLayout_6.addWidget(self.roadStatLabel, 4, 0, 1, 1)
        self.notesTextEdit = QtGui.QTextEdit(self.groupBox)
        self.notesTextEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.notesTextEdit.setReadOnly(True)
        self.notesTextEdit.setObjectName(_fromUtf8("notesTextEdit"))
        self.gridLayout_6.addWidget(self.notesTextEdit, 8, 1, 1, 1)
        self.adoptLabel = QtGui.QLabel(self.groupBox)
        self.adoptLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.adoptLabel.setObjectName(_fromUtf8("adoptLabel"))
        self.gridLayout_6.addWidget(self.adoptLabel, 6, 0, 1, 1)
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
        self.gridLayout_6.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.wholeRoadCheckBox = QtGui.QCheckBox(self.groupBox)
        self.wholeRoadCheckBox.setObjectName(_fromUtf8("wholeRoadCheckBox"))
        self.gridLayout_6.addWidget(self.wholeRoadCheckBox, 2, 1, 1, 1)
        self.swaLabel = QtGui.QLabel(self.groupBox)
        self.swaLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.swaLabel.setObjectName(_fromUtf8("swaLabel"))
        self.gridLayout_6.addWidget(self.swaLabel, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lorNoLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lorNoLineEdit.sizePolicy().hasHeightForWidth())
        self.lorNoLineEdit.setSizePolicy(sizePolicy)
        self.lorNoLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lorNoLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.lorNoLineEdit.setReadOnly(True)
        self.lorNoLineEdit.setObjectName(_fromUtf8("lorNoLineEdit"))
        self.horizontalLayout_2.addWidget(self.lorNoLineEdit)
        self.routeLabel = QtGui.QLabel(self.groupBox)
        self.routeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.routeLabel.setObjectName(_fromUtf8("routeLabel"))
        self.horizontalLayout_2.addWidget(self.routeLabel)
        self.routeLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.routeLineEdit.sizePolicy().hasHeightForWidth())
        self.routeLineEdit.setSizePolicy(sizePolicy)
        self.routeLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.routeLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.routeLineEdit.setReadOnly(True)
        self.routeLineEdit.setObjectName(_fromUtf8("routeLineEdit"))
        self.horizontalLayout_2.addWidget(self.routeLineEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)
        self.adoptStackedWidget = QtGui.QStackedWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adoptStackedWidget.sizePolicy().hasHeightForWidth())
        self.adoptStackedWidget.setSizePolicy(sizePolicy)
        self.adoptStackedWidget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.adoptStackedWidget.setObjectName(_fromUtf8("adoptStackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.gridLayout_4 = QtGui.QGridLayout(self.page)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.adoptLineEdit = QtGui.QLineEdit(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adoptLineEdit.sizePolicy().hasHeightForWidth())
        self.adoptLineEdit.setSizePolicy(sizePolicy)
        self.adoptLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.adoptLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.adoptLineEdit.setReadOnly(True)
        self.adoptLineEdit.setObjectName(_fromUtf8("adoptLineEdit"))
        self.gridLayout_4.addWidget(self.adoptLineEdit, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 1, 1, 1)
        self.adoptStackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.gridLayout_8 = QtGui.QGridLayout(self.page_2)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setMargin(0)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.adoptDateEdit = QtGui.QDateEdit(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adoptDateEdit.sizePolicy().hasHeightForWidth())
        self.adoptDateEdit.setSizePolicy(sizePolicy)
        self.adoptDateEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.adoptDateEdit.setCalendarPopup(True)
        self.adoptDateEdit.setObjectName(_fromUtf8("adoptDateEdit"))
        self.gridLayout_8.addWidget(self.adoptDateEdit, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem3, 0, 1, 1, 1)
        self.adoptStackedWidget.addWidget(self.page_2)
        self.gridLayout_6.addWidget(self.adoptStackedWidget, 6, 1, 1, 1)
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
        self.maintIdLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maintIdLineEdit.sizePolicy().hasHeightForWidth())
        self.maintIdLineEdit.setSizePolicy(sizePolicy)
        self.maintIdLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.maintIdLineEdit.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.maintIdLineEdit.setReadOnly(True)
        self.maintIdLineEdit.setObjectName(_fromUtf8("maintIdLineEdit"))
        self.gridLayout_2.addWidget(self.maintIdLineEdit, 0, 0, 1, 1)
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
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.maintIdLabel = QtGui.QLabel(self.groupBox)
        self.maintIdLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maintIdLabel.setObjectName(_fromUtf8("maintIdLabel"))
        self.gridLayout_6.addWidget(self.maintIdLabel, 0, 0, 1, 1)
        self.locationLabel = QtGui.QLabel(self.groupBox)
        self.locationLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.locationLabel.setObjectName(_fromUtf8("locationLabel"))
        self.gridLayout_6.addWidget(self.locationLabel, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 1, 1)
        self.rdPolyGroupBox = QtGui.QGroupBox(srwrMaintDialog)
        self.rdPolyGroupBox.setObjectName(_fromUtf8("rdPolyGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.rdPolyGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rdPolyListWidget = QtGui.QListWidget(self.rdPolyGroupBox)
        self.rdPolyListWidget.setStyleSheet(_fromUtf8("border-width:0.5px;\n"
"border-style: solid;\n"
"border-radius: 2px;\n"
"border-color:  rgb(100,100,100);\n"
"background-color: rgb(213, 234, 234);"))
        self.rdPolyListWidget.setObjectName(_fromUtf8("rdPolyListWidget"))
        self.gridLayout.addWidget(self.rdPolyListWidget, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.rdPolyGroupBox, 1, 0, 1, 1)
        self.coordinatesGroupBox = QtGui.QGroupBox(srwrMaintDialog)
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
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.editLinkPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.editLinkPushButton.setEnabled(False)
        self.editLinkPushButton.setObjectName(_fromUtf8("editLinkPushButton"))
        self.horizontalLayout_4.addWidget(self.editLinkPushButton)
        self.editCoordsPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.editCoordsPushButton.setEnabled(False)
        self.editCoordsPushButton.setObjectName(_fromUtf8("editCoordsPushButton"))
        self.horizontalLayout_4.addWidget(self.editCoordsPushButton)
        self.mapPushButton = QtGui.QPushButton(self.coordinatesGroupBox)
        self.mapPushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.mapPushButton.setObjectName(_fromUtf8("mapPushButton"))
        self.horizontalLayout_4.addWidget(self.mapPushButton)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.gridLayout_9.addWidget(self.coordinatesGroupBox, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.closePushButton = QtGui.QPushButton(srwrMaintDialog)
        self.closePushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.horizontalLayout_5.addWidget(self.closePushButton)
        self.gridLayout_9.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)

        self.retranslateUi(srwrMaintDialog)
        self.stackedWidget_2.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.adoptStackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(srwrMaintDialog)

    def retranslateUi(self, srwrMaintDialog):
        srwrMaintDialog.setWindowTitle(_translate("srwrMaintDialog", "RoadNet - Maintenance Record", None))
        self.notesLabel.setText(_translate("srwrMaintDialog", "Notes", None))
        self.entryDateLabel.setText(_translate("srwrMaintDialog", "Entry Date", None))
        self.byLabel.setText(_translate("srwrMaintDialog", "By", None))
        self.lorNoLabel.setText(_translate("srwrMaintDialog", "LOR No", None))
        self.roadStatLabel.setText(_translate("srwrMaintDialog", "Road Status", None))
        self.adoptLabel.setText(_translate("srwrMaintDialog", "Adopted Date", None))
        self.wholeRoadCheckBox.setText(_translate("srwrMaintDialog", "Whole road", None))
        self.swaLabel.setText(_translate("srwrMaintDialog", "SWA Org", None))
        self.routeLabel.setText(_translate("srwrMaintDialog", "Route", None))
        self.refLabel.setText(_translate("srwrMaintDialog", "Ref", None))
        self.maintIdLabel.setText(_translate("srwrMaintDialog", "Maint ID", None))
        self.locationLabel.setText(_translate("srwrMaintDialog", "Location", None))
        self.rdPolyGroupBox.setTitle(_translate("srwrMaintDialog", "Road Polygons", None))
        self.coordinatesGroupBox.setTitle(_translate("srwrMaintDialog", "Coordinates", None))
        self.startYLabel.setText(_translate("srwrMaintDialog", "Start Y", None))
        self.endXLabel.setText(_translate("srwrMaintDialog", "End X", None))
        self.startXLabel.setText(_translate("srwrMaintDialog", "Start X", None))
        self.endYLabel.setText(_translate("srwrMaintDialog", "End Y", None))
        self.editLinkPushButton.setText(_translate("srwrMaintDialog", "Edit Polygon/Maint Link", None))
        self.editCoordsPushButton.setText(_translate("srwrMaintDialog", "Edit Start/End Coordinates", None))
        self.mapPushButton.setText(_translate("srwrMaintDialog", "Map", None))
        self.closePushButton.setText(_translate("srwrMaintDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    srwrMaintDialog = QtGui.QDialog()
    ui = Ui_srwrMaintDialog()
    ui.setupUi(srwrMaintDialog)
    srwrMaintDialog.show()
    sys.exit(app.exec_())

