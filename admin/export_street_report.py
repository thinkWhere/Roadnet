# -*- coding: utf-8 -*-
import csv
from datetime import datetime

from PyQt4.QtSql import QSqlQuery, QSqlQueryModel
from PyQt4.QtCore import QModelIndex, Qt
from PyQt4.QtGui import QMessageBox

from Roadnet.roadnet_dialog import StreetReportsAlert
from Roadnet import database

__author__ = 'matthew.bradley'


class StreetReportsExport:
    def __init__(self, iface, db, export_path, options, csvBool, dia, params):
        self.iface = iface
        self.db = db
        self.street_dia = dia
        self.csv_requested = csvBool
        self.export_path = export_path + ".csv" if self.csv_requested else export_path + ".txt"
        self.options = options
        self.file = open(self.export_path, 'w')
        if self.csv_requested:
            self.csv = csv.writer(self.file, delimiter=',', quotechar='"',
                                  quoting=csv.QUOTE_NONNUMERIC, lineterminator='\r')
        self.report_title = "STREET CHANGES REPORT"
        self.no_content = "\n \nNO RECORDS FOUND \n \n"
        self.parser = None
        self.params = params
        self.org = database.get_from_gaz_metadata(db, "owner")
        self.user = self.params['UserName']
        self.error_alert = None
        self.headers = {
            0: ["USRN", "DESCRIPTION", "TYPE", "LOCALITY", "TOWN", "COUNTY", "START DATE", "ENTRY DATE",
                "UPDATE DATE", "CLOSURE DATE", "UPDATED BY", "CLOSED BY"],
            1: ["USRN", "TYPE", "DESCRIPTION", "LOCALITY", "TOWN", "COUNTY", "CATEGORY", "LOCATION_TEXT"]
        }

    def run_export(self):
        # if the additional table option is selected and no
        # additional tables are selected warns the user
        if self.options["tables"]["radio"] is True:
            if len(self.options["tables"]["result"]) == 0:
                # Please select an additional table
                # trigger a dialog box but remain in the street reports menu
                self.error_alert = StreetReportsAlert()
                self.error_alert.ui.cancelPushButton.clicked.connect(self.error_alert.close)
                self.error_alert.exec_()
                return
            else:
                self.report_srwr()
                self.street_dia.close()
        elif self.options["streets"]["radio"] is True:
            self.report_streets()
            self.street_dia.close()
        # shows a confirmation window when finished
        street_reports_export_msg_box = QMessageBox(QMessageBox.Information, " ",
                                                    "Export Street Reports Complete",
                                                    QMessageBox.Ok, None)
        street_reports_export_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        street_reports_export_msg_box.exec_()

    def report_srwr(self):

        sqlgenericsel = "SELECT s.USRN, s.Description,s.Street_ref_type, l.Name AS Locality, " \
                        "t.Name AS Town, c.name AS County, s.Start_Date, s.Entry_Date, s.Update_Date, " \
                        "s.Closure_Date, s.Updated_By, s.Closed_By "

        sqlgenericfrom = "((tblSTREET s INNER JOIN tlkpTOWN t ON s.Town_Ref = t.Town_Ref) " \
                         "INNER JOIN tlkpCOUNTY c ON s.County_Ref = c.county_ref) " \
                         "INNER JOIN tlkpLOCALITY l ON s.Loc_Ref = l.Loc_Ref "

        # Build a list of selected values from the listWidget
        listselected = list()

        for item in self.options["tables"]["result"]:
            sep = str(item.text()).find(":", 0, len(item.text()))
            listselected.append(item.text()[:sep])
            listselected.sort()

        # create comma sep list of values for query from an array
        strselected = ",".join(map(str, listselected))

        qrys = {
            1: " %s, lrs.Description as Category, m.location_text FROM (( %s ) "
               "INNER JOIN tblMaint m on s.USRN = m.USRN) "
               "LEFT JOIN tlkpRoad_Status lrs on m.Road_Status_ref = lrs.Road_Status_Ref "
               "WHERE s.Currency_flag = 0 AND m.Currency_Flag = 0 AND m.Road_Status_Ref in ( %s ) "
               "ORDER BY s.Street_Ref_Type,s.USRN" % (sqlgenericsel, sqlgenericfrom, strselected),

            2: " %s, lrc.Description as Category, rc.location_text FROM (( %s ) "
               "INNER JOIN tblReins_Cat rc on s.USRN = rc.USRN) "
               "LEFT JOIN tlkpReins_Cat lrc on rc.Reinstatement_Code = lrc.Reinstatement_Code "
               "WHERE s.Currency_flag = 0 AND rc.Currency_Flag = 0 AND rc.Reinstatement_Code in ( %s ) "
               "ORDER BY s.Street_Ref_Type,s.USRN" % (sqlgenericsel, sqlgenericfrom, strselected),

            3: " %s, lsg.Designation_text as Category,sd.location_text FROM (( %s ) "
               "INNER JOIN tblSpec_Des sd on s.USRN = sd.USRN) "
               "LEFT JOIN tlkpSpec_Des lsg on sd.Designation_Code = lsg.Designation_Code "
               "WHERE s.Currency_flag = 0 AND sd.Currency_Flag = 0 AND sd.Designation_Code in ( %s ) "
               "ORDER BY s.Street_Ref_Type,s.USRN" % (sqlgenericsel, sqlgenericfrom, strselected)
        }

        avals = ["USRN", "Description", "Street_ref_type", "Locality", "Town", "County", "Category", "location_text"]

        if self.csv_requested:
            self.csv.writerow(["Street with " + str(self.options["tables"]["type"]) + " Categories in " + strselected])
            self.csv.writerow(self.headers[1])
            self.results_to_csv_row(avals, qrys.get(self.options["tables"]["combo"]), "srwr")
        else:
            self.start_report()
            header = "Street with " + str(self.options["tables"]["type"]) + " Categories in " + strselected + "\n"
            self.file.write(header)
            line_length = len(header)
            self.file.write('-' * line_length + "\n \n")
            self.results_to_txt_row(avals, qrys.get(self.options["tables"]["combo"]), "srwr")
            self.end_report()

    def report_streets(self):
        sqlgenericsel = "SELECT tblSTREET.USRN, tblStreet.Description,tblSTREET.Street_ref_type, " \
                        "tlkpLOCALITY.Name AS Locality, tlkpTOWN.Name AS Town, tlkpCOUNTY.name AS County, " \
                        "tblStreet.Start_Date, tblStreet.Entry_Date, tblStreet.Update_Date, tblStreet.Closure_Date, " \
                        "tblStreet.Updated_By, tblStreet.Closed_By FROM ((tblSTREET INNER JOIN tlkpTOWN ON " \
                        "tblSTREET.Town_Ref = tlkpTOWN.Town_Ref) INNER JOIN tlkpCOUNTY ON " \
                        "tblSTREET.County_Ref = tlkpCOUNTY.county_ref) INNER JOIN tlkpLOCALITY " \
                        "ON tblSTREET.Loc_Ref = tlkpLOCALITY.Loc_Ref "

        entry = sqlgenericsel + "WHERE tblStreet.Entry_Date > " + self.options["streets"]["result"] + \
                                " AND tblStreet.currency_flag = 0"
        closed = sqlgenericsel + "WHERE tblStreet.Closure_date > " + self.options["streets"]["result"]
        changed = sqlgenericsel + "WHERE tblStreet.Update_date > " + self.options["streets"]["result"] + \
                                  " AND tblStreet.currency_flag = 0 " \
                                  "AND tblStreet.Entry_date < " + self.options["streets"]["result"]

        avals = ["USRN", "Description", "Street_ref_type", "Locality", "Town", "County", "Start_Date", "Entry_Date",
                 "Update_Date", "Closure_Date", "Updated_By", "Closed_By"]

        if self.csv_requested:
            self.csv.writerow(["New Streets Since ", self.format_dates(str(self.options["streets"]["result"]))])
            self.csv.writerow(avals)
            self.results_to_csv_row(avals, entry, "streets")
            self.csv.writerow(["Closed Streets Since ", self.format_dates(str(self.options["streets"]["result"]))])
            self.csv.writerow(avals)
            self.results_to_csv_row(avals, entry, "streets")
            self.csv.writerow(["Updated Streets Since ", self.format_dates(str(self.options["streets"]["result"]))])
            self.csv.writerow(avals)
            self.results_to_csv_row(avals, entry, "streets")

        else:
            self.start_report()
            header = "New Streets Since " + self.format_dates(str(self.options["streets"]["result"])) + "\n"
            self.file.write(header)
            line_length = len(header)
            self.file.write('-' * line_length + "\n \n")
            self.results_to_txt_row(avals, entry, "streets")
            header = "Closed Streets Since " + self.format_dates(str(self.options["streets"]["result"])) + "\n"
            self.file.write(header)
            line_length = len(header)
            self.file.write('-' * line_length + "\n \n")
            self.results_to_txt_row(avals, closed, "streets")
            header = "Updated Streets Since " + self.format_dates(str(self.options["streets"]["result"])) + "\n"
            self.file.write(header)
            line_length = len(header)
            self.file.write('-' * line_length + "\n \n")
            self.results_to_txt_row(avals, changed, "streets")
            self.end_report()

    def results_to_txt_row(self, vals, sql, mode):
        query_model = QSqlQueryModel()
        query_model.setQuery(sql)
        model_index = QModelIndex()
        row_count = query_model.rowCount(model_index)
        if row_count < 1:
            self.file.write(self.no_content)
        else:
            query = QSqlQuery(self.db)
            query.exec_(sql)
            rec = query.record()
            if mode == "streets":
                avals = [rec.indexOf(vals[0]), rec.indexOf(vals[1]), rec.indexOf(vals[2]), rec.indexOf(vals[3]),
                         rec.indexOf(vals[4]), rec.indexOf(vals[5]), rec.indexOf(vals[6]), rec.indexOf(vals[7]),
                         rec.indexOf(vals[8]), rec.indexOf(vals[9]), rec.indexOf(vals[10]), rec.indexOf(vals[11])
                         ]
                n = 0
                # write content
                headers = self.headers[0]
                while n <= len(headers) - 1:
                    if n == len(headers) - 1:
                        self.file.write(str(headers[n]) + "\n")
                    else:
                        self.file.write(str(headers[n]) + " ")
                    n += 1
                while query.next():
                    line = [query.value(avals[0]), query.value(avals[1]), query.value(avals[2]),
                            query.value(avals[3]), query.value(avals[4]), query.value(avals[5]),
                            query.value(avals[6]), query.value(avals[7]), query.value(avals[8]),
                            query.value(avals[9]), query.value(avals[10]), query.value(avals[11])]

                    self.file.write(str(line[0]) + " , " + str(line[1]) + " , " + str(line[2]) + " , " +
                                    str(line[3]) + " , " + str(line[4]) + " , " + str(line[5]) + " , " +
                                    self.format_dates(str(line[6])) + " , " + self.format_dates(str(line[7])) +
                                    " , " + self.format_dates(str(line[8])) + " , " + self.format_dates(str(line[9])) +
                                    " , " + str(line[10]) + " " + str(line[11]) + "\n"
                                    )
            else:
                avals = [rec.indexOf(vals[0]), rec.indexOf(vals[1]), rec.indexOf(vals[2]), rec.indexOf(vals[3]),
                         rec.indexOf(vals[4]), rec.indexOf(vals[5]), rec.indexOf(vals[6]), rec.indexOf(vals[7])]
                m = 0
                headers = self.headers[1]
                while m <= len(headers) - 1:
                    if m == len(headers) - 1:
                        self.file.write(str(headers[m]) + "\n")
                    else:
                        self.file.write(str(headers[m]) + " ")
                    m += 1
                while query.next():
                    line = [query.value(avals[0]), query.value(avals[1]), query.value(avals[2]), query.value(avals[3]),
                            query.value(avals[4]), query.value(avals[5]), query.value(avals[6]), query.value(avals[7])]
                    self.file.write(
                        str(line[0]) + " , " + str(line[1]) + " , " + str(line[2]) + " , " + str(line[3]) + " , " +
                        str(line[4]) + " , " + str(line[5]) + " , " + str(line[6]) + " , " + str(line[7]) + "\n")

    def results_to_csv_row(self, vals, sql, mode):
        query = QSqlQuery(self.db)
        query.exec_(sql)
        rec = query.record()
        if mode == "streets":
            avals = [rec.indexOf(vals[0]), rec.indexOf(vals[1]), rec.indexOf(vals[2]), rec.indexOf(vals[3]),
                     rec.indexOf(vals[4]), rec.indexOf(vals[5]), rec.indexOf(vals[6]), rec.indexOf(vals[7]),
                     rec.indexOf(vals[8]), rec.indexOf(vals[9]), rec.indexOf(vals[10]), rec.indexOf(vals[11])
                     ]
            while query.next():
                line = [query.value(avals[0]), query.value(avals[1]), query.value(avals[2]), query.value(avals[3]),
                        query.value(avals[4]), query.value(avals[5]), self.format_dates(str(query.value(avals[6]))),
                        self.format_dates(str(query.value(avals[7]))),
                        self.format_dates(str(query.value(avals[8]))),
                        self.format_dates(str(query.value(avals[9]))),
                        query.value(avals[10]), query.value(avals[11])]
                self.csv.writerow(line)
        else:
            avals = [rec.indexOf(vals[0]), rec.indexOf(vals[1]), rec.indexOf(vals[2]), rec.indexOf(vals[3]),
                     rec.indexOf(vals[4]), rec.indexOf(vals[5]), rec.indexOf(vals[6]), rec.indexOf(vals[7])]

            while query.next():
                line = [query.value(avals[0]), query.value(avals[1]), query.value(avals[2]), query.value(avals[3]),
                        query.value(avals[4]), query.value(avals[5]), query.value(avals[6]), query.value(avals[7])]

                self.csv.writerow(line)

    def format_dates(self, input_date):
        if input_date is "NULL" or input_date == "0":
            output_date = ""
            return output_date
        else:
            try:
                in_date_obj = datetime.strptime(input_date, "%Y%m%d")
                output_date = str((in_date_obj.strftime("%d/%m/%Y")))
            except ValueError:
                output_date = ""
            return output_date

    def start_report(self):
        self.file.write(str(self.report_title) + ' for {0} \n'.format(self.org))
        self.file.write('Created on : {0} at {1} By : {2} \n'.format(datetime.today().strftime("%d/%m/%Y"),
                                                                     datetime.now().strftime("%H:%M"),
                                                                     str(self.user)))
        self.file.write(
            "------------------------------------------------------------------------------------------ \n \n \n \n")

    def end_report(self):
        self.file.write("\n \n \n")
        self.file.write("---------- End of Report -----------")
