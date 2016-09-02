# -*- coding: utf-8 -*-
__author__ = 'Alessandro'

import os
from math import sqrt
from PyQt4.QtSql import QSqlQueryModel, QSqlQuery
from PyQt4.QtCore import QObject, QRunnable, pyqtSignal, QModelIndex
from qgis.core import QgsMapLayerRegistry, QgsPoint, QgsFeatureRequest
from datetime import datetime

report_file = None
user = ""
queries = {}
headers = {}
headers_no_items = {}
column_names = {}
db = None
esu_layer = None
poly_layer = None
tol = None
passing_list = []


def write_header(section_header, include_footpaths=False, include_subtitle=False):
    """
    prints different header formats, dependent on the element to validate_mandatory
    :param section_header: id of the header from dict headers
    :param include_footpaths: bool include or not the 'include path' string
    :param include_subtitle: bool include or not a subtitle
    :return: void
    """
    global db
    global report_file
    # include footpaths string and note
    if include_footpaths:
        title = section_header[0]
        subtitle = section_header[1]
        note = section_header[2]
        title_length = len(title)
        note_length = len(note)
        report_file.write(title + "\n")
        report_file.write('-' * title_length + "\n")
        report_file.write(subtitle + "\n \n")
        report_file.write(note + "\n")
        report_file.write('-' * note_length + "\n \n")
    # include note but not footpath string
    elif isinstance(section_header, list) and not include_subtitle:
        title = section_header[0]
        note = section_header[2]
        title_length = len(title)
        note_length = len(note)
        report_file.write(title + "\n")
        report_file.write('-' * title_length + "\n \n")
        report_file.write(note + "\n")
        report_file.write('-' * note_length + "\n \n")
    # include subtitles
    elif (isinstance(section_header, list)) and include_subtitle:
        title = section_header[0]
        subtitle = section_header[1]
        title_length = len(title)
        report_file.write(title + "\n")
        report_file.write('-' * title_length + "\n \n")
        report_file.write(subtitle + "\n \n")
    else:
        # print a simple header
        line_length = len(section_header)
        report_file.write(section_header + "\n")
        report_file.write('-' * line_length + "\n \n")
    report_file.flush()
    os.fsync(report_file.fileno())


def write_content(query_id, header_id, header_no_content_id, columns_name_id, include_footpaths=True,
                  include_subtitle=False):
    """
    format the content of the data coming from the db either in text or dialog format
    :param query_id: int reference to the query dictionary
    :param header_id: int reference to the header dictionary
    :param header_no_content_id: int reference to the header no content dictionary
    :param columns_name_id: int reference to the list of columns of the required table
    :param include_footpaths: bool value to include footpaths in type 3 streets query
    :param include_subtitle: bool indicates if the header has a subtitle
    :return: void
    """
    global report_file
    global queries
    global db
    # build a query model object
    query_model = QSqlQueryModel()
    if not include_footpaths:
        filtered_query = queries[2].replace("AND (lnkESU_STREET.Currency_flag = 0)",
                                            "AND (lnkESU_STREET.Currency_flag = 0) AND "
                                            "(tblStreet.Description not like '%Footpath%')")
        query_model.setQuery(filtered_query)
    else:
        query = QSqlQuery(queries[query_id], db)
        query_model.setQuery(query)
    while query_model.canFetchMore():
        query_model.fetchMore()
    parent_model_index = QModelIndex()
    # if the path is not specified sends data to function creating a list
    if report_file is None:
        content_to_screen(content_list=None, query_model=query_model,columns_name_id=columns_name_id,
                          no_content_id=header_no_content_id)
    else:
        # get number of rows and columns
        n_rows = query_model.rowCount(parent_model_index)
        n_columns = query_model.columnCount(parent_model_index)
        # if the report is textual write the header title
        # include footpaths
        if include_footpaths and header_id == 2:
            write_header(headers[2], True)
        # report includes a subtitle but not footpaths
        elif include_subtitle:
            write_header(headers[header_id], False, True)
        else:
            # write a simple header
            write_header(headers[header_id])
        # if there are no rows write the header title no content
        if n_rows < 1:
            report_file.write(headers_no_items[header_no_content_id] + " \n \n \n")
            return
        # write the content to the text file
        else:
            i = 0
            j = 0
            k = 0
            # write column names
            while k <= len(column_names[columns_name_id]) - 1:
                if k == len(column_names[columns_name_id]) - 1:
                    report_file.write(column_names[columns_name_id][k] + "\n")
                else:
                    report_file.write(column_names[columns_name_id][k])
                k += 1
            # identify data in the model and write to txt file
            while i <= n_rows - 1:
                while j <= n_columns - 1:
                    model_index = query_model.createIndex(i, j)
                    data = str(model_index.data())
                    report_file.write("{0}".format(data))
                    j += 1
                j = 0
                # if it is the last item put three line breaks
                if i == n_rows - 1:
                    report_file.write("\n \nTOTAL : {0} \n".format(str(n_rows)))
                    report_file.write("\n \n \n")
                else:
                    report_file.write("\n")
                i += 1
            report_file.flush()
            os.fsync(report_file.fileno())


def content_to_screen(content_list=None, query_model=None, columns_name_id=None, no_content_id=None):
    """
    handles the creation of an on-screen validation report version, the function handles the case
    of a report created both from db records and mixed data from db and spatial features
    :param content_list: list[string] 'ready made' list of values to print on the screen if data comes
    from mixed sources (db + features)
    :param query_model: QtSqlQueryModel model of the query if all data comes from db
    :param columns_name_id: int index of the column names dictionary to print column names on tables
    """
    global passing_list
    if content_list is None:
        parent_model_index = QModelIndex()
        # get number of rows and columns
        n_rows = query_model.rowCount(parent_model_index)
        n_columns = query_model.columnCount(parent_model_index)
        # if the path is not specified build the list view
        # creates a list of values
        content_list = []
        items_list = []
        i = 0
        j = 0
        k = 0
        while k <= len(column_names[columns_name_id]) - 1:
            content_list.append(column_names[columns_name_id])
            k += 1
            # if there are no problems just print a message
            # on the first item in the list
        if n_rows < 1:
            content_list.append([headers_no_items[no_content_id]])
        else:
            # identify data in the model and write to txt file
            while i <= n_rows - 1:
                while j <= n_columns - 1:
                    model_index = query_model.createIndex(i, j)
                    data = str(model_index.data())
                    items_list.append(data)
                    j += 1
                content_list.append(items_list)
                j = 0
                items_list = []
                i += 1
        passing_list = content_list


