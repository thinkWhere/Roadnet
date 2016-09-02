# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_filter_street_record_ui.ui'
#
# Created: Fri Dec  4 12:22:46 2015
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

class Ui_filterStreetRecordDialog(object):
    def setupUi(self, filterStreetRecordDialog):
        filterStreetRecordDialog.setObjectName(_fromUtf8("filterStreetRecordDialog"))
        filterStreetRecordDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        filterStreetRecordDialog.resize(813, 487)
        filterStreetRecordDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(filterStreetRecordDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.mapPushButton = QtGui.QPushButton(filterStreetRecordDialog)
        self.mapPushButton.setObjectName(_fromUtf8("mapPushButton"))
        self.gridLayout_9.addWidget(self.mapPushButton, 0, 5, 1, 1)
        self.quickFindPushButton = QtGui.QPushButton(filterStreetRecordDialog)
        self.quickFindPushButton.setObjectName(_fromUtf8("quickFindPushButton"))
        self.gridLayout_9.addWidget(self.quickFindPushButton, 0, 2, 1, 1)
        self.gotoRecordPushButton = QtGui.QPushButton(filterStreetRecordDialog)
        self.gotoRecordPushButton.setObjectName(_fromUtf8("gotoRecordPushButton"))
        self.gridLayout_9.addWidget(self.gotoRecordPushButton, 0, 6, 1, 1)
        self.totalSelectionLabel = QtGui.QLabel(filterStreetRecordDialog)
        self.totalSelectionLabel.setText(_fromUtf8(""))
        self.totalSelectionLabel.setObjectName(_fromUtf8("totalSelectionLabel"))
        self.gridLayout_9.addWidget(self.totalSelectionLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_9, 2, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(filterStreetRecordDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_10 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.townComboBox = QtGui.QComboBox(self.groupBox)
        self.townComboBox.setObjectName(_fromUtf8("townComboBox"))
        self.gridLayout_4.addWidget(self.townComboBox, 1, 0, 1, 1)
        self.townLabel = QtGui.QLabel(self.groupBox)
        self.townLabel.setObjectName(_fromUtf8("townLabel"))
        self.gridLayout_4.addWidget(self.townLabel, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_4, 0, 2, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.localityLabel = QtGui.QLabel(self.groupBox)
        self.localityLabel.setObjectName(_fromUtf8("localityLabel"))
        self.gridLayout_3.addWidget(self.localityLabel, 0, 0, 1, 1)
        self.localityComboBox = QtGui.QComboBox(self.groupBox)
        self.localityComboBox.setObjectName(_fromUtf8("localityComboBox"))
        self.gridLayout_3.addWidget(self.localityComboBox, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.stateLabel = QtGui.QLabel(self.groupBox)
        self.stateLabel.setObjectName(_fromUtf8("stateLabel"))
        self.gridLayout_6.addWidget(self.stateLabel, 0, 0, 1, 1)
        self.stateComboBox = QtGui.QComboBox(self.groupBox)
        self.stateComboBox.setObjectName(_fromUtf8("stateComboBox"))
        self.gridLayout_6.addWidget(self.stateComboBox, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_6, 0, 4, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.descriptionLineEdit = QtGui.QLineEdit(self.groupBox)
        self.descriptionLineEdit.setMinimumSize(QtCore.QSize(140, 0))
        self.descriptionLineEdit.setText(_fromUtf8(""))
        self.descriptionLineEdit.setObjectName(_fromUtf8("descriptionLineEdit"))
        self.gridLayout_2.addWidget(self.descriptionLineEdit, 1, 0, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.groupBox)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout_2.addWidget(self.descriptionLabel, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.recordTypeLabel = QtGui.QLabel(self.groupBox)
        self.recordTypeLabel.setObjectName(_fromUtf8("recordTypeLabel"))
        self.gridLayout_5.addWidget(self.recordTypeLabel, 0, 0, 1, 1)
        self.recordTypeComboBox = QtGui.QComboBox(self.groupBox)
        self.recordTypeComboBox.setObjectName(_fromUtf8("recordTypeComboBox"))
        self.gridLayout_5.addWidget(self.recordTypeComboBox, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_5, 0, 3, 1, 1)
        self.clearPushButton = QtGui.QPushButton(self.groupBox)
        self.clearPushButton.setObjectName(_fromUtf8("clearPushButton"))
        self.gridLayout_10.addWidget(self.clearPushButton, 0, 5, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(filterStreetRecordDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.resultsTableView = QtGui.QTableView(self.groupBox_2)
        self.resultsTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.resultsTableView.setObjectName(_fromUtf8("resultsTableView"))
        self.resultsTableView.verticalHeader().setVisible(False)
        self.gridLayout_8.addWidget(self.resultsTableView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(filterStreetRecordDialog)
        QtCore.QMetaObject.connectSlotsByName(filterStreetRecordDialog)

    def retranslateUi(self, filterStreetRecordDialog):
        filterStreetRecordDialog.setWindowTitle(_translate("filterStreetRecordDialog", "roadNet - Filter Street Records", None))
        self.mapPushButton.setText(_translate("filterStreetRecordDialog", "Map", None))
        self.quickFindPushButton.setText(_translate("filterStreetRecordDialog", "Quick Find", None))
        self.gotoRecordPushButton.setText(_translate("filterStreetRecordDialog", "Goto Record", None))
        self.groupBox.setTitle(_translate("filterStreetRecordDialog", "Selection Criteria", None))
        self.townLabel.setText(_translate("filterStreetRecordDialog", "Town", None))
        self.localityLabel.setText(_translate("filterStreetRecordDialog", "Locality", None))
        self.stateLabel.setText(_translate("filterStreetRecordDialog", "State", None))
        self.descriptionLabel.setText(_translate("filterStreetRecordDialog", "Description", None))
        self.recordTypeLabel.setText(_translate("filterStreetRecordDialog", "Record Type", None))
        self.clearPushButton.setText(_translate("filterStreetRecordDialog", "Clear", None))
        self.groupBox_2.setTitle(_translate("filterStreetRecordDialog", "Selection Results", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    filterStreetRecordDialog = QtGui.QDialog()
    ui = Ui_filterStreetRecordDialog()
    ui.setupUi(filterStreetRecordDialog)
    filterStreetRecordDialog.show()
    sys.exit(app.exec_())

