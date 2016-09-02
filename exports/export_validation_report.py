# -*- coding: utf-8 -*-
from math import sqrt

from PyQt4.QtSql import QSqlQueryModel
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox, QProgressDialog

from qgis.core import QgsMapLayerRegistry, QgsPoint, QgsFeatureRequest

from Roadnet.generic_functions import ipdb_breakpoint

__author__ = 'Alessandro Cristofori'


class ExportValidationReport:
    """
    Control the overall process of exporting validation reports to text file
    from the validation report form on the admin menu
    """

    def __init__(self, report_title, org_name, db, iface, file_path=None):
        self.report_title = report_title.upper()
        self.db = db
        self.iface = iface
        self.org_name = org_name.upper()
        self.user = "test_user"
        self.file_path = file_path
        self.report_file = None
        self.start_point = QgsPoint()
        self.end_point = QgsPoint()
        self.esu_layer = QgsMapLayerRegistry.instance().mapLayersByName('ESU Graphic')[0]
        self.poly_layer = QgsMapLayerRegistry.instance().mapLayersByName('Road Polygons')[0]
        self.filter = None
        self.queries = {}
        self.headers = {}
        self.headers_no_items = {}
        self.column_names = {}
        self.init_headers()
        self.init_queries()
        self.validation_dia = None
        self.progress_win = None
        self.progress_win = QProgressDialog("", None, 0, 13, self.validation_dia)
        self.progress_win.setFixedSize(380, 100)
        self.progress_win.setModal(True)
        self.progress_win.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.progress_win.setWindowTitle("Export Validation Report")

    def init_headers(self):
        # initialises the text of headers and column names to use in the report
        self.headers = {0: 'Duplicate street descriptions :',
                        1: 'Streets not linked to ESUs :',
                        2: ['ESUs linked to Public Type 1 or 2 Streets but not to Type 3 :', '(Including Footpaths)',
                            'NOTE : Some of these esus may be linked to private parts '
                            'of streets that are part public and part private'],
                        3: ['Duplicate ESU References : ',
                            'The following ESUs have duplicate ESU references. '
                            'It is important that these are unique values \n' \
                            'These references are based on the esu midpoint and are used when exporting to DTF'],
                        4: 'ESUs not linked to Streets :',
                        5: 'ESUs incorrectly linked to Type 1 and Type 2 Streets :',
                        6: 'ESUs linked to Type 3 or 4 Streets but not to Type 1 or 2 :',
                        7: 'ESUs linked to Unofficial street types (ie. not 1,2,3 or 4) :',
                        8: 'Streets with Start / End coordinates more than {0}m from ESUs :',
                        9: 'IDs of tiny {0}s :',
                        10: 'IDs of emtpy geometries :',
                        11: 'Type 1/2 Streets not linked to Maintenance Records :',
                        12: 'Type 1/2 Streets not linked to Reinstatement Records :',
                        13: 'Maintenance Records With Invalid Start-End Co-ordinates',
                        14: 'Reinstatement Records With Invalid Start-End Co-ordinates',
                        15: 'Special Designation Records With Invalid Start-End Co-ordinates',
                        16: 'Maintenance Records not linked to any Polygons :',
                        17: 'Polygons not linked to a Maintenance Record :',
                        18: 'Polygons wrongly assigned to more than one Maintenance record :'}

        self.headers_no_items = {0: 'No duplicate street descriptions.',
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

        self.column_names = {0: ['Description, Locality, Town'],
                             1: ['USRN, Version, Type, Description, Update Date, Updated By'],
                             2: ['ESU ID, Street Reference Type, USRN, Street Description'],
                             3: ['ESU ID, ESU Reference (External)'],
                             4: ['ESU ID'],
                             5: ['USRN, Start/End, Type, Description'],
                             6: ['USRN, Type, Description'],
                             7: ['USRN, ASD ID, Reference Number'],
                             8: ['USRN, Maintenance ID, Status'],
                             9: ['Polygon ID'],
                             10: ['Polygon ID, USRN, Maintenance ID']}

    def write_content(self, query_id, header_id, header_no_content_id, columns_name_id, include_footpaths=True,
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
        # build a query model object
        query_model = QSqlQueryModel()
        if not include_footpaths:
            filtered_query = self.queries[2].replace("AND (lnkESU_STREET.Currency_flag = 0)",
                                                     "AND (lnkESU_STREET.Currency_flag = 0) AND "
                                                     "(tblStreet.Description not like '%Footpath%')")
            query_model.setQuery(filtered_query)
        else:
            query_model.setQuery(self.queries[query_id])
        while query_model.canFetchMore():
            query_model.fetchMore()
        parent_model_index = QModelIndex()
        # if the path is not specified sends data to function creating a list
        if self.file_path is None:
            assert isinstance(columns_name_id, object)
            items_list = self.content_to_screen(content_list=None, query_model=query_model,
                                                columns_name_id=columns_name_id, no_content_id=header_no_content_id)
            return items_list

    def start_report(self):
        self.progress_win.show()
        self.progress_win.setLabelText("Starting report")
        self.progress_win.setValue(1)

    def dup_street_desc(self):
        """
        duplicate street description report section creation
        :return: void if the report is to text
                list[string] if the report is to screen
        """
        # self.progress_win.show()
        self.progress_win.setLabelText("Checking duplicate street descriptions...")
        items_list = self.write_content(0, 0, 0, 0)
        self.progress_win.setValue(1)
        return items_list

    def street_not_esu_desc(self):
        """
        streets not linked to ESU report section creation
        :return: void if the report is to text
                list[string] if the report is to screen
        """
        self.progress_win.setLabelText("Checking streets not linked to ESUs...")
        items_list = self.write_content(1, 1, 1, 1)
        self.progress_win.setValue(2)
        return items_list

    def no_type3_desc(self, include_footpath):
        """
        streets not connected to type 3 report section
        :param include_footpath: bool, include or not footpath in the query
        :return: void if the report is to text
                list[string] if the report is to screen
        """
        if include_footpath:
            self.progress_win.setLabelText("Checking ESUs linked to Public Type 1 or 2 Streets but not to Type 3 "
                                           "(Including Footpaths)...")
            items_list = self.write_content(2, 2, 2, 2)
            self.progress_win.setValue(3)
            return items_list
        else:
            self.progress_win.setLabelText("Checking ESUs linked to Public Type 1 or 2 Streets but not to Type 3...")
            items_list = self.write_content(2, 2, 2, 2, False)
            self.progress_win.setValue(3)
            return items_list

    def dup_esu_ref(self):
        """
        duplicate ESU references report section
        :param include_subtitle: include or not a header subtitle
        :return: void if the report is to text
                list[string] if the report is to screen, the subtitile is
                included by default
        """
        self.progress_win.setLabelText("Checking Duplicate ESU References...")
        items_list = self.write_content(3, 3, 3, 3)
        self.progress_win.setValue(4)
        return items_list

    def no_link_esu_streets(self):
        """
        section report on ESUs not linked to any street
        :return:void if the report is to text
                list[string] if the report is to screen, the subtitile is
                not included by default
        """
        self.progress_win.setLabelText("Checking ESUs not linked to Streets...")
        items_list = self.write_content(4, 4, 4, 4)
        self.progress_win.setValue(5)
        return items_list

    def invalid_cross_references(self):
        """
        this function handles three checks that are grouped
        under the same checkbox in the form 'invalid cross references'
        first check: ESUs not linked to type 1 and 2 streets
        second check: ESUs linked to type 3 and 4 streets but not linked to type 1 or 2
        third check: ESUs linked to unofficial street types (none of the previous type)
        :return void if the report is to text
                list[[string]x3] if the report is to screen
        """
        self.progress_win.setLabelText("Checking Invalid Cross-References...")
        results_list = []
        esu12_list = self.write_content(5, 5, 5, 4)
        esu34_list = self.write_content(6, 6, 6, 4)
        unoff_list = self.write_content(7, 7, 7, 4)
        results_list.append(esu12_list)
        results_list.append(esu34_list)
        results_list.append(unoff_list)
        self.progress_win.setValue(6)
        return results_list

    def check_start_end(self, tol):
        # set the feature counter to 0
        count = 0
        # initialises two virtual objects points (start and end point)
        start_point = self.start_point
        end_point = self.end_point
        # uses the qgis python api to access the ESU Graphic Layer
        esu_layer = self.esu_layer
        # runs the query number 8 to retrieve all streets from the Database
        streets_model = QSqlQueryModel()
        streets_model.setQuery(self.queries[8])
        while streets_model.canFetchMore():
            streets_model.fetchMore()
        n_columns = streets_model.columnCount()
        n_rows = streets_model.rowCount()
        i = 0
        j = 0
        # first loop start (for each street):
        start_end_content = []
        while i <= n_rows - 1:
            self.progress_win.setLabelText("Checking start-end Coordinates...")
            # initialises the state of the checks booleans both to false
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
            esus_list = self.get_linked_esu_list(usrn)
            feat_filter = self.build_layer_filter(esus_list)
            feat_request = QgsFeatureRequest()
            feat_request.setFilterExpression(feat_filter)
            # second loop starts (for each arc (ESU) composing the street)
            # iterate through all filtered features and their proximity with the start and end of the street
            features = self.esu_layer.getFeatures(feat_request)
            features.rewind()
            # iterates through features
            for feat in features:
                # check start end points for each of the only if none of the start end points of
                # a ESU on each street is not already matched
                if (start_ok is not True) or (end_ok is not True):
                    result = self.start_end_proximity(start_point, end_point, feat, tol)
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
                else:
                    break
            # in case of problems
            if not start_ok or not end_ok:
                count += 1
                start_end_item = [str(col_info[0]) + ","]
                # handles the creation of the report on a text file
                if not start_ok and not end_ok:
                    start_end_item.append("(both),")
                if not start_ok and end_ok:
                    start_end_item.append("(start),")
                if start_ok and not end_ok:
                    start_end_item.append("(end),")
                start_end_item.append(str(ref_type) + ",")
                start_end_item.append(str(desc) + "\n")
                start_end_content.append(start_end_item)
            j = 0
            i += 1
        if count == 0:
            self.progress_win.setValue(7)
            return
        else:
            start_end_content.insert(0, self.column_names[5])
            self.progress_win.setValue(7)
            return self.content_to_screen(content_list=start_end_content, query_model=None, columns_name_id=None,
                                          no_content_id=8)

    def start_end_proximity(self, start_point_street, end_point_street, feature, tolerance):
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

    def get_linked_esu_list(self, usrn):
        """
        function that selects all esus for a determined street
        :param usrn: the unique identifier of a certain street
        :return: list[esu_ids] all esu ids linked to a certain street or
        void in case a street does not have any linked esu
        """
        # executing the query
        esus_query_model = QSqlQueryModel()
        esus_query_model.setQuery(self.queries[9].format(usrn))
        while esus_query_model.canFetchMore():
            esus_query_model.fetchMore()
        n_rows = esus_query_model.rowCount()
        # skip if no esus are linked
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

    def build_layer_filter(self, esus_list):
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

    def check_tiny_esus(self, type, tolerance):
        """
        function that checks for empty geometries and for features smaller than a set
        tolerance dimension expressed in metres
        :param type: string, indicates which layer is to check ("ESUS or polygons")
        :param tolerance: int, the tolerance
        :return:
        """
        check_layer = None
        field_name = None
        check_geom = None
        check_geom_dim = None
        empty_geoms = []
        tiny_shapes = []
        if type == "esu":
            # self.progress_win.setLabelText("Checking tiny and empty ESUs geometries...")
            check_layer = self.esu_layer
            field_name = "esu_id"
            # self.progress_win.setValue(8)
        if type == "rd_poly":
            # self.progress_win.setLabelText("Checking tiny and empty polygons geometries...")
            check_layer = self.poly_layer
            field_name = "rd_pol_id"
            # self.progress_win.setValue(13)
        if not check_layer:
            no_layer_msg_box = QMessageBox(QMessageBox.Warning, " ", "Cannot retrieve {} Layer".format(type),
                                           QMessageBox.Ok, None)
            no_layer_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            no_layer_msg_box.exec_()
            return
        else:
            # checks the field index exists
            fields = check_layer.pendingFields().toList()
            field_names_list = []
            for field in fields:
                field_names_list.append(field.name())
            if field_name not in field_names_list:
                no_field_msg_box = QMessageBox(QMessageBox.Warning, " ",
                                               "Cannot find field named {}".format(field_name),
                                               QMessageBox.Ok, None)
                no_field_msg_box.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                no_field_msg_box.exec_()
                return
            else:
                # loop through all features in the layer
                check_features = check_layer.getFeatures()
                check_features.rewind()
                # checks for empty geometries
                for check_feature in check_features:
                    check_geom = check_feature.geometry()
                    check_geom_id = check_feature[field_name]
                    if check_geom is None:
                        empty_geoms.append(check_geom_id)
                    elif not check_geom.isGeosValid():
                        empty_geoms.append(check_geom_id)
                    # check for feature dimensions smaller than tolerance
                    else:
                        if type == 'esu':
                            check_geom_dim = check_geom.length()
                        if type == 'rd_poly':
                            check_geom_dim = check_geom.area()
                        if check_geom_dim < tolerance:
                            tiny_shapes.append(check_geom_id)
            tiny_content = []
            empty_content = []
            check_list = []
            if type == "esu":
                tiny_content.append(self.column_names[4])
                empty_content.append(self.column_names[4])
            if type == "rd_poly":
                tiny_content.append(self.column_names[9])
                empty_content.append(self.column_names[9])
            # if there are any problems with tiny shapes
            if len(tiny_shapes) > 0:
                for shape in tiny_shapes:
                    tiny_item = [str(shape)]
                    tiny_content.append(tiny_item)
                check_list.append(tiny_content)
            if len(tiny_shapes) == 0:
                last_item = []
                tiny_content.append(last_item)
                last_item.append(str(self.headers_no_items[9].format(type)))
                # return tiny_content
                check_list.append(tiny_content)
            # if there are any problems with empty geometries
            if len(empty_geoms) > 0:
                for empty in empty_geoms:
                    empty_item = [str(empty)]
                    empty_content.append(empty_item)
                check_list.append(empty_content)
            if len(empty_geoms) == 0:
                last_item = []
                empty_content.append(last_item)
                last_item.append(str(self.headers_no_items[10].format(type)))
                check_list.append(empty_content)
        return check_list

    def check_maint_reinst(self):
        """
        groups two checks for streets type 1 and 2, checks streets that
        are not linked to maintenance records and check streets that are not
        linked to reinstatement records
        :return: void if the report is to text
                list[[string]x2] if the report is to screen
        """
        # self.progress_win.setLabelText("Checking maintenance records for streets...")
        if self.file_path is None:
            results_list = [self.write_content(10, 11, 11, 6), self.write_content(11, 12, 12, 6)]
            self.progress_win.setValue(9)
            return results_list

    def check_asd_coords(self):
        """
        groups three checks on start and end coordinates for streets classified as
        maintenance, reinstatement and special designation
        :return: void if the report is to text
                list[[string]x3] if the report is to screen
        """
        self.progress_win.setLabelText("Checking streets asd coords...")
        results_list = [self.write_content(12, 13, 13, 7), self.write_content(13, 14, 14, 7),
                        self.write_content(14, 15, 15, 7)]
        self.progress_win.setValue(10)
        return results_list

    def maint_no_poly(self):
        # function that checks maintenance record that have no link to
        # road polygons
        self.progress_win.setLabelText("Checking maintenance records for polygons...")
        result_list = self.write_content(15, 16, 16, 8)
        self.progress_win.setValue(11)
        return result_list

    def poly_no_maint(self):
        """
        group of two checks on road polygons
        1: polygons that have not link to maintenance records
        2: polygons wrongly assigned to more than one maintenance record
        :return: void
        """
        results_list = [self.write_content(16, 17, 17, 9), self.write_content(17, 18, 18, 10)]
        self.progress_win.setValue(12)
        return results_list

    def end_report(self, parent):
        self.progress_win.close()
        parent.close()

    def content_to_screen(self, content_list=None, query_model=None, columns_name_id=None, no_content_id=None):
        """
        handles the creation of an on-screen validation report version, the function handles the case
        of a report created both from db records and mixed data from db and spatial features
        :param content_list: list[string] 'ready made' list of values to print on the screen if data comes
        from mixed sources (db + features)
        :param query_model: QtSqlQueryModel model of the query if all data comes from db
        :param columns_name_id: int index of the column names dictionary to print column names on tables
        """
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
            while k <= len(self.column_names[columns_name_id]) - 1:
                content_list.append(self.column_names[columns_name_id])
                k += 1
                # if there are no problems just print a message
                # on the first item in the list
            if n_rows < 1:
                content_list.append([self.headers_no_items[no_content_id]])
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
        return content_list

    def init_queries(self):
        """ database queries initialisation"""
        self.queries = {

            0: "SELECT (ifnull(tblSTREET.Description, '') ||'|'|| ifnull(tlkpLOCALITY.Name, '')||'|'|| "
               "ifnull(tlkpTOWN.Name,'')) AS DuplicateRoads FROM (tblSTREET INNER JOIN tlkpLOCALITY "
               "ON tblSTREET.Loc_Ref = tlkpLOCALITY.Loc_Ref) INNER JOIN tlkpTOWN "
               "ON tblSTREET.Town_Ref = tlkpTOWN.Town_Ref GROUP BY tblSTREET.Currency_flag, "
               "tblSTREET.Description, tlkpLOCALITY.Name, tlkpTOWN.Name HAVING (((Count(tblSTREET.USRN))>1) "
               "AND ((tblSTREET.Currency_flag)=0))",

            1: "SELECT (ifnull(tblSTREET.USRN, '') ||'|'|| ifnull(tblSTREET.Version_No, '') ||'|'|| "
               "ifnull(tblSTREET.Street_ref_type, '') ||'|'|| ifnull(tblSTREET.Description, '')||'|'|| "
               "ifnull(tblSTREET.Update_date, '') ||'|'|| ifnull(tblSTREET.Updated_by, '')) AS not_linked_usrn "
               "FROM tblSTREET LEFT JOIN (SELECT * from lnkESU_STREET where lnkESU_Street.Currency_Flag = 0) "
               "AS STREET_LINK ON (tblSTREET.Version_No = STREET_LINK.usrn_version_no) "
               "AND (tblSTREET.USRN = STREET_LINK.usrn) WHERE (((tblSTREET.Currency_flag) = 0) "
               "AND ((STREET_LINK.usrn) Is Null)) ORDER BY tblSTREET.USRN ",

            2: "SELECT (ifnull(q12.esu_id,'') ||'|'|| ifnull(q12.street_ref_type,'') ||'|'|| "
               "ifnull(q12.USRN,'') ||'|'|| ifnull(q12.Description,'')) AS type3_not_linked "
               "FROM (SELECT DISTINCT lnkESU_STREET.esu_id, "
               "tblSTREET.Street_ref_type, tblStreet.Description,tblStreet.USRN "
               "FROM (lnkESU_STREET INNER JOIN tblSTREET ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) "
               "AND (lnkESU_STREET.usrn = tblSTREET.USRN)) INNER JOIN tblMAINT ON (tblSTREET.USRN = tblMAINT.USRN) "
               "WHERE (((tblSTREET.street_ref_type = 1) Or (tblSTREET.street_ref_type = 2)) AND "
               "(lnkESU_STREET.Currency_flag = 0) And (tblSTREET.Currency_flag = 0) AND "
               "(tblMAINT.Road_Status_Ref = 1)) ORDER BY lnkESU_STREET.esu_id) AS q12 LEFT JOIN "
               "(SELECT lnkESU_STREET.esu_id, tblSTREET.Street_ref_type FROM lnkESU_STREET INNER JOIN tblSTREET "
               "ON (lnkESU_STREET.usrn_version_no = tblSTREET.Version_No) AND (lnkESU_STREET.usrn = tblSTREET.USRN) "
               "WHERE ((tblSTREET.street_ref_type = 3) "
               "AND (lnkESU_STREET.Currency_flag = 0) And (tblSTREET.Currency_flag = 0)) "
               "ORDER BY lnkESU_STREET.esu_id) AS q3 ON q12.esu_id = q3.esu_id WHERE (q3.esu_id Is Null)",

            3: "SELECT (ifnull(qryID.esu_id,'') ||'|'|| ifnull(qryID.esuxy,'')) as dup_esu_ref FROM "
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

            10: "SELECT (ifnull(tblSTREET.USRN,'') ||'|'|| ifnull(tblSTREET.Street_ref_type,'') ||'|'|| "
                "ifnull(tblSTREET.Description,'')) AS type12_maint "
                "FROM tblSTREET LEFT JOIN (SELECT tblMAINT.USRN, tblMAINT.Maint_id "
                "FROM tblMAINT WHERE (((tblMAINT.Currency_flag)=0))) as maint ON tblSTREET.USRN = maint.USRN "
                "WHERE (((tblSTREET.street_ref_type) = 1 Or (tblSTREET.street_ref_type) = 2) "
                "AND ((tblSTREET.Currency_flag) = 0) And ((maint.maint_id) Is Null)) "
                "ORDER BY tblSTREET.USRN",

            11: "SELECT (ifnull(tblSTREET.USRN,'') ||'|'|| ifnull(tblSTREET.Street_ref_type,'') "
                "||'|'|| ifnull(tblSTREET.Description,'')) AS check_reins "
                "FROM tblSTREET LEFT JOIN (SELECT tblReins_Cat.USRN, tblReins_Cat.Reins_cat_id FROM tblReins_Cat "
                "WHERE (((tblReins_Cat.Currency_flag)=0))) as reins ON tblSTREET.USRN = reins.USRN "
                "WHERE (((tblSTREET.street_ref_type) = 1 Or (tblSTREET.street_ref_type) = 2) "
                "AND ((tblSTREET.Currency_flag) = 0) And ((reins.Reins_cat_id) Is Null)) "
                "AND tblStreet.USRN not in (Select distinct s.USRN "
                "FROM tblStreet s inner join tblMaint m on m.USRN = s.USRN WHERE s.Currency_flag = 0 "
                "AND m.currency_flag = 0 and m.road_status_ref = 4) "
                "ORDER BY tblSTREET.USRN",

            12: "SELECT (ifnull(S.USRN,'') ||'|'||ifnull(ASD.Maint_ID,'') ||'|'|| ifnull(ASD.Reference_No,'')) "
                "as inv_maint FROM tblMaint ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 AND ((ASD.start_xref = 0 "
                "or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            13: "SELECT (ifnull(S.USRN,'') ||'|'|| ifnull(ASD.Reins_Cat_Id,'') ||'|'|| ifnull(ASD.Reference_No,'')) "
                "AS inv_reins FROM tblReins_Cat ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 "
                "AND ((ASD.start_xref = 0 or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            14: "SELECT (ifnull(S.USRN,'') ||'|'|| ifnull(ASD.Spec_Des_ID,'') ||'|'|| ifnull(ASD.Reference_No,'')) "
                "AS inv_spec_des FROM tblSpec_Des ASD left join tblSTREET S ON S.USRN = ASD.USRN "
                "WHERE ASD.Currency_flag = 0 AND S.Currency_Flag = 0 AND ASD.Whole_Road = 0 "
                "AND ((ASD.start_xref = 0 or ASD.start_Yref = 0 or ASD.end_xref = 0 or ASD.end_yref = 0 ) or "
                "(ASD.start_xref = NULL or ASD.start_Yref = NULL or ASD.end_xref = NULL or ASD.end_yref = NULL)) "
                "ORDER BY S.USRN",

            15: "SELECT (ifnull(tblMAINT.USRN,'') ||'|'|| ifnull(tblMAINT.Maint_id, '') ||'|'|| "
                "ifnull(tlkpROAD_STATUS.Description, '')) as road_status "
                "FROM (tblMAINT LEFT JOIN lnkMAINT_RD_POL ON tblMAINT.Maint_id = lnkMAINT_RD_POL.maint_id) "
                "INNER JOIN tlkpROAD_STATUS ON tblMAINT.Road_status_ref = tlkpROAD_STATUS.Road_status_ref "
                "WHERE (((tblMAINT.Currency_flag) = 0) And ((lnkMAINT_RD_POL.rd_pol_id) Is Null)) "
                "ORDER BY tblMAINT.USRN",

            16: "SELECT rdpoly.RD_POL_ID FROM rdpoly "
                "LEFT JOIN (select * from lnkMaint_RD_POL WHERE currency_flag = 0) "
                "AS mrp ON rdpoly.RD_POL_ID = mrp.rd_pol_id WHERE (((mrp.Maint_ID) Is Null)) ORDER BY rdpoly.RD_POL_ID",

            17: "SELECT (ifnull(mp.rd_pol_id,'') ||'|'|| ifnull(tblMAINT.USRN,'') ||'|'|| "
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

