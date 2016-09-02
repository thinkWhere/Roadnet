# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/rn_about_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName(_fromUtf8("aboutDialog"))
        aboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        aboutDialog.setEnabled(True)
        aboutDialog.resize(438, 366)
        aboutDialog.setMinimumSize(QtCore.QSize(438, 366))
        aboutDialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(aboutDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.imageLabel = QtGui.QLabel(aboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setMinimumSize(QtCore.QSize(126, 105))
        self.imageLabel.setMaximumSize(QtCore.QSize(126, 105))
        self.imageLabel.setSizeIncrement(QtCore.QSize(0, 0))
        self.imageLabel.setText(_fromUtf8(""))
        self.imageLabel.setPixmap(QtGui.QPixmap(_fromUtf8("../image/rn_logo_v2.png")))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.horizontalLayout.addWidget(self.imageLabel)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(aboutDialog)
        self.label.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.versionLabel = QtGui.QLabel(aboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLabel.sizePolicy().hasHeightForWidth())
        self.versionLabel.setSizePolicy(sizePolicy)
        self.versionLabel.setMaximumSize(QtCore.QSize(290, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.versionLabel.setFont(font)
        self.versionLabel.setObjectName(_fromUtf8("versionLabel"))
        self.verticalLayout.addWidget(self.versionLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.descLabel = QtGui.QLabel(aboutDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        font.setPointSize(9)
        self.descLabel.setFont(font)
        self.descLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.descLabel.setWordWrap(True)
        self.descLabel.setObjectName(_fromUtf8("descLabel"))
        self.verticalLayout_2.addWidget(self.descLabel)
        self.gnuLicenseLabel = QtGui.QLabel(aboutDialog)
        self.gnuLicenseLabel.setWordWrap(True)
        self.gnuLicenseLabel.setObjectName(_fromUtf8("gnuLicenseLabel"))
        self.verticalLayout_2.addWidget(self.gnuLicenseLabel)
        self.thinkWhereLinkLabel = QtGui.QLabel(aboutDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        font.setPointSize(9)
        self.thinkWhereLinkLabel.setFont(font)
        self.thinkWhereLinkLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.thinkWhereLinkLabel.setObjectName(_fromUtf8("thinkWhereLinkLabel"))
        self.verticalLayout_2.addWidget(self.thinkWhereLinkLabel)
        self.line = QtGui.QFrame(aboutDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.copyrightLabel = QtGui.QLabel(aboutDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.copyrightLabel.setFont(font)
        self.copyrightLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.copyrightLabel.setWordWrap(True)
        self.copyrightLabel.setObjectName(_fromUtf8("copyrightLabel"))
        self.horizontalLayout_2.addWidget(self.copyrightLabel)
        self.okButton = QtGui.QPushButton(aboutDialog)
        self.okButton.setMinimumSize(QtCore.QSize(81, 23))
        self.okButton.setMaximumSize(QtCore.QSize(81, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout_2.addWidget(self.okButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About roadNet", None))
        self.label.setText(_translate("aboutDialog", "roadNet", None))
        self.versionLabel.setText(_translate("aboutDialog", "Version:", None))
        self.descLabel.setText(_translate("aboutDialog", "roadNet is an application for managing a local street gazetteer (LSG) complying with BS7666 standards, using the conventions set out for the Scottish Gazetteer.  It also enables the creation and management of associated data (ASD) which is required by the Scottish Road Works Register. The application manages all information required by these standards, as well as additional data fields that are of use internally by local authorities.  The RAMP functions manage a register of road assets.", None))
        self.gnuLicenseLabel.setText(_translate("aboutDialog", "<html><head/><body><p align=\"center\">roadNet is licenced under the <a href=\"http://www.gnu.org/licenses\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU General Public Licence Version 2</span></a>.</p></body></html>", None))
        self.thinkWhereLinkLabel.setText(_translate("aboutDialog", "<html><head/><body><p>Visit <a href=\"http://www.thinkwhere.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.thinkwhere.com</span></a> for more information.</p></body></html>", None))
        self.copyrightLabel.setText(_translate("aboutDialog", "Copyright thinkWhere Ltd 2016", None))
        self.okButton.setText(_translate("aboutDialog", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    aboutDialog = QtGui.QDialog()
    ui = Ui_aboutDialog()
    ui.setupUi(aboutDialog)
    aboutDialog.show()
    sys.exit(app.exec_())

