# -*- coding: utf-8 -*-
from datetime import datetime
from PyQt4.QtCore import QPyNullVariant
from PyQt4.QtSql import QSqlQuery

__author__ = 'Alessandro Cristofori'


class Metadata:
    """
    Display and edit the metadata
    """
    def __init__(self, iface, db, meta_dia, params):
        """
        :param iface: QgsInterface
        :param db: database connection
        :param meta_dia: metadata dialog
        :param params: params dictionary
        :return:
        """
        self.iface = iface
        self.db = db
        self.meta_dia = meta_dia
        self.get_meta_info = "SELECT name, scope, territory, owner, custodian, coord_sys, coord_units, " \
                             "metadata_date, class_scheme, code_scheme, custodian_code, " \
                             "gaz_language, charset from tblGazMetadata "
        self.get_last_street = "SELECT max(update_date) AS LastStreet FROM tblStreet"
        self.get_last_esu = "SELECT Max(closure_date) AS LastClose, Max(entry_date) AS lastEntry FROM tblESU"
        self.get_last_date = "Select MAX(Entry_Date) AS LastEntry, MAX(Closure_Date) AS LastClose FROM {tbl_name}"
        self.set_update_values = "UPDATE tblGazMetadata SET "
        self.set_data()
        self.meta_values = []
        self.connect_buttons()
        if params['role'] == 'readonly':
            self.read_only_mode()

    def read_only_mode(self):
        """
        Switch the dialog to read-only mode by changing line edits and buttons.
        """

        # Change the buttons
        cancel_button, apply_button = self.meta_dia.ui.buttonBox.buttons()
        self.meta_dia.ui.buttonBox.removeButton(apply_button)
        cancel_button.setText('OK')

        # Make fields read only, getting style from 'Name' example
        read_only_style = self.meta_dia.ui.nameLineEdit.styleSheet()
        for field in (self.meta_dia.ui.scopeLineEdit,
                      self.meta_dia.ui.terrLineEdit,
                      self.meta_dia.ui.gazLineEdit,
                      self.meta_dia.ui.mailLineEdit):
            field.setStyleSheet(read_only_style)
            field.setReadOnly(True)

        # Make check boxes uncheckable
        self.meta_dia.ui.langCheckBox.setCheckable(False)
        self.meta_dia.ui.charCheckBox.setCheckable(False)

    def connect_buttons(self):
        """
        events handler for OK and Cancel buttons
        :rtype : object
        """
        cancel_button, apply_button = self.meta_dia.ui.buttonBox.buttons()
        apply_button.clicked.connect(self.get_data)
        cancel_button.clicked.connect(self.close_browser)

    def set_data(self):
        # set text boxes to db values
        self.meta_dia.ui.lsgLineEdit.setText(self.lsg_last_date())
        self.meta_dia.ui.asdLineEdit.setText(self.asd_last_date())
        self.meta_values = self.set_values()
        self.meta_dia.ui.nameLineEdit.setText(self.meta_values[0])
        self.meta_dia.ui.scopeLineEdit.setText(self.meta_values[1])
        self.meta_dia.ui.terrLineEdit.setText(self.meta_values[2])
        self.meta_dia.ui.gazLineEdit.setText(self.meta_values[3])
        self.meta_dia.ui.mailLineEdit.setText(self.meta_values[4])
        self.meta_dia.ui.coordLineEdit.setText(self.meta_values[5])
        self.meta_dia.ui.unitsLineEdit.setText(self.meta_values[6])
        self.meta_dia.ui.metaLineEdit.setText(self.meta_values[7])
        self.meta_dia.ui.classLineEdit.setText(self.meta_values[8])
        self.meta_dia.ui.stateLineEdit.setText(self.meta_values[9])
        self.meta_dia.ui.custLineEdit.setText(self.meta_values[10])
        self.meta_dia.ui.langCheckBox.setChecked(self.populate_check_boxes(self.meta_values[11]))
        self.meta_dia.ui.charCheckBox.setChecked(self.populate_check_boxes(self.meta_values[12]))

    def close_browser(self):
        # close the dialog window
        self.meta_dia.close()

    def lsg_last_date(self):
        """
        get the last update date from db to show in LSG label
        :return: string
        """
        qry_lsg = QSqlQuery(self.get_last_street, self.db)  # THIS
        while qry_lsg.next():
            try:
                date_lsg_obj = datetime.strptime(str(qry_lsg.value(0)), "%Y%m%d")
            except ValueError:
                date_lsg_obj = '000000'

        qry_esu = QSqlQuery(self.get_last_esu, self.db)
        while qry_esu.next():
            try:
                date_esu_closure_obj = datetime.strptime(str(qry_esu.value(0)), "%Y%m%d")
            except ValueError:
                date_esu_closure_obj = '000000'
            try:
                date_esu_entry_obj = datetime.strptime(str(qry_esu.value(1)), "%Y%m%d")
            except ValueError:
                date_esu_entry_obj = '00000'

        last_lsg_change = max(date_lsg_obj, date_esu_closure_obj, date_esu_entry_obj).date()
        date_clean = str(last_lsg_change.strftime("%d/%m/%Y"))

        return date_clean

    def asd_last_date(self):
        """
        get the last update date (e.g. latest of entry or updates date) from db to show in ASD label
        :return: string
        """
        last_update = 0
        tbl_names = ["tblMAINT", "tblREINS_CAT", "tblSPEC_DES"]

        for tbl_name in tbl_names:
            query = QSqlQuery(self.db)
            query.exec_(self.get_last_date.format(tbl_name=tbl_name))
            query.next()
            rec = query.record()
            last_entry, last_close = (rec.value('LastEntry'), rec.value('LastClose'))

            if not isinstance(last_entry, QPyNullVariant):
                if int(last_entry) > last_update:
                    last_update = last_entry

            if not isinstance(last_close, QPyNullVariant):
                if int(last_close) > last_update:
                    last_update = last_close

        last_update_date = datetime.strptime(str(last_update), "%Y%m%d")
        asd_date_clean = last_update_date.strftime("%d/%m/%Y")

        return asd_date_clean

    def set_values(self):
        """
        set all required values to show in the form widgets from db
        :return: string[]
        """
        i = 0
        meta_values = []
        qry_md_vals = QSqlQuery(self.db)
        qry_md_vals.exec_(self.get_meta_info)
        rec = qry_md_vals.record()
        field_count = rec.count()
        meta_vals = [rec.indexOf("name"), rec.indexOf("scope"), rec.indexOf("territory"), rec.indexOf("owner"),
                     rec.indexOf("custodian"), rec.indexOf("coord_sys"), rec.indexOf("coord_units"),
                     rec.indexOf("metadata_date"), rec.indexOf("class_scheme"), rec.indexOf("code_scheme"),
                     rec.indexOf("custodian_code"), rec.indexOf("gaz_language"), rec.indexOf("charset")]
        while qry_md_vals.next():
            while i <= field_count - 1:
                if i == 7:  # handles date formatting
                    date_obj = datetime.strptime(str(qry_md_vals.value(meta_vals[i])), "%Y%m%d")
                    meta_date_clean = str(date_obj.strftime("%d/%m/%Y"))
                    meta_values.append(meta_date_clean)
                    i += 1
                    continue
                meta_values.append(str(qry_md_vals.value(meta_vals[i])))
                i += 1
        return meta_values

    def get_data(self):
        """
        get values inputted by the user and record changes into the db
        :return:void
        """
        changed_text = {}
        scope_line_edit = self.meta_dia.ui.scopeLineEdit
        terr_line_edit = self.meta_dia.ui.terrLineEdit
        gaz_line_edit = self.meta_dia.ui.gazLineEdit
        email_line_edit = self.meta_dia.ui.mailLineEdit
        lang_check_box = self.meta_dia.ui.langCheckBox
        char_check_box = self.meta_dia.ui.charCheckBox
        changed_text["scope"] = "scope =  '" + str(scope_line_edit.text()) + "'"
        changed_text["territory"] = "territory = '" + str(terr_line_edit.text()) + "'"
        changed_text["owner"] = " owner = '" + str(gaz_line_edit.text()) + "'"
        changed_text["custodian"] = " custodian = '" + str(email_line_edit.text()) + "'"
        if lang_check_box.isChecked():
            changed_text["language"] = " gaz_language = 'WEL' "
        else:
            changed_text["language"] = " gaz_language = 'ENG' "
        if char_check_box.isChecked():
            changed_text["character"] = " charset = 'Welsh' "
        else:
            changed_text["character"] = " charset = 'English' "
        separator = " , "
        modified = (changed_text["scope"], changed_text["territory"], changed_text["owner"], changed_text["custodian"],
                    changed_text["language"], changed_text["character"])
        str_update = self.set_update_values + separator.join(modified)
        qry_update = QSqlQuery(str_update, self.db)
        self.close_browser()
        return

    def populate_check_boxes(self, value):
        """
        check if text boxes need to be checked or not
        :param value: string
        :return: bool
        """
        if value == "ENG" or value == "English":
            return False
        elif value == "WEL" or value == "Welsh":
            return True
        else:
            return False




