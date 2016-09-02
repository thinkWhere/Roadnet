# -*- coding: utf-8 -*-
"""Contains classes for connecting to databases and populating models, and
functions for managing database files."""

from datetime import datetime
import os
import re
import shutil
from PyQt4.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlRelation,
    QSqlRelationalTableModel,
    QSqlTableModel)
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox, QFileDialog, QPixmap, QIcon, QDialog
from roadnet_dialog import DbPathDlg
import config
from generic_functions import ipdb_breakpoint

__author__ = 'matthew.walsh'


class DbPathSelect:
    """
    Forms and functions to change the database path in the parameters file.
    """
    def __init__(self, params, params_file):
        # Get parameters including database path
        self.params = params
        self.params_file = params_file
        self.app_root = self.params["RNDataStorePath"]
        self.current_db = self.params["DbName"]
        if self.app_root is None or self.current_db is None:
            self.db_path = ""
        else:
            self.db_path = os.path.join(self.app_root, self.current_db)
        self.new_db_path = None
        # Setup gui dialogues
        self.db_path_dlg = DbPathDlg()
        self.db_path_dlg.ui.newPathLineEdit.setText("")
        self.db_path_dlg.ui.currPathLineEdit.setText(self.db_path)
        self.app_root = os.path.dirname(__file__)
        self.open_image = QPixmap(os.path.join(self.app_root,
                                               "image",
                                               "folder_open_icon.png"))
        self.db_path_dlg.ui.openButton.setIcon(QIcon(self.open_image))
        self.db_path_dlg.ui.openButton.setToolTip("Select File")
        self.choose_file_dialog = QFileDialog()
        self.connect_buttons()

    def connect_buttons(self):
        self.db_path_dlg.ui.currPathLineEdit.setText(self.db_path)
        self.db_path_dlg.ui.cancelButton.clicked.connect(self.close_browser)
        self.db_path_dlg.ui.applyButton.clicked.connect(self.apply_changes)
        self.db_path_dlg.ui.openButton.clicked.connect(self.select_path)

    def close_browser(self):
        if not self.db_path_dlg.result() == QDialog.Accepted:
            self.db_path_dlg.setResult(QDialog.Rejected)
        self.db_path_dlg.close()

    def apply_changes(self):
        if self.check_db_name() is False:
            # Go back to form
            return
        # If correct, update self
        self.new_db_path = str(self.new_db_path)
        self.app_root = os.path.dirname(self.new_db_path)
        self.current_db = os.path.basename(self.new_db_path)
        self.save_changes()
        self.close_browser()
        self.db_path_dlg.setResult(QDialog.Accepted)

    def check_db_name(self):
        # Check name not empty
        if self.db_path_dlg.ui.newPathLineEdit.text() == "":
            restore_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                          "Database location cannot be empty",
                                          QMessageBox.Ok, None, Qt.CustomizeWindowHint)
            restore_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            restore_msg_box.exec_()
            return False
        # Check name not backup
        self.new_db_path = self.db_path_dlg.ui.newPathLineEdit.text()
        new_db_filename = os.path.basename(self.new_db_path)
        name_is_backup = re.search('^\D*_backup(\d|10)(.sqlite)\D*$',
                                   new_db_filename)
        if name_is_backup:
            backup_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                          "You cannot select a backup Database version",
                                          QMessageBox.Ok, None, Qt.CustomizeWindowHint)
            backup_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            backup_msg_box.exec_()
            return False
        else:
            return True

    def save_changes(self):
        self.params["RNDataStorePath"] = self.app_root
        self.params["DbName"] = self.current_db
        self.params_file.update_xml_file(self.params)  # Changes written to file

    def select_path(self):
        path = self.choose_file_dialog.getOpenFileName(
            self.db_path_dlg, "Select Database Directory",
            self.db_path, "(*.sqlite)")
        self.new_db_path = path
        if self.new_db_path != "":
            self.db_path_dlg.ui.newPathLineEdit.setText(self.new_db_path)
            self.db_path_dlg.ui.applyButton.setEnabled(True)


