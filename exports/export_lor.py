# -*- coding: utf-8 -*-
import os
import csv

from PyQt4.QtSql import QSqlQuery


class ExportListOfRoads:
    """
    Simple class for exporting the list of roads option
    """

    def __init__(self, public_radio, any_radio, pub_chk, pro_chx, priv_chx, trunk_chx,
                 inc_t3_chx, inc_t4_chx, inc_lor_chx, usrn_chx, town_chx, csv_chx, out_dir, code, db):
        self.pubic_radio = public_radio
        self.any_radio = any_radio
        self.pub_chx = pub_chk
        self.pro_chx = pro_chx
        self.priv_chx = priv_chx
        self.trunk_chx = trunk_chx
        self.inc_t3_chx = inc_t3_chx
        self.inc_t4_chx = inc_t4_chx
        self.inc_lor_chx = inc_lor_chx
        self.usrn_cx = usrn_chx
        self.town_chx = town_chx
        self.csv_chx = csv_chx
        self.path = out_dir
        self.code = code
        self.db = db

        self.csv = None
        self.csv_filename = os.path.join(out_dir, 'untitled.csv')

    def export_lor(self):
        """
        Export list of roads to CSV.
        """
        strstatussql = ""  # List of road status codes to be included
        strstreettypesql = "1,2"  # List of street types to be included
        strincludefieldsql = ""  # SQL with additional fields to export
        strordersql = "tblSTREET.Description"  # SQL with additional sorting order

        if self.any_radio:
            if self.pub_chx:
                strstatussql += "1"
            if self.pro_chx:
                if strstatussql != "":
                    if strstatussql != "":
                        strstatussql += ","
                strstatussql += "2"
            if self.priv_chx:
                if strstatussql != "":
                    strstatussql += ","
                strstatussql += "3"
            if self.trunk_chx:
                if strstatussql != "":
                    strstatussql += ","
                strstatussql += "4"
        else:
            strstatussql = "1"
        if self.town_chx:
            strordersql = "tlkpTOWN.Name," + strordersql
        if self.inc_t3_chx or self.inc_t4_chx:
            if self.inc_t3_chx:
                strstreettypesql += ",3"
            if self.inc_t4_chx:
                strstreettypesql += ",4"
                strincludefieldsql += ", tblStreet.Street_Ref_Type as Type"
                strordersql = "tblStreet.Street_Ref_Type," + strordersql
        if self.inc_lor_chx:
            strincludefieldsql += ", tblMaint.Lor_No as Road_No"
        if self.usrn_cx:
            strincludefieldsql += ", tblSTREET.USRN as USRN"
        sql_lor = "SELECT DISTINCT tblSTREET.Description AS Name, tlkpTOWN.Name AS Town," \
                  " tblMAINT.Location_Text as Description, tlkpROAD_STATUS.Description as Status" \
                  " %s FROM (tlkpLOCALITY INNER JOIN (tlkpTOWN INNER JOIN tblSTREET" \
                  " ON tlkpTOWN.Town_Ref = tblSTREET.Town_Ref) ON tlkpLOCALITY.Loc_Ref = tblSTREET.Loc_Ref)" \
                  " INNER JOIN (tblMAINT INNER JOIN tlkpROAD_STATUS" \
                  " ON tblMAINT.Road_status_ref = tlkpROAD_STATUS.Road_status_ref) ON tblSTREET.USRN = tblMAINT.USRN" \
                  " WHERE ((tblMaint.Road_Status_Ref in ( %s ))" \
                  " AND (tblSTREET.Street_ref_type In ( %s )) AND (tblMAINT.Currency_flag=0)" \
                  " AND (tblSTREET.Currency_flag=0)) ORDER BY %s ;" % \
                  (strincludefieldsql, strstatussql, strstreettypesql, strordersql)

        query = QSqlQuery(self.db)
        query.exec_(sql_lor)
        rec = query.record()
        try:
            # create the output file
            if self.csv_chx:
                self.csv_filename = os.path.join(self.path,
                                                 "{}LOR.csv".format(self.code))
                output_file = open(self.csv_filename, "wb")
                self.csv = csv.writer(output_file, delimiter=',', quotechar='"',
                                      quoting=csv.QUOTE_NONNUMERIC, lineterminator='\r')
            else:
                self.csv_filename = os.path.join(self.path,
                                                 "{}.txt".format(self.code))
                output_file = open(self.csv_filename, "wb")
        # loop over each result and write it the text or CSV
            while query.next():
                vals = [
                    query.value(rec.indexOf('Name')),
                    query.value(rec.indexOf('Town')),
                    query.value(rec.indexOf('Description')),
                    query.value(rec.indexOf('Status'))
                ]
                if self.usrn_cx:
                    vals.append(query.value(rec.indexOf('USRN')))
                if self.inc_lor_chx:
                    vals.append(query.value(rec.indexOf('Road_No')))
                if self.csv_chx:
                    self.csv.writerow(list(vals))
                else:
                    line = str()
                    for v in vals:
                        if type(v) != unicode:
                            v = unicode(v)

                        line += v + " "
                    line += "\n"
                    output_file.write(line)
            output_file.close()
            return None
        except IOError:
            return self.csv_filename

