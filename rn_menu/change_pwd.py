# -*- coding: utf-8 -*-
__author__ = 'Alessandro'

from PyQt4.QtSql import QSqlQuery, QSql
from PyQt4.QtGui import QMessageBox
from  PyQt4.Qt import Qt


class ChangePwd:
    def __init__(self, change_pwd_dia, iface, db, plugin_dir, params):
        self.change_pwd_dia = change_pwd_dia
        self.iface = iface
        self.db = db
        self.params = params
        self.model_navigation()
        self.user = self.params['UserName']
        self.pwd_query = None
        self.old_input_pwd = None
        self.current_pwd = None
        self.new_pwd = None
        self.new_conf_pwd = None
        self.plugin_dir = plugin_dir
        self.wrong_pwd_msg_box = None

    def model_navigation(self):
        buttons = self.change_pwd_dia.ui.okCancelButton.buttons()
        buttons[0].clicked.connect(self.change_pwd_handler)
        buttons[1].clicked.connect(self.close_browser)

    def change_pwd_handler(self):
        """
        this function handles all cases of user password inputs
        :return:
        """
        self.old_input_pwd = self.change_pwd_dia.ui.oldPwdLineEdit.text()
        self.new_pwd = self.change_pwd_dia.ui.pwdLineEdit.text()
        self.new_conf_pwd = self.change_pwd_dia.ui.confirmLineEdit.text()
        if self.old_input_pwd == "":
            return
        else:
            if self.compare_pwd() is False:
                self.wrong_pwd_msg_box = QMessageBox(QMessageBox.Warning,
                                                     " ",
                                                     "The input current password is not correct",
                                                     QMessageBox.Ok,
                                                     None)
                self.wrong_pwd_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                self.wrong_pwd_msg_box.exec_()
                return
            if self.new_pwd == "" or self.new_conf_pwd == "":
                self.wrong_pwd_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                                     "You must insert the new password in both fields",
                                                     QMessageBox.Ok,
                                                     None)
                self.wrong_pwd_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                self.wrong_pwd_msg_box.exec_()
                return
            if not self.new_pwd == self.new_conf_pwd:
                self.wrong_pwd_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                                     "The passwords inserted do not match", 
                                                     QMessageBox.Ok,
                                                     None)
                self.wrong_pwd_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                self.wrong_pwd_msg_box.exec_()
                return
            if len(self.new_pwd) > 15 or len(self.new_conf_pwd) > 15:
                self.wrong_pwd_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                                     "The password cannot be longer than 15 characters",
                                                     QMessageBox.Ok,
                                                     None)
                self.wrong_pwd_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                self.wrong_pwd_msg_box.exec_()
                return
        pwd_changed = self.change_pwd(self.db)
        if pwd_changed:
            pwd_change_info = QMessageBox(QMessageBox.Information, " ",
                    "Password updated in database.  Save changes at the end of"
                    " session to new password next login.",
                    QMessageBox.Ok, None)
            pwd_change_info.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            pwd_change_info.exec_()
            self.old_input_pwd = self.change_pwd_dia.ui.oldPwdLineEdit.setText("")
            self.new_pwd = self.change_pwd_dia.ui.pwdLineEdit.setText("")
            self.new_conf_pwd = self.change_pwd_dia.ui.confirmLineEdit.setText("")
            self.change_pwd_dia.close()
        else:
            no_db_access_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                               "Cannot access Database",
                                               QMessageBox.Ok,
                                               None)
            no_db_access_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_db_access_msg_box.exec_()
        return

    def change_pwd(self, db):
        """
        function that changes the password to the db, i needs the
        current user ID
        :return:
        """
        self.pwd_query = QSqlQuery(db)
        self.pwd_query.prepare("UPDATE tblUsers SET userpwd =:pwd WHERE username =:usr")
        self.pwd_query.bindValue(":pwd", self.new_pwd)
        self.pwd_query.bindValue(":usr", self.user)
        executed = self.pwd_query.exec_()
        if not executed:
            return executed
        else:
            return executed

    def close_browser(self):
        # close the browser
        self.change_pwd_dia.close()
        return

    def compare_pwd(self):
        """
        function that compares the current password to the one the user is trying to change
        :return: bool True if password matches False if not
        """
        pwd_query = QSqlQuery()
        pwd_str = "SELECT userpwd FROM tblUsers WHERE username =:user"
        pwd_query.prepare(pwd_str)
        pwd_query.bindValue(":user", self.user, QSql.Out)
        pwd_query.exec_()
        pwd_query.first()
        old_pwd = pwd_query.value(0)
        if self.old_input_pwd != old_pwd:
            return False
        else:
            return True



