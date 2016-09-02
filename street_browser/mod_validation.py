# -*- coding: utf-8 -*-
from PyQt4.QtSql import QSqlQuery

__author__ = 'matthew.walsh'


class ValidateDescription:
    """
    Validation check to ensure that a street description is unique to the town and locality
    """

    def __init__(self, street_browser, db):
        self.db = db
        self.street_browser = street_browser
        self.usrn = None

    def validate(self, usrn=None):
        """
        Main method to run validation, True = valid desc
        :param usrn: current USRN
        :return: true if desc is unique
        """
        self.usrn = usrn
        params = self.get_query_params()
        valid = self.validation_query(params[0], params[1], params[2])
        return valid

    def get_query_params(self):
        """
        Get the desc, town_ref and loc_ref from the street browser
        :rtype : (str, str, str)
        :return: new description, town id, location id
        """
        desc = str(self.street_browser.ui.descriptionTextEdit.toPlainText())
        town_combo = self.street_browser.ui.townComboBox
        town_ref = str(town_combo.itemData(town_combo.currentIndex()))
        loc_combo = self.street_browser.ui.localityComboBox
        loc_ref = str(loc_combo.itemData(loc_combo.currentIndex()))
        return desc, town_ref, loc_ref

    def validation_query(self, desc, town_ref, loc_ref):
        """
        Run validation query, returns True for unique description text
        :param desc: Description string
        :param town_ref: town id
        :param loc_ref: location id
        :return: true if match found
        """
        sql = "SELECT description FROM tblSTREET WHERE LOWER(description) = " \
              "LOWER('%s') AND town_ref = %s AND loc_ref = %s AND currency_flag = 0" % (desc, town_ref, loc_ref)
        if self.usrn:
            # usrn is provided for existing records, so it doesnt count itself
            sql += " AND usrn != %s" % str(self.usrn)
        query = QSqlQuery(sql, self.db)
        if query.seek(0):
            return False
        else:
            return True


class ValidateStreetType:
    """
    Checks to ensure a Esu is only attached to a single type 1 or type 2 street
    """

    def __init__(self, street_browser, db):
        self.street_browser = street_browser
        self.db = db

    def get_esu_selection(self, usrn):
        """
        Get the Esu selection from db
        :param usrn: USRN
        :return: list of esu's
        """
        esu_selection = []
        sql = "select esu_id from lnkESU_STREET where usrn = %s and currency_flag = 0" % usrn
        query = QSqlQuery(sql, self.db)
        while query.next():
            esu_selection.append(query.value(0))
        return esu_selection

    def validate(self, usrn, final_esu_selection=None):
        """
        Validates that all ESU's are only attached to a single type-1 or type-2 usrn
        :param usrn: USRN
        :param final_esu_selection: list of esu's
        :return: true if esu links are valid
        """
        record_type_combo = self.street_browser.ui.recordTypeComboBox
        if final_esu_selection:
            esu_list = final_esu_selection
        else:
            esu_list = self.get_esu_selection(usrn)
        # only need to check type 1 and 2 records
        record_type = int(record_type_combo.itemData(record_type_combo.currentIndex()))
        if record_type == 1 or record_type == 2:  # Type 1 or Type 2 hardcoded!
            bad_esu = []
            for esu_key in esu_list:
                sql = """SELECT tblSTREET.usrn, tblSTREET.street_ref_type FROM lnkESU_STREET
                    INNER JOIN tblSTREET ON lnkESU_STREET.usrn_version_no = tblSTREET.version_no
                    AND lnkESU_STREET.usrn = tblSTREET.usrn WHERE lnkESU_STREET.esu_id = %s
                    AND lnkESU_STREET.currency_flag = 0 AND tblSTREET.currency_flag = 0 AND tblSTREET.usrn != %s""" \
                    % (esu_key, usrn)
                query = QSqlQuery(sql, self.db)
                while query.next():
                    typee = int(query.value(1))
                    if typee == 1 or typee == 2:
                        bad_esu.append(esu_key)
            if bad_esu:
                # esu's found
                return False
            else:
                return True
        else:
            return True