def start_end_proximity(start_point_street, end_point_street, feature, tolerance):
    """
    check distance of start and end point of the street with each ESU
    if it is greater or smaller than the set tolerance
    :param start_point: start point of each street to which the ESU is linked
    :param end_point: endpoint of each street to which the ESU is linked
    :param feature: the ESU to test
    :param tolerance: distance in metres expressed by the user, over which we flag up a problem
    :return int result: integer that expresses if the distance of the start end point of the ESU
                        from the tart end point of the street is greater or lower than the set tolerance
    """
    result = 0
    geom = feature.geometry()
    multi_poly_list = geom.asMultiPolyline()
    # if the geometry is not empty check start end coords
    if len(multi_poly_list) > 0:
        multi_poly = geom.asMultiPolyline()[0]
        # " feature has " + str(multi_poly) + str()
        len_list = len(multi_poly)
        start_point_esu = multi_poly[0]
        end_point_esu = multi_poly[len_list - 1]
        # test 1: distance between start vertex of ESU and start point of street
        dist_start_1 = sqrt(start_point_esu.sqrDist(start_point_street))
        # test 2: distance between start vertex of ESU and end point of street
        dist_end_1 = sqrt(start_point_esu.sqrDist(end_point_street))
        # test 3: distance between end vertex of ESU and start point of street
        dist_start_2 = sqrt(end_point_esu.sqrDist(start_point_street))
        # test 4: distance between end vertex of ESU and end point of street
        dist_end_2 = sqrt(end_point_esu.sqrDist(end_point_street))
        # start tolerances evaluation
        if dist_start_1 < tolerance or dist_start_2 < tolerance:
            result = 1
        # end tolerances evaluation
        if dist_end_1 < tolerance or dist_end_2 < tolerance:
            result += 2
    return result


def get_linked_esu_list(usrn):
    """
    function that selects all esus for a determined street
    :param usrn: the unique identifier of a certain street
    :return: list[esu_ids] all esu ids linked to a certain street or
    void in case a street does not have any linked esu
    """
    # executing the query
    global db
    esus_query_model = QSqlQueryModel()
    esus_query_model.setQuery(queries[9].format(usrn))
    while esus_query_model.canFetchMore():
        esus_query_model.fetchMore()
    n_rows = esus_query_model.rowCount()
    if n_rows == 0:
        return
    else:
        i = 0
        esus_list = []
        # creating a list of ESUs Ids that are linked to the street
        while i <= n_rows - 1:
            model_index = esus_query_model.createIndex(i, 0)
            esu = model_index.data()
            esus_list.append(esu)
            i += 1
        return esus_list


def build_layer_filter(esus_list):
    """
    builds a qgis layer expression from a list of strings to return
    filtered features from a layer
    :param esus_list: list of strings containing all ESUs in a street
    :return: string filter to apply to feature request
    """
    str_esu = ""
    i = 0
    while i <= len(esus_list) - 1:
        if i == 0 or i == len(esus_list):
            str_esu += '"esu_id" = ' + str(esus_list[i]) + ' '
        else:
            str_esu += 'OR "esu_id" = ' + str(esus_list[i]) + ' '
        i += 1
    return str_esu


class StartReport(QRunnable):
    def __init__(self, file_path, org_name):
        super(StartReport, self).__init__()
        # open the db connection in thread
        db.open()
        self.signals = GeneralSignals()
        self.file_path = file_path
        self.task = "Starting Report"
        self.progress = 1
        self.org_name = org_name
        self.user = user
        self.report_title = "roadNet Validation Report"

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        global report_file
        # create the file and prints the header
        report_file = open(self.file_path, 'wb')
        report_file.write(str(self.report_title) + ' for {0} \n'.format(self.org_name))
        report_file.write('Created on : {0} at {1} By : {2} \n'.format(datetime.today().strftime("%d/%m/%Y"),
                                                                       datetime.now().strftime("%H:%M"),
                                                                       str(self.user)))
        report_file.write(
            "----------------------------------------"
            "-------------------------------------------------- \n \n \n \n")
        report_file.flush()
        os.fsync(report_file.fileno())


