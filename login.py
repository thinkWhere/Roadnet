# -*- coding: utf-8 -*-
"""
Contains class and functions to create login dialog, query database to check
username, password and role, and change password.
"""

__author__ = 'john.stevenson, alessandro'

import os
from PyQt4.QtGui import QMessageBox
from PyQt4.QtSql import QSqlQuery, QSql, QSqlDatabase
from PyQt4.Qt import Qt
from roadnet_dialog import LoginDlg
import database
import config


class CredentialGetter(object):
    """
    Handles login dialogue, checking password against database, returning
    username and role.
    """
    def __init__(self):
        """
        Initialise the dialogue, connect the buttons and act on inputs.
        """
        self.login_dlg = LoginDlg()
        self.username = None
        self.password = None
        self.login_dlg.ui.usrLineEdit.setText("")
        self.login_dlg.ui.pwdLineEdit.setText("")
        if config.DEBUG_MODE:
            self.login_dlg.ui.usrLineEdit.setText("thinkwhere (DEBUG MODE)")
            self.login_dlg.ui.pwdLineEdit.setText("thinkwhere (DEBUG MODE)")
        self.connect_buttons()
        self.login_dlg.exec_()

    def connect_buttons(self):
        """
        Link buttons to internal functions.
        """
        buttons = self.login_dlg.ui.okCancelButton.buttons()
        buttons[0].clicked.connect(self.store_credentials)
        buttons[1].clicked.connect(self.cancel_login)

    def store_credentials(self):
        """
        Check credentials against database.  Return username and role if
        valid.

        :return UserName, role: Strings with user information
        """
        self.username = str(self.login_dlg.ui.usrLineEdit.text()).rstrip()
        self.password = str(self.login_dlg.ui.pwdLineEdit.text()).rstrip()
        self.close_dialog()

    def cancel_login(self):
        """
        Login cancelled.  Return 'cancelled' as username and role.

        :return UserName, role: Both are 'cancelled'
        """
        self.username = 'cancelled'
        self.password = 'cancelled'
        self.close_dialog()

    def close_dialog(self):
        """
        Closes the dialog.
        """
        self.login_dlg.close()

    def get_credentials(self):
        """
        Returns username, password.
        """
        return self.username, self.password


def login_and_get_role(params):
    """
    Log user in and set role.  Values are stored within the params dictionary.
    """
    # Get username and password from dialog
    params['UserName'], password = input_credentials()
    params['role'] = 'init'
    if params['UserName'] == 'cancelled':
        return
    # Check and assign role
    params['role'] = check_credentials(params, password)
    if params['role'] == 'init':
        login_and_get_role(params)  # Wrong username/password.  Ask again.
    # Editor gets readonly if lock file exists
    if params['role'] == 'editor':
        db_locked = database.check_lock_file(params)
        if db_locked:
            params['role'] = 'readonly'


def input_credentials():
    """
    Creates and calls a CredentialGetter to get credentials from the user.
    Returns username, password.
    """
    getter = CredentialGetter()
    username, password = getter.get_credentials()
    return username, password


def check_credentials(params, password):
    """
    Check credentials against database.  If correct, return 'role', else
    return False.

    :param params: Dictionary of parameters, including UserName and db path.
    :param password: String of password
    :return role / False: role (string), or false if denied.
    """
    # Connect to database
    if config.DEBUG_MODE:
        print('DEBUG_MODE: checking credentials')
    db_path = os.path.join(params['RNDataStorePath'], params['DbName'])
    username = params['UserName']
    db = database.connect_and_open(db_path, 'roadnet_db')

    # Query database
    login_query = QSqlQuery(db)
    login_query.prepare(
        """SELECT usertype FROM tblUsers
           WHERE username =:usr AND userpwd =:pwd""")
    login_query.bindValue(":usr", username, QSql.Out)
    login_query.bindValue(":pwd", password, QSql.Out)
    executed = login_query.exec_()
    if not executed:
        raise Exception('Database query failed.')
    if login_query.first() is True:  # i.e. matching record returned
        # Correct username or password: get role
        role = login_query.value(0)
        if role == 'admin':
            role = 'editor'  # Admin role is no longer used
    else:
        # Set debug mode settings to thinkwhere and editor and remove lock
        if config.DEBUG_MODE:
            params['UserName'] = 'thinkwhere'
            params['role'] = 'editor'
            role = 'editor'
            lock_file_path = os.path.join(params['RNDataStorePath'], 'RNLock')
            if os.path.isfile(lock_file_path):
                os.remove(lock_file_path)
        else:
            # Wrong username or password: warning message
            wrong_login_msg = QMessageBox(QMessageBox.Warning, " ",
                                          "Incorrect username or password",
                                          QMessageBox.Ok, None)
            wrong_login_msg.setWindowFlags(Qt.CustomizeWindowHint |
                                           Qt.WindowTitleHint)
            wrong_login_msg.exec_()
            role = 'init'

    # Close database
    del(login_query)
    connection_name = db.connectionName()
    db.close()
    del(db)
    QSqlDatabase.removeDatabase(connection_name)
    if config.DEBUG_MODE:
        print('DEBUG_MODE: closing QSqlDatabase {}'.format(
            connection_name))
    # Return role or None
    return role