def connect_and_open(db_file_path, connection_name):
    """
    Create a QSqlDatabase connection to the database and open it.

    :param db_file_path: String with database location
    :param connection_name: String with name of connection for Qt use
    :return db: QSqlDatabase object representing open database
    """
    db = QSqlDatabase.addDatabase("QSPATIALITE", connection_name)
    db.setDatabaseName(db_file_path)
    # db.setConnectOptions("QSQLITE_BUSY_TIMEOUT")
    # Also a read only option could use to restrict concurrent access
    if not db.open():
        db_not_open_msg_box = QMessageBox(QMessageBox.Warning, " ", "Database error: {}").format(db.lastError().text(),
                                                                                                 QMessageBox.Ok, None)
        db_not_open_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        db_not_open_msg_box.exec_()
        return
    if config.DEBUG_MODE:
        print('DEBUG_MODE: opening QSqlDatabase {}'.format(
            db.connectionName()))
    return db


def get_model(db):
    """
    Create and populate the model used for all tblSTREET operations.
    
    :param db: Open QSqlDatabase object
    :return model: QSqlRelationalTableModel instance
    """
    # Assign names for easier access to column IDs
    (PK_UID, USRN, VERSION_NO, CURRENCY_FLAG, STREET_REF_TYPE, DESCRIPTION,
     ENTRY_DATE, UPDATE_DATE, START_DATE, AUTHORITY, CLOSURE_DATE, START_XREF,
     START_YREF, END_XREF, END_YREF, TOLERANCE, STREET_SUB_TYPE, STREET_STATE,
     STATE_DATE, STREET_CLASS, LOC_REF, COUNTY_REF, TOWN_REF, UPDATED_BY,
     CLOSED_BY, MIN_X, MIN_Y, MAX_X, MAX_Y, DESCRIPTION_ALT) = range(30)
    # Define model settings
    model = QSqlRelationalTableModel(db=db)
    model.setTable("tblSTREET")
    model.setFilter("currency_flag = 0")  # Only get most recent
    model.setSort(USRN, Qt.SortOrder())  # Order by usrn
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)

    # Set up relational links to other tables
    model.setRelation(STREET_REF_TYPE,
        QSqlRelation("tlkpSTREET_REF_TYPE", "street_ref", "description"))
    model.setRelation(LOC_REF,
        QSqlRelation("tlkpLOCALITY", "loc_ref", "name"))
    model.setRelation(TOWN_REF,
        QSqlRelation("tlkpTOWN", "town_ref", "name"))
    model.setRelation(COUNTY_REF,
        QSqlRelation("tlkpCOUNTY", "county_ref", "name"))
    model.setRelation(STREET_STATE,
        QSqlRelation("tlkpSTREET_STATE", "state_ref", "state_desc"))
    model.setRelation(STREET_CLASS,
        QSqlRelation("tlkpSTREET_CLASS", "class_ref",
                     "street_classification"))
    model.setRelation(AUTHORITY,
        QSqlRelation("tlkpAUTHORITY", "auth_code", "description"))

    # Populate the model with data from the table
    model.select()
    # The following is required if table has more than 256 rows
    while model.canFetchMore():
        model.fetchMore()

    # Populate relational tables (which may have more than 256 rows)
    for relational_column in [STREET_REF_TYPE, LOC_REF, TOWN_REF, COUNTY_REF,
                              STREET_STATE, STREET_CLASS, AUTHORITY]:
        relation_model = model.relationModel(relational_column)
        while relation_model.canFetchMore():
            relation_model.fetchMore()

    return model


def check_file(db_file_path):
    """
    Check database file exists and can be opened.  Passes without exception if
    successful.

    :param file_path: Path of database file.
    """
    if not os.path.isfile(db_file_path):
        raise IOError('File not found: {}'.format(db_file_path))
    if not _run_test_query(db_file_path):
        raise Exception('Database is not valid sqlite file.')


def _run_test_query(db_file_path):
    """
    Runs SQL (sqlite) query to test database file is valid.  Returns
    True for success, False otherwise.

    :param db: Open QSqlDatabase object
    :return bool: True if query runs succesfully.
    """
    if config.DEBUG_MODE:
        print('DEBUG_MODE: testing database connection')
    db = connect_and_open(db_file_path, 'test_connection')
    query = QSqlQuery(db=db)
    result = query.exec_("""SELECT * FROM sqlite_master""")
    del(query)
    connection_name = db.connectionName()
    db.close()
    del(db)
    QSqlDatabase.removeDatabase(connection_name)
    if config.DEBUG_MODE:
        print('DEBUG_MODE: closing QSqlDatabase {}'.format(
            connection_name))
    return result