class EndReport(QRunnable):
    def __init__(self):
        super(EndReport, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Finishing report"
        self.progress = 100

    def run(self):

        self.signals.result.emit(self.task, self.progress)
        if report_file is not None:
            # write footer and close file
            report_file.write("\n \n \n")
            report_file.write("---------- End of Report -----------")
            report_file.flush()
            os.fsync(report_file.fileno())
            report_file.close()

            self.signals.report_finished.emit()


class DupStreetDesc(QRunnable):
    """
    duplicate street description report section creation
    :return: void if the report is to text
            list[string] if the report is to screen
    """

    def __init__(self):
        super(DupStreetDesc, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking duplicate street descriptions..."
        self.progress = 16.6

    def run(self):
        self.signals.result.emit(self.task,self.progress)
        if report_file is None:
            write_content(0, 0, 0, 0)
            global passing_list
            self.signals.list.emit(passing_list,'dupStreetCheckBox')

        else:
            write_content(0, 0, 0, 0)


class StreetsNoEsuDesc(QRunnable):
    """
    streets not linked to ESU report section creation
    :return: void if the report is to text
            list[string] if the report is to screen
    """

    def __init__(self):
        super(StreetsNoEsuDesc, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking streets not linked to ESUs..."
        self.progress = 25

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            write_content(1, 1, 1, 1)
            global passing_list
            self.signals.list.emit(passing_list,'notStreetEsuCheckBox')

        else:
            write_content(1, 1, 1, 1)


class Type3Desc(QRunnable):
    """
    streets not connected to type 3 report section
    :param include_footpath: bool, include or not footpath in the query
    :return: void if the report is to text
            list[string] if the report is to screen
    """

    def __init__(self, include_footpath):
        super(Type3Desc, self).__init__()
        self.signals = GeneralSignals()
        self.include_fp = include_footpath
        if self.include_fp:
            self.task = "Checking ESUs linked to Public Type 1 or 2 Streets but not to Type 3 \n" \
                        "(Including Footpaths)..."
        else:
            self.task = "Checking ESUs linked to Public Type 1 or 2 Streets but not to Type 3..."
        self.progress = 33.3

    def run(self):
        global passing_list
        self.signals.result.emit(self.task, self.progress)
        if self.include_fp:
            if report_file is None:
                write_content(2, 2, 2, 2)
                self.signals.list.emit(passing_list, 'incFootPathCheckBox')
            else:
                write_content(2, 2, 2, 2)
        else:
            if report_file is None:
                write_content(2, 2, 2, 2, False)
                self.signals.list.emit(passing_list, 'notType3CheckBox')

            else:
                write_content(2, 2, 2, 2, False)


class DupEsuRef(QRunnable):
    """
    duplicate ESU references report section
    :param include_subtitle: include or not a header subtitle
    :return: void if the report is to text
    list[string] if the report is to screen, the subtitile is
    included by default
    """

    def __init__(self, include_subtitle):
        super(DupEsuRef, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking Duplicate ESU References..."
        self.include_st = include_subtitle
        self.progress = 41.6

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            write_content(3, 3, 3, 3)
            global passing_list
            self.signals.list.emit(passing_list, 'dupEsuRefCheckBox')

        else:
            if self.include_st:
                write_content(3, 3, 3, 3, True, True)
            else:
                write_content(3, 3, 3, 3)


class NoLinkEsuStreets(QRunnable):
    """
    section report on ESUs not linked to any street
    :return:void if the report is to text
            list[string] if the report is to screen, the subtitile is
            not included by default
    """

    def __init__(self):
        super(NoLinkEsuStreets, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking ESUs not linked to Streets..."
        self.progress = 50

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            write_content(4, 4, 4, 4)
            global passing_list
            self.signals.list.emit(passing_list, 'notEsuStreetCheckBox')

        else:
            write_content(4, 4, 4, 4)


class InvalidCrossReferences(QRunnable):
    """
        this function handles three checks that are grouped
        under the same checkbox in the form 'invalid cross references'
        first check: ESUs not linked to type 1 and 2 streets
        second check: ESUs linked to type 3 and 4 streets but not linked to type 1 or 2
        third check: ESUs linked to unofficial street types (none of the previous type)
        :return void if the report is to text
                list[[string]x3] if the report is to screen
        """

    def __init__(self):
        super(InvalidCrossReferences, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking Invalid Cross-References..."
        self.progress = 58.3

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            results_list = []
            global passing_list
            write_content(5, 5, 5, 4)
            results_list.append(passing_list)
            write_content(6, 6, 6, 4)
            results_list.append(passing_list)
            write_content(7, 7, 7, 4)
            results_list.append(passing_list)
            self.signals.list.emit(results_list, 'invCrossRefCheckBox')

        else:
            # ESUs not linked to type 1 and 2 streets
            write_content(5, 5, 5, 4)
            # ESUs linked to type 3 and 4 but not to type 1 and 2
            write_content(6, 6, 6, 4)
            # ESUs linked to unofficial street types
            write_content(7, 7, 7, 4)


class CheckStartEnd(QRunnable):
    def __init__(self):
        super(CheckStartEnd, self).__init__()
        global tol
        self.tolerance = tol
        self.signals = GeneralSignals()
        self.task = "Checking start-end Coordinates..."
        self.progress = 58.3
        self.start_point = QgsPoint()
        self.end_point = QgsPoint()

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        global esu_layer
        # set the feature counter to 0
        count = 0
        # initialises two virtual objects points (start and end point)
        start_point = self.start_point
        end_point = self.end_point
        streets_model = QSqlQueryModel()
        streets_model.setQuery(queries[8])
        while streets_model.canFetchMore():
            streets_model.fetchMore()
        n_columns = streets_model.columnCount()
        n_rows = streets_model.rowCount()
        i = 0
        j = 0
        # first loop start (for each street):
        start_end_content = []
        while i <= n_rows - 1:
            start_ok = False
            end_ok = False
            col_info = []
            while j <= n_columns - 1:
                model_index = streets_model.createIndex(i, j)
                if j == 0:
                    data = model_index.data()
                    col_info.append(data)
                if j == 1:
                    data = model_index.data()
                    col_info.append(data)
                if j == 2:
                    data = model_index.data()
                    col_info.append(data)
                if j >= 3:
                    data = model_index.data()
                    col_info.append(data)
                j += 1
            usrn = col_info[0]
            ref_type = col_info[2]
            desc = col_info[1]
            start_point.set(float(col_info[3]), float(col_info[4]))
            end_point.set(float(col_info[5]), float(col_info[6]))
            # filter the layer "ESU Graphic" for the ESUs Ids returned from the list
            # deal just with the arcs part of multi arcs street
            esus_list = get_linked_esu_list(usrn)
            feat_filter = build_layer_filter(esus_list)
            feat_request = QgsFeatureRequest()
            feat_request.setFilterExpression(feat_filter)
            # second loop starts (for each arc (ESU) composing the street)
            # iterate through all filtered features and their proximity with the start and end of the street
            features = esu_layer.getFeatures(feat_request)
            # break the code here in two function the first will extract the features and
            # the second will print the data
            features.rewind()
            for feat in features:
                result = start_end_proximity(start_point, end_point, feat, self.tolerance)
                # both dist are ok
                if result == 3:
                    start_ok = True
                    end_ok = True
                # just end dist is ok
                elif result == 2:
                    end_ok = True
                # just start dist is ok
                elif result == 1:
                    start_ok = True
            # in case of problems
            if not start_ok or not end_ok:
                count += 1
                start_end_item = [str(col_info[0]) + ", "]
                # handles the creation of the report on a text file
                if not start_ok and not end_ok:
                    start_end_item.append("(both), ")
                if not start_ok and end_ok:
                    start_end_item.append("(start), ")
                if start_ok and not end_ok:
                    start_end_item.append("(end), ")
                start_end_item.append(str(ref_type) + ", ")
                start_end_item.append(str(desc) + "\n")
                start_end_content.append(start_end_item)
            j = 0
            i += 1
        if count == 0:
            tol_header = str(headers[8]).format(str(self.tolerance))
            if report_file is not None:
                write_header(tol_header, False, False)
                report_file.write("\n" + headers_no_items[8] + " \n \n \n")
            else:
                return
        else:
            # write header
            if report_file is not None:
                tol_header = str(headers[8]).format(str(self.tolerance))
                write_header(tol_header, False, False)
                k = 0
                # write column names
                while k <= len(column_names[5]) - 1:
                    if k == len(column_names[5]) - 1:
                        report_file.write(column_names[5][k] + "\n")
                    else:
                        report_file.write(column_names[5][k])
                    k += 1
                for content in start_end_content:
                    l = 0
                    while l <= len(content) - 1:
                        report_file.write(str(content[l]))
                        l += 1
                report_file.write("\n" + "TOTAL : " + str(count) + "\n \n \n")
            else:
                start_end_content.insert(0, column_names[5])
                global passing_list
                content_to_screen(content_list=start_end_content, query_model=None, columns_name_id=None,
                                         no_content_id=8)
                self.signals.list.emit(passing_list, 'startEndCheckBox')


class CheckTinyEsus(QRunnable):
    """
    runnable that checks for empty geometries and for features smaller than a set
    tolerance dimension expressed in metres
    :param type: string, indicates which layer is to check ("ESUS or polygons")
    :param tolerance: int, the tolerance
    :return:
    """

    def __init__(self, geom_type, tol):
        super(CheckTinyEsus, self).__init__()
        self.geom_type = geom_type
        self.tolerance = tol
        self.signals = GeneralSignals()
        self.task = "Checking tiny and empty geometries..."
        self.progress = [66.6, 95]

        # self.signals.result.emit(self.progress)
        self.check_layer = None
        self.field_name = None
        self.check_geom_dim = None
        self.empty_geoms = []
        self.tiny_shapes = []

    def run(self):
        global column_names
        global headers
        global headers_no_items
        if self.geom_type == "esu":
            self.signals.result.emit(self.task, self.progress[0])
            global esu_layer
            self.check_layer = esu_layer
            self.field_name = "esu_id"
        if self.geom_type == "rd_poly":
            self.signals.result.emit(self.task, self.progress[1])
            global poly_layer
            self.check_layer = poly_layer
            self.field_name = "rd_pol_id"
        if not self.check_layer:
            return
        else:
            # checks the field index exists
            fields = self.check_layer.pendingFields().toList()
            field_names_list = []
            for field in fields:
                field_names_list.append(field.name())
            if self.field_name not in field_names_list:
                return
            else:
                # loop through all features in the layer
                check_features = self.check_layer.getFeatures()
                check_features.rewind()
                # checks for empty geometries
                for check_feature in check_features:
                    check_geom = check_feature.geometry()
                    check_geom_id = check_feature[self.field_name]
                    if check_geom is None:
                        self.empty_geoms.append(check_geom_id)
                    elif not check_geom.isGeosValid():
                        self.empty_geoms.append(check_geom_id)
                    # check for feature dimensions smaller than tolerance
                    else:
                        if self.geom_type == 'esu':
                            self.check_geom_dim = check_geom.length()
                        if self.geom_type == 'rd_poly':
                            self.check_geom_dim = check_geom.area()
                        if self.check_geom_dim < self.tolerance:
                            self.tiny_shapes.append(check_geom_id)
            tiny_count = len(self.tiny_shapes)
            empty_count = len(self.empty_geoms)
            tiny_content = []
            empty_content = []
            check_list = []
            if self.geom_type == "esu":
                tiny_content.append(column_names[4])
                empty_content.append(column_names[4])
            if self.geom_type == "rd_poly":
                tiny_content.append(column_names[9])
                empty_content.append(column_names[9])
            if len(self.tiny_shapes) > 0:
                if report_file is not None:
                    write_header("\n" + str(headers[9]).format(self.geom_type))
                    report_file.write(str(tiny_content[0][0]) + "\n")
                    for shape in self.tiny_shapes:
                        report_file.write(str(shape) + "\n")
                    report_file.write(
                        "\nTOTAL OF TINY {0} : {1} \n".format((str(self.geom_type) + "s").upper(), str(tiny_count)) +
                        "\n \n \n")
                    report_file.flush()
                    os.fsync(report_file.fileno())
                if report_file is None:
                    # handles here screen report creation
                    for shape in self.tiny_shapes:
                        tiny_item = [str(shape)]
                        tiny_content.append(tiny_item)
                check_list.append(tiny_content)
                # return tiny_content
            # no problems with tiny shapes
            if len(self.tiny_shapes) == 0:
                if report_file is not None:
                    report_file.write("\n" + str(headers_no_items[9]).format(self.geom_type) + " \n \n \n")
                    report_file.flush()
                    os.fsync(report_file.fileno())
                if report_file is None:
                    last_item = []
                    tiny_content.append(last_item)
                    last_item.append(str(headers_no_items[9].format(self.geom_type)))
                    # handles here screen report creation
                    # return tiny_content
                    check_list.append(tiny_content)
            # if there are any problems with empty geometries
            if len(self.empty_geoms) > 0:
                if report_file is not None:
                    write_header(str(headers[10]))
                    report_file.write(str(empty_content[0][0]) + "\n")
                    for empty in self.empty_geoms:
                        report_file.write(str(empty) + "\n")
                    report_file.write("\nTOTAL OF EMPTY GEOMETRIES: {0}".format(str(empty_count)))
                    report_file.write("\n \n \n \n")
                    report_file.flush()
                    os.fsync(report_file.fileno())
                if report_file is None:
                    # handles here the screen report
                    for empty in self.empty_geoms:
                        empty_item = [str(empty)]
                        empty_content.append(empty_item)
                    check_list.append(empty_content)
            if len(self.empty_geoms) == 0:
                if report_file is not None:
                    report_file.write("\n" + str(headers_no_items[10]) + " \n \n \n \n")
                    report_file.flush()
                    os.fsync(report_file.fileno())
                    return
                if report_file is None:
                    # handles here the screen report
                    last_item = []
                    empty_content.append(last_item)
                    last_item.append(str(headers_no_items[10].format(self.geom_type)))
                    check_list.append(empty_content)
        if report_file is None:
            if self.geom_type == 'esu':
                self.signals.list.emit(check_list, 'tinyEsuCheckBox')
            if self.geom_type == 'rd_poly':
                self.signals.list.emit(check_list,'tinyPolysCheckBox')

    @staticmethod
    def _write_to_report_file(open_report_file, text):
        """
        Print text to the report file.  This function is useful for debugging.
        :param open_report_file: Open report file object
        :param text: text to write
        """
        if open_report_file is None:
            raise Exception('Report file not accessible')

        open_report_file.write(text)
        open_report_file.flush()
        os.fsync(open_report_file.fileno())


class CheckMaintReins(QRunnable):
    """
    groups two checks for streets type 1 and 2, checks streets that
    are not linked to maintenance records and check streets that are not
    linked to reinstatement records
    :return: void if the report is to text
            list[[string]x2] if the report is to screen
    """

    def __init__(self):
        super(CheckMaintReins, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking maintenance records for streets..."
        self.progress = 75

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            global passing_list
            results_list = []
            write_content(10, 11, 11, 6)
            results_list.append(passing_list)
            write_content(11, 12, 12, 6)
            results_list.append(passing_list)
            self.signals.list.emit(results_list,'notMaintReinsCheckBox')
        else:
            # check for maintenance
            write_content(10, 11, 11, 6)
            # check for reinstatement
            write_content(11, 12, 12, 6)


class CheckAsdCoords(QRunnable):
    """
    groups three checks on start and end coordinates for streets classified as
    maintenance, reinstatement and special designation
    :return: void if the report is to text
            list[[string]x3] if the report is to screen
    """

    def __init__(self):
        super(CheckAsdCoords, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking streets start/end coords..."
        # change progression value
        self.progress = 80

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            global passing_list
            results_list = []
            write_content(12, 13, 13, 7)
            results_list.append(passing_list)
            write_content(13, 14, 14, 7)
            results_list.append(passing_list)
            write_content(14, 15, 15, 7)
            results_list.append(passing_list)
            self.signals.list.emit(results_list, 'asdStartEndCheckBox')
        else:
            # check for maintenance
            write_content(12, 13, 13, 7)
            # check for reinstatement
            write_content(13, 14, 14, 7)
            # check for special designation
            write_content(14, 15, 15, 7)


class MaintNoPoly(QRunnable):
    """
    runnable that checks maintenance record that have no link to
    road polygons
    """
    def __init__(self):
        super(MaintNoPoly, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking maintenance records for polygons..."
        self.progress = 85

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            global passing_list
            write_content(15, 16, 16, 8)
            self.signals.list.emit(passing_list, 'notMaintPolysCheckBox')
        else:
            write_content(15, 16, 16, 8)


class PolyNoMaint(QRunnable):
    """
    group of two checks on road polygons
    1: polygons that have not link to maintenance records
    2: polygons wrongly assigned to more than one maintenance record
    :return: void
    """

    def __init__(self):
        super(PolyNoMaint, self).__init__()
        self.signals = GeneralSignals()
        self.task = "Checking maintenance records for polygons..."
        self.progress = 90

    def run(self):
        self.signals.result.emit(self.task, self.progress)
        if report_file is None:
            global passing_list
            results_list = []
            write_content(16, 17, 17, 9)
            results_list.append(passing_list)
            write_content(17, 18, 18, 10)
            results_list.append(passing_list)
            self.signals.list.emit(results_list, 'notPolysMaintCheckBox')
        else:
            # polygons that have not link to maintenance records
            write_content(16, 17, 17, 9)
            # polygons wrongly assigned to more than one maintenance record
            write_content(17, 18, 18, 10)


class GeneralSignals(QObject):
    result = pyqtSignal(str, int)
    report_finished = pyqtSignal()
    task_started = pyqtSignal()
    task_finished = pyqtSignal()
    list = pyqtSignal(list, str)


class InitGlobals:
    """
    this class is called before the execution of every thread to initialise the static elements
    of the report (queries, headers and text)
    """

    def __init__(self, db_con, params, tolerance=None):
        # initialises tolerance if exists
        global tol
        tol = tolerance
        # initialises db connection
        global db
        db = db_con
        # initialises plug-in params from xml
        # params = params
        # global org_name
        # org_name = params["OrgName"]
        global user
        user = params["UserName"]
        # initialises layers
        global esu_layer
        esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
        global poly_layer
        poly_layer = QgsMapLayerRegistry.instance().mapLayersByName('Road Polygons')[0]
        # initialises db queries
        global queries
        queries = {

            0: "SELECT (ifnull(tblSTREET.Description, '') ||', '|| ifnull(tlkpLOCALITY.Name, '')||', '|| "
               "ifnull(tlkpTOWN.Name,'')) AS DuplicateRoads FROM (tblSTREET INNER JOIN tlkpLOCALITY "
               "ON tblSTREET.Loc_Ref = tlkpLOCALITY.Loc_Ref) INNER JOIN tlkpTOWN "
               "ON tblSTREET.Town_Ref = tlkpTOWN.Town_Ref GROUP BY tblSTREET.Currency_flag, "
               "tblSTREET.Description, tlkpLOCALITY.Name, tlkpTOWN.Name HAVING (((Count(tblSTREET.USRN))>1) "
               "AND ((tblSTREET.Currency_flag)=0))",

            1: "SELECT (ifnull(tblSTREET.USRN, '') ||', '|| ifnull(tblSTREET.Version_No, '') ||', '|| "
               "ifnull(tblSTREET.Street_ref_type, '') ||', '|| ifnull(tblSTREET.Description, '')||', '|| "
               "ifnull(tblSTREET.Update_date, '') ||', '|| ifnull(tblSTREET.Updated_by, '')) AS not_linked_usrn "
               "FROM tblSTREET LEFT JOIN (SELECT * from lnkESU_STREET where lnkESU_Street.Currency_Flag = 0) "
               "AS STREET_LINK ON (tblSTREET.Version_No = STREET_LINK.usrn_version_no) "
               "AND (tblSTREET.USRN = STREET_LINK.usrn) WHERE (((tblSTREET.Currency_flag) = 0) "
               "AND ((STREET_LINK.usrn) Is Null)) ORDER BY tblSTREET.USRN ",

            2: "SELECT (ifnull(q12.esu_id,'') ||', '|| ifnull(q12.street_ref_type,'') ||', '|| "
               "ifnull(q12.USRN,'') ||', '|| ifnull(q12.Description,'')) "
                "AS type3_not_linked "
                "FROM (SELECT DISTINCT lnkESU_STREET.esu_id, "
               "tblSTREET.Street_ref_type, tblStreet.Description,tblStreet.USRN "
                "FROM (lnkESU_STREET INNER JOIN tblSTREET "
                "ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
                "AND (lnkESU_STREET.usrn = tblSTREET.USRN)) "
                "INNER JOIN tblMAINT "
                "ON (tblSTREET.USRN = tblMAINT.USRN) "
                "WHERE (((tblSTREET.street_ref_type = 1) "
                "OR (tblSTREET.street_ref_type = 2)) "
                "AND (lnkESU_STREET.Currency_flag = 0) AND (tblSTREET.Currency_flag = 0) "
                "AND (tblMAINT.Road_Status_Ref = 1)) "
                "ORDER BY lnkESU_STREET.esu_id) "
                "AS q12 "
                "LEFT JOIN (SELECT lnkESU_STREET.esu_id, tblSTREET.Street_ref_type "
                "FROM lnkESU_STREET INNER JOIN tblSTREET "
                "ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
                "AND (lnkESU_STREET.usrn = tblSTREET.USRN) "
                "WHERE ((tblSTREET.street_ref_type = 3) "
                "AND (lnkESU_STREET.Currency_flag = 0) AND (tblSTREET.Currency_flag = 0)) "
                "ORDER BY lnkESU_STREET.esu_id) AS q3 ON q12.esu_id = q3.esu_id WHERE (q3.esu_id IS Null)",

            3: "SELECT (ifnull(qryID.esu_id,'') ||', '|| ifnull(qryID.esuxy,'')) as dup_esu_ref FROM "
               "(SELECT Count(tblESU.esu_id) AS CountOfesu_id, "
               "((substr('0000000'|| xref, -7,7) || substr('0000000'||yref, -7,7))) AS esuxy "
               " FROM tblESU WHERE tblESU.currency_flag=0 GROUP BY tblESU.currency_flag, "
               "(substr('0000000'|| xref, -7, 7) || substr('0000000'||yref, -7,7))) qryCntID "
               " INNER JOIN (SELECT tblESU.esu_id, (substr('0000000'|| xref, -7, 7) || substr('0000000'||yref, -7,7))"
               " AS esuxy From tblESU WHERE (tblESU.currency_flag=0)) qryID "
               "ON qryCntID.esuxy = qryID.esuxy WHERE (qryCntID.CountOfesu_id>1)",

            4: " SELECT tblESU.esu_id AS esu_not_linked "
               "FROM tblESU LEFT JOIN "
               "((SELECT lnkESU_STREET.* From lnkESU_STREET WHERE (((lnkESU_STREET.currency_flag)=0)))) "
               "AS STREET_LINK ON (tblESU.version_no = STREET_LINK.esu_version_no) "
               "AND (tblESU.esu_id = STREET_LINK.esu_id) "
               "WHERE (((tblESU.currency_flag)=0) AND ((STREET_LINK.usrn) Is Null))",

            5: "SELECT * FROM (SELECT DISTINCT esu_id, count(USRN) AS USRN_Count "
               "FROM (SELECT lnkESU_Street.esu_id,tblStreet.USRN "
               "FROM tblSTREET INNER JOIN lnkESU_STREET ON (tblSTREET.USRN = lnkESU_STREET.usrn) "
               "AND (tblSTREET.Version_No = lnkESU_STREET.usrn_version_no) "
               "WHERE (((tblSTREET.Street_ref_type)=1 Or (tblSTREET.Street_ref_type)=2) "
               "AND ((tblSTREET.Currency_flag)=0) AND ((lnkESU_STREET.currency_flag)=0))) AS sq "
               "GROUP BY esu_id) WHERE USRN_Count > 1",

            6: "SELECT q34.esu_id as ESUID "
               "FROM (SELECT lnkESU_STREET.esu_id, tblSTREET.Street_ref_type "
               "FROM lnkESU_STREET INNER JOIN tblSTREET ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
               "AND (lnkESU_STREET.usrn = tblSTREET.USRN) "
               "WHERE (((tblSTREET.street_ref_type) = 3 OR (tblSTREET.street_ref_type) = 4) "
               "AND ((lnkESU_STREET.Currency_flag) = 0) And ((tblSTREET.Currency_flag) = 0)) "
               "ORDER BY lnkESU_STREET.esu_id) as q34 "
               "LEFT JOIN (SELECT lnkESU_STREET.esu_id, tblSTREET.Street_ref_type "
               "FROM lnkESU_STREET INNER JOIN tblSTREET ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
               "AND (lnkESU_STREET.usrn = tblSTREET.USRN) "
               "WHERE (((tblSTREET.street_ref_type) = 1 Or (tblSTREET.street_ref_type) = 2) "
               "AND ((lnkESU_STREET.Currency_flag) = 0) AND ((tblSTREET.Currency_flag) = 0)) "
               "ORDER BY lnkESU_STREET.esu_id) as q12 ON q34.esu_id = q12.esu_id WHERE (((q12.esu_id) Is Null))",

            7: "SELECT lnkESU_STREET.esu_id as ESUID, tblSTREET.USRN as USRN, tblSTREET.Street_ref_type as REFTYPE "
               "FROM lnkESU_STREET INNER JOIN tblSTREET ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
               "AND (lnkESU_STREET.usrn = tblSTREET.USRN) "
               "WHERE (((tblSTREET.Street_ref_type) Not In (1,2,3,4)) "
               "AND ((lnkESU_STREET.currency_flag)=0) "
               "AND ((tblSTREET.Currency_flag)=0)) "
               "ORDER BY lnkESU_STREET.esu_id",

            8: "SELECT DISTINCT tblStreet.USRN, tblStreet.Description, "
               "tblStreet.Street_ref_type, ifnull(tblStreet.Start_xref, 0), "
               "ifnull(tblStreet.Start_yref, 0), ifnull(tblStreet.End_xref, 0), ifnull(tblStreet.End_yref, 0) "
               "FROM tblStreet LEFT JOIN lnkESU_STREET ON (tblStreet.USRN = lnkESU_STREET.usrn) "
               "AND (tblStreet.Version_No = lnkESU_STREET.usrn_version_no) "
               "WHERE (((lnkESU_STREET.usrn) Is Not Null) AND ((tblStreet.Currency_flag)=0) "
               "AND ((lnkESU_STREET.currency_flag)=0)) "
               "ORDER BY tblStreet.USRN;",

            9: "SELECT lnkESU_STREET.esu_id "
               "From lnkESU_STREET "
               " WHERE (((lnkESU_STREET.usrn)= {0}) "
               " AND ((lnkESU_STREET.currency_flag)=0))",

            10: "SELECT (ifnull(tblSTREET.USRN,'') ||', '|| ifnull(tblSTREET.Street_ref_type,'') ||', '|| "
                "ifnull(tblSTREET.Description,'')) AS type12_maint "
                "FROM tblSTREET LEFT JOIN (SELECT tblMAINT.USRN, tblMAINT.Maint_id "
                "FROM tblMAINT WHERE (((tblMAINT.Currency_flag)=0))) as maint ON tblSTREET.USRN = maint.USRN "
                "WHERE (((tblSTREET.street_ref_type) = 1 Or (tblSTREET.street_ref_type) = 2) "
                "AND ((tblSTREET.Currency_flag) = 0) And ((maint.maint_id) Is Null)) "
                "ORDER BY tblSTREET.USRN",

            11: "SELECT (ifnull(tblSTREET.USRN,'') ||', '|| ifnull(tblSTREET.Street_ref_type,'') "
                "||', '|| ifnull(tblSTREET.Description,'')) AS check_reins "
                "FROM tblSTREET LEFT JOIN (SELECT tblReins_Cat.USRN, tblReins_Cat.Reins_cat_id FROM tblReins_Cat "
                "WHERE (((tblReins_Cat.Currency_flag)=0))) as reins ON tblSTREET.USRN = reins.USRN "
                "WHERE (((tblSTREET.street_ref_type) = 1 Or (tblSTREET.street_ref_type) = 2) "
                "AND ((tblSTREET.Currency_flag) = 0) And ((reins.Reins_cat_id) Is Null)) "
                "AND tblStreet.USRN not in (Select distinct s.USRN "
                "FROM tblStreet s inner join tblMaint m on m.USRN = s.USRN WHERE s.Currency_flag = 0 "
                "AND m.currency_flag = 0 and m.road_status_ref = 4) "
                "ORDER BY tblSTREET.USRN",

            12: "SELECT (ifnull(S.USRN,'') ||', '||ifnull(ASD.Maint_ID,'') ||', '|| ifnull(ASD.Reference_No,'')) "
                "as inv_maint FROM tblMaint ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 AND ((ASD.start_xref = 0 "
                "or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            13: "SELECT (ifnull(S.USRN,'') ||', '|| ifnull(ASD.Reins_Cat_Id,'') ||', '|| ifnull(ASD.Reference_No,'')) "
                "AS inv_reins FROM tblReins_Cat ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 "
                "AND ((ASD.start_xref = 0 or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            14: "SELECT (ifnull(S.USRN,'') ||', '|| ifnull(ASD.Spec_Des_ID,'') ||', '|| ifnull(ASD.Reference_No,'')) "
                "AS inv_spec_des FROM tblSpec_Des ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 "
                "AND ((ASD.start_xref = 0 or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            15: "SELECT (ifnull(tblMAINT.USRN,'') ||', '|| ifnull(tblMAINT.Maint_id, '') ||', '|| "
                "ifnull(tlkpROAD_STATUS.Description, '')) as road_status "
                "FROM (tblMAINT LEFT JOIN lnkMAINT_RD_POL ON tblMAINT.Maint_id = lnkMAINT_RD_POL.maint_id) "
                "INNER JOIN tlkpROAD_STATUS ON tblMAINT.Road_status_ref = tlkpROAD_STATUS.Road_status_ref "
                "WHERE (((tblMAINT.Currency_flag) = 0) And ((lnkMAINT_RD_POL.rd_pol_id) Is Null)) "
                "ORDER BY tblMAINT.USRN",

            16: "SELECT rdpoly.RD_POL_ID FROM rdpoly "
                "LEFT JOIN (select * from lnkMaint_RD_POL WHERE currency_flag = 0) "
                "AS mrp ON rdpoly.RD_POL_ID = mrp.rd_pol_id WHERE (((mrp.Maint_ID) Is Null)) ORDER BY rdpoly.RD_POL_ID",

            17: "SELECT (ifnull(mp.rd_pol_id,'') ||', '|| ifnull(tblMAINT.USRN,'') ||', '|| "
                "ifnull(tblMAINT.Maint_id,'')) AS check_polys "
                "FROM (SELECT lnkMAINT_RD_POL.rd_pol_id, Count(lnkMAINT_RD_POL.maint_id) AS CountOfmaint_id "
                "From lnkMAINT_RD_POL "
                "GROUP BY lnkMAINT_RD_POL.rd_pol_id, lnkMAINT_RD_POL.currency_flag "
                "HAVING (((Count(lnkMAINT_RD_POL.maint_id))>1) AND ((lnkMAINT_RD_POL.currency_flag)=0))) as mp "
                "INNER JOIN (lnkMAINT_RD_POL INNER JOIN tblMAINT ON lnkMAINT_RD_POL.maint_id = tblMAINT.Maint_id) "
                "ON mp.rd_pol_id = lnkMAINT_RD_POL.rd_pol_id "
                "Where (((lnkMAINT_RD_POL.Currency_flag) = 0) And ((tblMAINT.Currency_flag) = 0)) "
                "ORDER BY mp.rd_pol_id, tblMAINT.USRN;"
        }

        global headers
        # initialises the text of headers and column names to use in the report
        headers = {0: 'Duplicate street descriptions :',
                   1: 'Streets not linked to ESUs :',
                   2: ['ESUs linked to Public Type 1 or 2 Streets but not to Type 3 :', '(Including Footpaths)',
                       'NOTE : Some of these esus may be linked to private parts '
                       'of streets that are part public and part private'],
                   3: ['Duplicate ESU References : ',
                       'The following ESUs have duplicate ESU references. '
                       'It is important that these are unique values \n'
                       'These references are based on the esu midpoint and are used when exporting to DTF'],
                   4: 'ESUs not linked to Streets :',
                   5: 'ESUs incorrectly linked to Type 1 and Type 2 Streets :',
                   6: 'ESUs linked to Type 3 or 4 Streets but not to Type 1 or 2 :',
                   7: 'ESUs linked to Unofficial street types (ie. not 1,2,3 or 4) :',
                   8: 'Streets with Start / End coordinates more than {0}m from ESUs :',
                   9: 'IDs of tiny {0}s :',
                   10: 'IDs of empty geometries :',
                   11: 'Type 1/2 Streets not linked to Maintenance Records :',
                   12: 'Type 1/2 Streets not linked to Reinstatement Records :',
                   13: 'Maintenance Records With Invalid Start-End Co-ordinates',
                   14: 'Reinstatement Records With Invalid Start-End Co-ordinates',
                   15: 'Special Designation Records With Invalid Start-End Co-ordinates',
                   16: 'Maintenance Records not linked to any Polygons :',
                   17: 'Polygons not linked to a Maintenance Record :',
                   18: 'Polygons wrongly assigned to more than one Maintenance record :'}

        global headers_no_items
        headers_no_items = {0: 'No duplicate street descriptions.',
                            1: 'No Unreferenced Streets found.',
                            2: 'No ESUs linked to Public Type 1 or 2 Streets but not to Type 3.',
                            3: 'No Duplicate ESU References found.',
                            4: 'No Unreferenced ESUs found.',
                            5: 'No ESUs incorrectly linked to Type 1 & 2 Streets.',
                            6: 'No ESUs incorrectly linked to Type 3 or 4 Streets but not 1 or 2.',
                            7: 'No ESUs incorrectly linked to Unofficial street types.',
                            8: 'No problems found.',
                            9: 'No tiny {0}s found.',
                            10: 'No invalid geometries found.',
                            11: 'No Type 1/2 Streets Without Maintenance Records.',
                            12: 'No Type 1/2 Streets Without Reinstatement Records.',
                            13: 'No Maintenance Records With Invalid Start-End Co-ordinates.',
                            14: 'No Reinstatement Records With Invalid Start-End Co-ordinates.',
                            15: 'No Special Designation Records With Invalid Start-End Co-ordinates.',
                            16: 'No Maintenance Records without polygons found.',
                            17: 'No polygons without Maintenance Records found.',
                            18: 'No Polygons wrongly assigned to more than one Maintenance record.'}
        global column_names
        column_names = {0: ['Description, Locality, Town'],
                        1: ['USRN, Version, Type, Description, Update_Date, Updated_By'],
                        2: ['ESU_ID, Street Reference Type ,USRN, Street Description'],
                        3: ['ESU_ID, ESU Reference (External)'],
                        4: ['ESU_ID'],
                        5: ['USRN, Start/End, Type, Description'],
                        6: ['USRN, Type, Description'],
                        7: ['USRN, ASD ID, ReferenceNo'],
                        8: ['USRN, MaintID, Status'],
                        9: ['PolyID'],
                        10: ['PolyID, USRN, MaintID']}
