# -*- coding: utf-8 -*-
import copy
import datetime
import math
import re

from PyQt4.QtSql import QSqlQuery

from qgis.core import QgsGeometry, QgsFeature


__author__ = 'matthew.bradley'


class ExportCSV:
    """
    Main Class for CSV Exports
    """
    def __init__(self, version, file_name, asd, sts, org, lang, code, db):
        self.version = version
        self.csv = file_name
        self.inc_asd = asd
        self.inc_sts = sts
        self.tmp_streets = list()
        self.xref_sts = list()
        self.xref_esu = list()
        self.db = db
        self.esu_features = None
        self.line_count = 0
        self.rec_count = 0
        self.org_name = org
        self.code_num = code
        self.alt_lang = lang
        self.progress = None

    def export_lsg_to_dtf(self):
        """
        Export LSG to DTF
        :return:
        """
        self.export_header()
        self.export_streets()
        self.export_esus()
        self.export_xrefs()
        if self.version == 75 and self.inc_asd:
            self.export_asd()
        elif self.version == 6 or self.version == 7:
            self.export_asd()
        self.export_meta()
        self.export_trailer()

    def export_srwr(self):
        """
        Run methods for implementing SRWR Exports.
        """
        self.export_header(inc_lsg=False, srwr=True)
        self.export_asd()
        self.export_meta()
        self.export_trailer()

    def export_header(self, inc_lsg=True, srwr=False):
        """
        Exports necessary header row at the start of the CSV This needs to be run for every export.
        :param srwr: bool for SRWR exports (to set header)
        :param inc_lsg: Default is true. False for SRWR exports
        :return: None - but writes row to created CSV
        """
        ivolnum = 1
        today = datetime.datetime.now()
        today_date = today.date()
        today_time = today.time().strftime('%H%M%S')
        last_update = self.find_last_update().date()

        file_type = "F"
        if self.version == 75:
            if self.inc_asd is True and inc_lsg is True:
                file_type = "E"
            elif inc_lsg is True:
                file_type = "C"
            elif self.inc_asd is True or srwr:
                file_type = "G"
        # MB: version 6 (DTF 6.3) has a specific date format
        opts = {
            6: [10, self.org_name, self.code_num,
                datetime.datetime.strptime(str(today_date), '%Y-%m-%d').strftime('%m%d%y'), ivolnum, today_time, "6.3"],
            7: [10, self.org_name, self.code_num, today_date, ivolnum, today_date, today_time, "7.1", file_type],
            75: [10, self.org_name, self.code_num, today_date, ivolnum, today_date, today_time, "1.0", file_type]
        }
        aheader = opts.get(self.version)
        aheader = format_floats_and_strings(aheader)
        self.csv.writerow(aheader)

    def find_last_update(self):
        """
        Finds the most recent update date from either tblESU or tblSTREET.
        :rtype: datetime
        :return: Most recent date
        """
        # sqlite has no date data type so max works due to formatting YYYYMMDD
        max_tblstreet = "SELECT MAX(update_date) FROM tblSTREET"
        max_tblesu = "SELECT MAX(update_date) FROM tblESU"
        street_query = QSqlQuery(max_tblstreet, self.db)
        while street_query.next():
            street_max = street_query.value(0)
        esu_query = QSqlQuery(max_tblesu, self.db)
        while esu_query.next():
            esu_max = esu_query.value(0)
        street_max_d = datetime.datetime.strptime(str(street_max), "%Y%m%d")
        esu_max_d = datetime.datetime.strptime(str(esu_max), "%Y%m%d")
        # Return the most recent date
        if street_max_d > esu_max_d:
            return street_max_d
        else:
            return esu_max_d

    def format_date(self, date_str):
        """
        Takes a date string in YYYYMMDD format and returns as a string in YYYY-MM-DD format.
        :param date_str: date string
        :return: date string in YYYY-MM-DD format
        """
        try:
            date_str = str(date_str)
            date_time = datetime.datetime.strptime(date_str, '%Y%m%d')
            return str(date_time.date())
        except ValueError:
            return ""

    def export_streets(self):
        """
        Exports all streets to CSV
        :return:
        """
        record_num = 0

        language = self.alt_lang

        sql_template = """
           SELECT tblSTREET.*,
           tlkpLOCALITY.name AS Locality,
           tlkpLOCALITY.alt_name AS Locality_Alt,
           tlkpTOWN.name AS Town,
           tlkpTOWN.alt_name AS Town_Alt,
           tlkpCOUNTY.name AS County,
           tlkpCOUNTY.alt_name AS County_Alt
           FROM ((tblSTREET
              INNER JOIN tlkpTOWN
                 ON tblSTREET.town_ref = tlkpTOWN.town_ref)
              INNER JOIN tlkpLOCALITY
                 ON tblSTREET.loc_ref = tlkpLOCALITY.loc_ref)
              INNER JOIN tlkpCOUNTY
                 ON tblSTREET.county_ref = tlkpCOUNTY.county_ref
           WHERE  tblSTREET.street_ref_type < 5
               {extra_where_clauses}
           ;"""

        if self.inc_sts:
            extra_where_clauses = "AND (tblSTREET.currency_flag = 0 OR tblSTREET.Closure_date > 0)"
        else:
            extra_where_clauses = "AND tblSTREET.currency_flag = 0"
        sql = sql_template.format(extra_where_clauses=extra_where_clauses)

        query = QSqlQuery(self.db)
        query.exec_(sql)
        rec = query.record()
        # This gets all the right indexes for the query results, more flexibility for referencing each result
        aval = [rec.indexOf("USRN"),
                rec.indexOf("Version_No"),
                rec.indexOf("Street_ref_type"),
                rec.indexOf("description"),
                rec.indexOf("description_alt"),
                rec.indexOf("Entry_Date"),
                rec.indexOf("Update_Date"),
                rec.indexOf("Start_Date"),
                rec.indexOf("Authority"),
                rec.indexOf("Closure_Date"),
                rec.indexOf("start_xref"),
                rec.indexOf("start_yref"),
                rec.indexOf("end_xref"),
                rec.indexOf("end_yref"),
                rec.indexOf("tolerance"),
                rec.indexOf("street_state"),
                rec.indexOf("state_date"),
                rec.indexOf("street_class"),
                rec.indexOf("Locality"),
                rec.indexOf("Town"),
                rec.indexOf("County"),
                rec.indexOf("locality_alt"),
                rec.indexOf("town_alt"),
                rec.indexOf("county_alt")
                ]

        while query.next():
            self.line_count += 1
            record_num += 1

            if self.version > 6:
                if query.value(aval[15]) == "" or query.value(aval[15]) == 0:
                    query.value(aval[16]) == ""

            change = "I"
            if query.value(aval[9]) > 0:
                change = "D"

            opts = {
                6: [11,
                    query.value(aval[0]),
                    change,
                    query.value(aval[2]),
                    query.value(aval[3]),
                    query.value(aval[18]),
                    query.value(aval[19]),
                    query.value(aval[20]),
                    "",
                    "",
                    "",
                    "",
                    query.value(aval[8]),
                    query.value(aval[1]),
                    self.format_date(query.value(aval[6])),
                    self.format_date(query.value(aval[9])),
                    query.value(aval[10]),
                    query.value(aval[11]),
                    query.value(aval[12]),
                    query.value(aval[13]),
                    query.value(aval[14]),
                    1,
                    "",
                    self.format_date(query.value(aval[6])),
                    self.line_count],
                7: dict(street=[11,
                                change,
                                self.line_count,
                                query.value(aval[0]),
                                query.value(aval[2]),
                                query.value(aval[8]),
                                query.value(aval[15]),
                                self.format_date(query.value(aval[16])),
                                "",
                                query.value(aval[17]),
                                query.value(aval[1]),
                                self.format_date(query.value(aval[5])),
                                self.format_date(query.value(aval[6])),
                                self.format_date(query.value(aval[7])),
                                self.format_date(query.value(aval[9])),
                                query.value(aval[10]),
                                query.value(aval[11]),
                                query.value(aval[12]),
                                query.value(aval[13]),
                                query.value(aval[14])],
                        streetdesc=[15,
                                    change,
                                    self.line_count + 1,
                                    query.value(aval[0]),
                                    query.value(aval[3]),
                                    query.value(aval[18]),
                                    query.value(aval[19]),
                                    query.value(aval[20]),
                                    "ENG"],
                        streetalt=[15,
                                   change,
                                   self.line_count + 2,
                                   query.value(aval[0]),
                                   query.value(aval[4]),
                                   query.value(aval[21]),
                                   query.value(aval[22]),
                                   query.value(aval[23]),
                                   language]),
                75: dict(street=[11,
                                 change,
                                 self.line_count,
                                 query.value(aval[0]),
                                 query.value(aval[2]),
                                 query.value(aval[8]),
                                 query.value(aval[15]),
                                 self.format_date(query.value(aval[16])),
                                 query.value(aval[17]),
                                 self.format_date(query.value(aval[5])),
                                 self.format_date(query.value(aval[6])),
                                 self.format_date(query.value(aval[7])),
                                 self.format_date(query.value(aval[9])),
                                 query.value(aval[10]),
                                 query.value(aval[11]),
                                 query.value(aval[12]),
                                 query.value(aval[13])],
                         streetdesc=[15,
                                     change,
                                     self.line_count + 1,
                                     query.value(aval[0]),
                                     query.value(aval[3]),
                                     query.value(aval[18]),
                                     query.value(aval[19]),
                                     query.value(aval[20]),
                                     "ENG"],
                         streetalt=[15,
                                    change,
                                    self.line_count + 2,
                                    query.value(aval[0]),
                                    query.value(aval[4]),
                                    query.value(aval[21]),
                                    query.value(aval[22]),
                                    query.value(aval[23]),
                                    language])
            }
            if self.version is 6:
                streets = self.clean_street(opts.get(self.version), query.value(aval[2]))
                streets = format_floats_and_strings(streets)
                self.csv.writerow(streets)
                self.tmp_streets.append(streets)
                self.xref_sts.append(long(streets[1]))
            else:
                streets_first = self.set_state(opts.get(self.version)['street'])
                streets_first = format_floats_and_strings(streets_first)
                self.csv.writerow(streets_first)
                self.tmp_streets.append(streets_first)
                self.xref_sts.append(long(streets_first[3]))

                streets = self.clean_street(opts.get(self.version)['streetdesc'], query.value(aval[2]))
                self.line_count += 1
                streets = format_floats_and_strings(streets)
                self.csv.writerow(streets)
                self.tmp_streets.append(streets)
                self.xref_sts.append(streets[3])
                if language != "ENG" and query.value(aval[4]) != "":
                    streets_alt = self.clean_street(opts.get(self.version)['streetalt'], query.value(aval[2]))
                    self.line_count += 1
                    streets_alt = format_floats_and_strings(streets_alt)
                    self.csv.writerow(streets_alt)
                    self.tmp_streets.append(streets_alt)
                    self.xref_sts.append(streets_alt[3])

    def export_esus(self):
        """
        Exports the ESUs to the CSV alongside all the midpoints which make up the shape
        :return:
        """
        self.esu_features = self.get_esu_feature()
        esu_record = list()
        for feat in self.esu_features:
            if feat['result'] > 0:
                str(feat['esu_id'] + "(" + str(feat['ESUXYID']) + ")")
            else:
                self.line_count += 1
                if self.version == 6:
                    esu_record = [13,
                                  "I",
                                  feat['attributes']['ESUXYID'],
                                  feat['attributes']['version_no'],
                                  self.format_date(feat['attributes']['Update_Date']),
                                  self.format_date(feat['attributes']['closure_date']),
                                  feat['length'],
                                  feat['start']['x'],
                                  feat['start']['y'],
                                  feat['end']['x'],
                                  feat['end']['y'],
                                  feat['attributes']['tolerance'],
                                  self.format_date(feat['attributes']['entry_date']),
                                  self.line_count
                                  ]
                elif self.version == 7:
                    esu_record = [13,
                                  "I",
                                  self.line_count,
                                  feat['attributes']['ESUXYID'],
                                  feat['attributes']['version_no'],
                                  self.format_date(feat['attributes']['Update_Date']),
                                  self.format_date(feat['attributes']['closure_date']),
                                  feat['length'],
                                  feat['start']['x'],
                                  feat['start']['y'],
                                  feat['end']['x'],
                                  feat['end']['y'],
                                  feat['attributes']['tolerance'],
                                  self.format_date(feat['attributes']['entry_date']),
                                  self.format_date(feat['attributes']['start_date']),
                                  ""
                                  ]
                elif self.version == 75:
                    esu_record = [13,
                                  "I",
                                  self.line_count,
                                  feat['attributes']['ESUXYID'],
                                  self.format_date(feat['attributes']['Update_Date']),
                                  self.format_date(feat['attributes']['closure_date']),
                                  feat['length'],
                                  feat['start']['x'],
                                  feat['start']['y'],
                                  feat['end']['x'],
                                  feat['end']['y'],
                                  self.format_date(feat['attributes']['entry_date']),
                                  self.format_date(feat['attributes']['start_date'])
                                  ]
                esu_record = format_floats_and_strings(esu_record)
                self.csv.writerow(esu_record)
                midcount = 1
                esu_mid_coord = list()
                if len(feat['midpoints']) > 0:
                    for point in feat['midpoints'][0]:
                        self.line_count += 1
                        midcount += 1
                        if self.version == 6:
                            esu_mid_coord = [14,
                                             feat['attributes']['ESUXYID'],
                                             feat['attributes']['version_no'],
                                             "I",
                                             midcount,
                                             point[0],
                                             point[1],
                                             self.format_date(feat['attributes']['Update_Date']),
                                             self.line_count]
                        elif self.version == 7:
                            esu_mid_coord = [14,
                                             "I",
                                             self.line_count,
                                             feat['attributes']['ESUXYID'],
                                             feat['attributes']['version_no'],
                                             midcount,
                                             point[0],
                                             point[1]]
                        elif self.version == 75:
                            esu_mid_coord = [14,
                                             "I",
                                             self.line_count,
                                             feat['attributes']['ESUXYID'],
                                             midcount,
                                             point[0],
                                             point[1],
                                             self.format_date(feat['attributes']['entry_date']),
                                             self.format_date(feat['attributes']['closure_date']),
                                             self.format_date(feat['attributes']['Update_Date'])]
                        esu_mid_coord = format_floats_and_strings(esu_mid_coord)
                        self.csv.writerow(esu_mid_coord)

    def export_xrefs(self):
        """
        Exports Cross references for all streets.
        Queries database for current XRefs and exports them in appropriate format for version
        :return:
        """

        record_num = 0
        sql = """SELECT L.*, ( CASE WHEN U.xref <= 999999 THEN ( 0 || U.xref) ELSE U.xref END || CASE WHEN U.yref
        <= 999999 THEN ( 0 || U.yref) ELSE U.yref END ) as esuxyid
        FROM lnkESU_STREET L, tblESU U, tblSTREET S
        WHERE U.version_no = L.esu_version_no
        AND U.esu_id = L.esu_id
        AND S.USRN = L.USRN
        AND S.version_no = L.USRN_version_no
        AND L.currency_flag=0
        AND U.currency_flag=0;"""
        query = QSqlQuery(self.db)
        query.exec_(sql)
        rec = query.record()
        aval = [rec.indexOf("ESU_ID"),
                rec.indexOf("esuxyid"),
                rec.indexOf("USRN"),
                rec.indexOf("Usrn_version_no"),
                rec.indexOf("ESU_version_no"),
                rec.indexOf("entry_date"),
                rec.indexOf("update_date"),
                rec.indexOf("closure_date"),
                rec.indexOf("start_date")
                ]
        while query.next():
            if query.value(aval[2]) in self.xref_sts:
                if query.value(aval[0]) in self.xref_esu:
                    record_num += 1
                    self.line_count += 1
                    xref = list()
                    if self.version == 6:
                        xref = [12,
                                2,
                                query.value(aval[2]),
                                "I",
                                query.value(aval[3]),
                                query.value(aval[1]),
                                query.value(aval[4]),
                                "", self.line_count]
                    elif self.version == 7:
                        xref = [12,
                                "I",
                                self.line_count,
                                2,
                                query.value(aval[2]),
                                1,
                                query.value(aval[1]),
                                1]
                    elif self.version == 75:
                        xref = [12,
                                "I",
                                self.line_count,
                                query.value(aval[2]),
                                2,
                                query.value(aval[1]),
                                self.format_date(query.value(aval[5])),
                                self.format_date(query.value(aval[5])),
                                self.format_date(query.value(aval[7])),
                                self.format_date(query.value(aval[6]))]
                    xref = format_floats_and_strings(xref)
                    self.csv.writerow(xref)

    def export_asd(self):

        if self.version == 6:
            self.export_maint()
            self.export_spec_des()
            self.export_reins()
        elif self.version == 75:
            self.export_maint()
            self.export_reins()
            self.export_spec_des()

    def export_maint(self):
        """
        Export Maintenance records and writes them too CSV
        :return:
        """
        if self.inc_sts is True:
            swhereclause = "OR (tblSTREET.closure_date > 0)"
        else:
            swhereclause = ""

        sqlallmaint = """
            SELECT maint.*,
                   tblstreet.authority
            FROM   (SELECT tblmaint.*
                    FROM   tblmaint,
                           (SELECT tblmaint.maint_id,
                                   Max(tblmaint.version_no) AS MaxVersion_no
                            FROM   tblmaint
                            GROUP  BY tblmaint.maint_id) MaxMaint
                    WHERE  ( tblmaint.maint_id = MaxMaint.maint_id )
                           AND ( tblmaint.version_no = MaxMaint.maxversion_no )) maint,
                   tblstreet
            WHERE  ( ( maint.usrn = tblstreet.usrn )
                     AND ( tblstreet.street_ref_type < 3 )
                     AND (( ( maint.currency_flag = 0 )
                            AND ( tblstreet.currency_flag = 0 ) {swhereclause} )) )
            ORDER  BY maint.usrn,
                      maint.reference_no
                      ;""".format(swhereclause=swhereclause)
        query = QSqlQuery(self.db)
        query.exec_(sqlallmaint)
        rec = query.record()

        aval = [rec.indexOf("USRN"),
                rec.indexOf("Reference_no"),
                rec.indexOf("SWA_ORG_REF"),
                rec.indexOf("Location_Text"),
                rec.indexOf("Whole_Road"),
                rec.indexOf("Road_Status_Ref"),
                rec.indexOf("start_xref"),
                rec.indexOf("start_yref"),
                rec.indexOf("end_xref"),
                rec.indexOf("end_yref"),
                rec.indexOf("Currency_Flag")]

        while query.next():
            self.line_count += 1
            iwholerd = query.value(aval[4])
            if iwholerd == 1:
                sloctext = ""
                sstartx = ""
                sstarty = ""
                sendx = ""
                sendy = ""
            else:
                sloctext = query.value(aval[3])
                sstartx = query.value(aval[6])
                sstarty = query.value(aval[7])
                sendx = query.value(aval[8])
                sendy = query.value(aval[9])

            schange = "I"
            if query.value(aval[10]) == 1:
                schange = "D"

            amaint = list()
            if self.version == 6:
                amaint = [51,
                          query.value(aval[0]),
                          self.code_num,
                          query.value(aval[1]),
                          query.value(aval[2]),
                          iwholerd,
                          sloctext,
                          query.value(aval[5]),
                          sstartx,
                          sstarty,
                          sendx,
                          sendy]
            elif self.version == 7:
                amaint = []
            elif self.version == 75:
                amaint = [51,
                          schange,
                          self.line_count,
                          query.value(aval[0]),
                          self.code_num,
                          query.value(aval[1]),
                          query.value(aval[2]),
                          iwholerd,
                          sloctext,
                          query.value(aval[5]),
                          sstartx,
                          sstarty,
                          sendx,
                          sendy]
            amaint = format_floats_and_strings(amaint)
            self.csv.writerow(amaint)

    def export_reins(self):
        """
        Exports reinstatement records and writes them to CSV
        :return:
        """
        sqlallreins = """
            SELECT tblreins_cat.*
            FROM tblreins_cat LEFT JOIN tblstreet
                ON tblreins_cat.usrn = tblstreet.usrn
            WHERE tblstreet.street_ref_type < 3
                AND tblstreet.currency_flag = 0
                AND tblreins_cat.currency_flag = 0
            ORDER BY usrn, reference_no
            ;"""
        query = QSqlQuery(self.db)
        query.exec_(sqlallreins)
        rec = query.record()

        v = [rec.indexOf("USRN"),
             rec.indexOf("Reference_no"),
             rec.indexOf("Entry_Date"),
             rec.indexOf("Location_Text"),
             rec.indexOf("Whole_Road"),
             rec.indexOf("Reinstatement_Code"),
             rec.indexOf("start_xref"),
             rec.indexOf("start_yref"),
             rec.indexOf("end_xref"),
             rec.indexOf("end_yref")]
        while query.next():
            self.line_count += 1
            iwholerd = query.value(v[4])
            if iwholerd == 1:
                sloctext = ""
                sstartx = ""
                sstarty = ""
                sendx = ""
                sendy = ""
            else:
                sloctext = query.value(v[3])
                sstartx = query.value(v[6])
                sstarty = query.value(v[7])
                sendx = query.value(v[8])
                sendy = query.value(v[9])
            areins = list()
            if self.version == 6:
                areins = [52,
                          query.value(v[0]),
                          self.code_num,
                          query.value(v[1]),
                          query.value(v[5]),
                          iwholerd,
                          sloctext,
                          sstartx,
                          sstarty,
                          sendx,
                          sendy]
            elif self.version == 7:
                areins = []
            elif self.version == 75:
                areins = [52,
                          "I",
                          self.line_count,
                          query.value(v[0]),
                          self.code_num,
                          query.value(v[1]),
                          query.value(v[5]),
                          iwholerd,
                          sloctext,
                          sstartx,
                          sstarty,
                          sendx,
                          sendy]

            areins = format_floats_and_strings(areins)
            self.csv.writerow(areins)

    def export_spec_des(self):
        """

        :return:
        """
        sql_all_spec_des = """
            SELECT tblspec_des.*
            FROM tblspec_des LEFT JOIN tblstreet
                ON tblspec_des.usrn = tblstreet.usrn
            WHERE tblstreet.street_ref_type < 3
                AND tblstreet.currency_flag = 0
                AND tblspec_des.currency_flag = 0
            ORDER BY usrn, reference_no
            ;"""
        query = QSqlQuery(self.db)
        query.exec_(sql_all_spec_des)
        rec = query.record()

        aval = [rec.indexOf("USRN"),
                rec.indexOf("Reference_no"),
                rec.indexOf("SWA_ORG_REF"),
                rec.indexOf("Location_Text"),
                rec.indexOf("Whole_Road"),
                rec.indexOf("Designation_Code"),
                rec.indexOf("start_xref"),
                rec.indexOf("start_yref"),
                rec.indexOf("end_xref"),
                rec.indexOf("end_yref"),
                rec.indexOf("Description"),
                rec.indexOf("designation_date"),
                rec.indexOf("entry_date")]

        while query.next():
            self.line_count += 1
            iwholerd = query.value(aval[4])
            if iwholerd == 1:
                sloctext = ""
                sstartx = ""
                sstarty = ""
                sendx = ""
                sendy = ""
            else:
                sloctext = query.value(aval[3])
                sstartx = query.value(aval[6])
                sstarty = query.value(aval[7])
                sendx = query.value(aval[8])
                sendy = query.value(aval[9])
            aspecdes = list()
            if self.version == 6:
                aspecdes = [53,
                            query.value(aval[0]),
                            self.code_num,
                            query.value(aval[1]),
                            query.value(aval[5]),
                            iwholerd,
                            sloctext,
                            sstartx,
                            sstarty,
                            sendx,
                            sendy,
                            query.value(aval[10]),
                            query.value(aval[2])]
            elif self.version == 7:
                aspecdes = []
            elif self.version == 75:
                aspecdes = [53,
                            "I",
                            self.line_count,
                            query.value(aval[0]),
                            self.code_num,
                            query.value(aval[1]),
                            query.value(aval[5]),
                            iwholerd,
                            sloctext,
                            sstartx,
                            sstarty,
                            sendx,
                            sendy,
                            query.value(aval[10]),
                            query.value(aval[2])]
            aspecdes = format_floats_and_strings(aspecdes)
            self.csv.writerow(aspecdes)

    def export_meta(self):
        """
        Exports Metadata records and writes them to CSV in new line
        :return:
        """
        if self.version == 75:
            sqlgazmetadata = "SELECT * from tblGazMetadata;"
            query = QSqlQuery(self.db)
            query.exec_(sqlgazmetadata)
            query.first()
            rec = query.record()

            now_format = str(datetime.datetime.now().date())

            aval = [rec.indexOf("name"),
                    rec.indexOf("scope"),
                    rec.indexOf("territory"),
                    rec.indexOf("owner"),
                    rec.indexOf("custodian"),
                    rec.indexOf("coord_sys"),
                    rec.indexOf("coord_units"),
                    rec.indexOf("metadata_date"),
                    rec.indexOf("class_scheme"),
                    rec.indexOf("code_scheme"),
                    rec.indexOf("current_date"),
                    rec.indexOf("gaz_language"),
                    rec.indexOf("charset"),
                    rec.indexOf("custodian_code")]
            ameta = [29,
                     query.value(aval[0]),
                     query.value(aval[1]),
                     query.value(aval[2]),
                     query.value(aval[3]),
                     query.value(aval[4]),
                     query.value(aval[13]),
                     query.value(aval[5]),
                     query.value(aval[6]),
                     self.format_date(query.value(aval[7])),
                     query.value(aval[8]),
                     query.value(aval[9]),
                     now_format,
                     query.value(aval[12]),
                     query.value(aval[11])]

            self.csv.writerow(ameta)

        else:
            pass

    def export_trailer(self):
        """
        Writes Trailing Row to CSV to Finish
        """
        now = datetime.datetime.now()
        now_format = now.strftime('%Y%m%d')
        now_format_time = now.strftime('%H%M%S')

        lastchange = self.get_last_lsg_date()
        atrail = list()
        if self.version == 6:
            atrail = [99, 0, self.line_count, now_format, now_format_time]
        elif self.version == 7:
            atrail = [99, 0, self.line_count, self.format_date(lastchange), now_format_time]
        elif self.version == 75:
            atrail = [99, 0, self.line_count, self.format_date(lastchange), now_format_time]

        atrail = format_floats_and_strings(atrail)
        self.csv.writerow(atrail)

    def clean_street(self, street_list, street_type):
        """
        Clean/reformat street results.
        :param street_list: Array from database
        :param street_type: INT: street type
        :return: list
        """
        desc_idx = 4
        town_idx = 6

        desc = street_list[desc_idx]
        town = street_list[town_idx]

        # clean up the description text
        if street_type is 3:
            descarr = desc.split(" ")
            datac = descarr[0][0]
            if datac is "C" or datac is "U":
                desc = "Z" + desc
                desc = "Z" + desc
        if street_type is 3 or street_type is 1:
            desc.replace('(', '').replace(')', '')
        desc.replace('*', '').replace(' ', '')
        street_list[desc_idx] = desc

        # Clean up town text
        street_list[town_idx] = (town.split('/')[0] if town.find('/') >= 0 else town)

        # Replace all '<none>' lookup values with empty string
        clean_none = list()
        for item in street_list:
            if str(item).lower().strip() == '<none>':
                clean_none.append("")
            else:
                clean_none.append(item)
        return clean_none

    def get_esu_feature(self):
        # Run Query and get the matching features
        shape_tbl = 'SELECT AsBinary(E.geometry) AS geom, E.esu_id AS esuid, E.PK_UID AS FID, T.* ' \
                    'FROM esu E, tblESU T ' \
                    'WHERE E.esu_id = T.esu_id and T.currency_flag = 0'
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        query.exec_(shape_tbl)
        rec = query.record()

        feat_list = list()

        while query.next():
            esu_id = query.value(rec.indexOf("esuid"))
            geom = query.value(rec.indexOf("geom"))

            # write  a temp geom to extract the geom to be written
            g = QgsGeometry()
            g.fromWkb(geom)
            feat = QgsFeature()
            feat.setGeometry(g)

            geom = feat.geometry()
            count = len(geom.asMultiPolyline()[0])
            start = geom.vertexAt(0)
            end = geom.vertexAt(count - 1)

            # only write in a mid point if the line has a midpoint vert
            mids = None
            if count >= 2:
                geom.deleteVertex(count - 1)
                geom.deleteVertex(0)
                mids = geom.asMultiPolyline()

            esuy = query.value(rec.indexOf("yref"))
            esux = query.value(rec.indexOf("xref"))
            if esuy <= 999999:
                esuy = "0" + str(query.value(rec.indexOf("yref")))
            if esux <= 999999:
                esux = "0" + str(query.value(rec.indexOf("xref")))

            afields = dict(esu_id=query.value(rec.indexOf("esu_id")),
                           xref=query.value(rec.indexOf("xref")),
                           yref=query.value(rec.indexOf("yref")),
                           ESUXYID=str(esux) + str(esuy),
                           version_no=query.value(rec.indexOf("version_no")),
                           entry_date=query.value(rec.indexOf("entry_date")),
                           closure_date=query.value(rec.indexOf("closure_date")),
                           start_date=query.value(rec.indexOf("start_date")),
                           Update_Date=query.value(rec.indexOf("Update_Date")),
                           start_xref=query.value(rec.indexOf("start_xref")),
                           start_yref=query.value(rec.indexOf("start_yref")),
                           end_xref=query.value(rec.indexOf("end_xref")),
                           end_yref=query.value(rec.indexOf("end_yref")),
                           tolerance=query.value(rec.indexOf("tolerance")),
                           )

            if geom is not None:
                self.xref_esu.append(esu_id)
                item = dict(result=0, esu_id=esu_id, start={
                    'x': start[0],
                    'y': start[1]
                }, end={
                    'x': end[0],
                    'y': end[1]
                }, length=count, attributes=afields, midpoints=mids)
            else:
                item = dict(result=1, esu_id=esu_id, ESUXYID=int(str(esux) + str(esuy)))
            feat_list.append(item)

        return feat_list

    def get_last_lsg_date(self):
        """
        Finds the most recent record insert/update date from either ESU's or street records.
        :return: date formatted YYYYMMDD
        """
        last_date = 0

        last_street = "Select max(Update_Date) as LastChange FROM tblStreet"
        query = QSqlQuery(self.db)
        query.exec_(last_street)
        query.seek(0)
        rec = query.record()
        last_street_date = query.value(rec.indexOf('LastChange'))

        last_esu = "SELECT Max([closure_date]) AS LastClose, Max([entry_date]) AS lastEntry FROM tblESU"
        query_esu = QSqlQuery(self.db)
        query_esu.exec_(last_esu)
        query_esu.seek(0)
        rec_esu = query_esu.record()

        last_esu_closure = query_esu.value(rec_esu.indexOf('LastClose'))
        last_esu_entry = query_esu.value(rec_esu.indexOf('lastEntry'))

        if last_street_date > last_date:
            last_date = last_street_date
        if last_esu_closure > last_date:
            last_date = last_esu_closure
        if last_esu_entry > last_date:
            last_date = last_esu_entry

        return last_date

    def set_state(self, record):
        """
        Removes the state date from a street record (type 11) if the state is 'unknown' (0).
        :param record: List of type 11 record items
        """
        state = record[6]
        if state == 0:
            record[7] = ''
        return record


def format_floats_and_strings(row):
    """
    Round any floating point numbers in list to 2 decimal places.
    :param row: List of int, float and str to be passed to csv writer
    :return: Copy of list with floats rounded.
    """
    data = copy.copy(row)
    for i in range(len(data)):
        if isinstance(data[i], float):
            # Round up to match ESRI output
            data[i] = round(data[i], 2)
            data[i] = '{:.2f}'.format(data[i])
        if not isinstance(data[i], float) and not isinstance(data[i], int):
            fix_title_text = False
            if fix_title_text:  # Disabled for now because it segfaults
                data[i] = convert_to_title_case(data[i])

    return data


def convert_to_title_case(text):
    """
    Convert text to title case.  .title() doesn't work because it lower-cases
    non-first characters.
    :param text: text string
    :return: Text String In Title Case
    """
    text = copy.copy(str(text))
    capitalized_words = [word[0].upper() + word[1:] for word in text.split(' ')]
    text_as_title = ' '.join(capitalized_words)

    return text_as_title