def open_working_copy(params):
    """
    Make copy of original database file to work on.  For editor role, this is
    database_working.sqlite, for readonly role, this is database_user.sqlite.
    Database is opened and returned as object.  Lock file created for editors.

    :param params: Dictionary of parameters, including role and file paths.
    :return db: Open database object.
    """
    master_db_path = os.path.join(params['RNDataStorePath'], params['DbName'])
    if params['role'] == 'readonly':
        # Read only users work on a database named with their username.
        working_db_name = params['DbName'].replace('.sqlite',
                                                   '_{}.sqlite'.format(
                                                       params['UserName']))
    elif params['role'] == 'editor':
        # Editors work on a database with working in the name.
        working_db_name = params['DbName'].replace('.sqlite',
                                                   '_working.sqlite')
        create_lock_file(params)
    # Store the working database location, copy database, open working.
    working_db_path = os.path.join(params['RNDataStorePath'], working_db_name)
    params['working_db_path'] = working_db_path
    shutil.copy(master_db_path, working_db_path)
    if config.DEBUG_MODE:
        print('DEBUG_MODE: opening main database connection')
    # Open this connection with default name to save passing connection name
    # with every query.
    db = connect_and_open(working_db_path, 'qt_sql_default_connection')
    return db


def update_sqlite_files(params):
    """
    Copy changes from working copy, or discard them.  Rotates backup files
    with up to 10 previous versions.  Removes lock file, if present.

    :param params: Dictionary of parameters, including role and file paths.
    """
    if params['role'] == 'readonly':
        # Read only database is discarded.
        try:
            os.remove(params['working_db_path'])
        except OSError:
            print('WARNING: Read only database not removed.')
        params['working_db_path'] = None
        return
    # Assuming editor role, prompt to save.
    msg_box_save_confirm = QMessageBox(
        "Save Changes",
        "Save changes to roadNet database?",
        QMessageBox.Question, QMessageBox.Yes, QMessageBox.No,
        QMessageBox.NoButton, None)
    msg_box_save_confirm.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    click_btn = msg_box_save_confirm.exec_()
    # Check if save requested
    if click_btn == QMessageBox.Yes:
        # Get list of backup files
        VERSION_LIMIT = 9
        backup_files = [f for f in os.listdir(params['RNDataStorePath'])
                        if f.endswith('.sqlite') and f.find('backup') > 0]
        if len(backup_files) > 0:
            # Increment numbers of backup databases
            backup_files.sort(reverse=True)  # Start at highest number
            for old_name in backup_files:
                basename, version, suffix = re.search(
                    r'(.*backup)(\d)(.*)', old_name).groups()
                if int(version) < VERSION_LIMIT:
                    new_name = '{}{}{}'.format(basename, int(version) + 1,
                                               suffix)
                    shutil.move(os.path.join(params['RNDataStorePath'],
                                             old_name),
                                os.path.join(params['RNDataStorePath'],
                                             new_name))
        # Save current database to first backup and to master database path
        basename = params['DbName'].split('.')[0]
        new_name = '{}_backup1.sqlite'.format(basename)
        shutil.copy(params['working_db_path'],
                    os.path.join(params['RNDataStorePath'], new_name))
        try:
            # Copy and remove, rather than move, as QGIS locks file
            shutil.copy(params['working_db_path'],
                        os.path.join(params['RNDataStorePath'],
                                     params['DbName']))
            os.remove(params['working_db_path'])
        except OSError:
            print('WARNING: database not renamed')
    else:
        try:
            # Don't save, just delete working database
            os.remove(params['working_db_path'])
        except OSError:
            print('WARNING: database not deleted')
    # Remove lock file and reset working database path
    remove_lock_file(params)
    params['working_db_path'] = None


def change_db_path(params, params_file):
    """
    Open a dialogue to allow user to select new path, then run test query on
    file.  In case of success, the xml file is updated and nothing is returned.

    :param params: Dictionary containing parameters, including old path
    :param params_file: ParamsFile object linked to xml file.
    :return bool: True if in db_path_dlg the OK button is pressed, False if cancel
    """
    old_path = os.path.join(params['RNDataStorePath'], params['DbName'])
    db_path_selector = DbPathSelect(params, params_file)
    # executes the window on button clicked
    db_path_selector.db_path_dlg.exec_()
    # cancel clicked
    if db_path_selector.db_path_dlg.result() == QDialog.Rejected:
        return False
    # ok clicked
    if db_path_selector.db_path_dlg.result() == QDialog.Accepted:
        db_path = os.path.join(params['RNDataStorePath'], params['DbName'])
        check_file(db_path)
        if db_path != old_path:
            db_changed_msg_box = QMessageBox(QMessageBox.Information, " ", "Database location successfully updated.\n\n"
                                                                           "Changes will take effect when roadNet next "
                                                                           "starts.", QMessageBox.Ok, None)
            db_changed_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            db_changed_msg_box.exec_()
        return True


def check_lock_file(params):
    """
    Checks for presence of RNLock in the data directory.

    :param params: Dictionary of parameters including data directory path
    :return bool: True/False
    """
    lock_file_path = os.path.join(params['RNDataStorePath'], 'RNLock')
    if os.path.isfile(lock_file_path):
        # Database is locked by another user
        with open(lock_file_path, 'r') as infile:
            lock_username = infile.readline().split(":")[1].strip()
        message = ('Database locked for editing by {} with lock file at:\n\n'
                   '{}\n\n'
                   'Opening as read only.'.format(lock_username,
                                                 lock_file_path))
        # Check for stray lock file.
        working_files = [f for f in os.listdir(params['RNDataStorePath'])
                         if f.endswith('_working.sqlite')]
        if len(working_files) == 0:
            message = (message + '\n\nNo database currently being edited. '
                                 'Check for stray lock file.')
        lock_file_msg_box = QMessageBox(QMessageBox.Information, " ",
                                        message, QMessageBox.Ok, None)
        lock_file_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        lock_file_msg_box.exec_()
        return True
    else:
        return False


def create_lock_file(params):
    """
    Create lock file RNLock in the data directory with the name of the locking
    user.
    """
    lock_file_path = os.path.join(params['RNDataStorePath'], 'RNLock')
    with open(lock_file_path, 'w') as f:
        f.write('Database locked by: {}\n'.format(params['UserName']))
        f.write('Database locked at: {}'.format(datetime.now().strftime(
                '%Y-%m-%d %H:%M')))


def db_restore_point(params):
    """
    Saves a copy of the working database as <database>_restore.sqlite.
    :return: void
    """
    working_db_path = params['working_db_path']
    restore_db_path = working_db_path.replace('working', 'restore')
    try:
        shutil.copy(working_db_path, restore_db_path)
        restore_msg_box = QMessageBox(QMessageBox.Information, "Create Restore Point",
                                      "Database copied to {}.".format(restore_db_path),
                                      QMessageBox.Ok, None, Qt.CustomizeWindowHint)
        restore_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        restore_msg_box.exec_()
    except (OSError, IOError):
        db_failed_msg_box = QMessageBox(QMessageBox.Warning, "Create Restore Point",
                                        "Database copy failed.", QMessageBox.Ok, None)
        db_failed_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        db_failed_msg_box.exec_()


def remove_lock_file(params):
    """
    Remove lock file RNLock from the data directory.
    """
    lock_file_path = os.path.join(params['RNDataStorePath'], 'RNLock')
    os.remove(lock_file_path)


def update_geometry_statistics(db):
    """
    Update internal tables with geometry statistics
    :param db: Database object
    """
    sql = """
        UPDATE geometry_columns_statistics SET last_verified = 0;"""
    run_sql(sql, db)

    sql = """
        SELECT UpdateLayerStatistics();"""
    run_sql(sql, db)


def run_sql(sql, db):
    """
    Run SQL query on the database.
    :param sql: String of sql
    :param db: Open QSql database
    return: QSqlQuery object to extract results
    """
    if config.DEBUG_MODE:
        print(sql)
    active_query = QSqlQuery(sql, db)
    if active_query.isActive() is False:
        raise StandardError('Database query problem: {}'.format(
            active_query.lastError().text()))
    return active_query

def get_from_gaz_metadata(db, column):
    """
    Get the gazetteer metadata from the database
    (e.g. org name, custodian code)
    :rtype: str
    :return: metadata item
    """
    sql = "SELECT {} FROM tblGazMetadata".format(column)
    query = QSqlQuery(sql, db)
    query.first()
    gaz_metadata = query.value(query.record().indexOf(column))
    return gaz_metadata
