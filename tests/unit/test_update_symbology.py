import unittest
from mock import patch, Mock

import Roadnet.admin.update_symbology as sym
UpdateSymbologyThread = sym.UpdateSymbologyThread


MAINT_IDS_LIST = {
            'unassigned': [],
            'single': [99],
            'multiple': [1, 2, 3]}

class TestUpdateSymbologyFeatureCount(unittest.TestCase):
    def setUp(self):
        self.p_init_data = patch.object(UpdateSymbologyThread, '_init_data')
        self.p_init_data.start()

    def tearDown(self):
        self.p_init_data.stop()

    def test_total_feature_count_rdpoly_true(self):
        update_symbology = self.update_symbology_rdpoly_esu_booleans(True, False)
        update_symbology.rdpoly_f_count = 10
        update_symbology.esu_f_count = 1
        count = update_symbology.calculate_total_feature_count()
        self.assertEqual(count, 10,
                         'Total feature count was not 10 ({})'.format(count))

    def test_total_feature_count_esu_true(self):
        update_symbology = self.update_symbology_rdpoly_esu_booleans(False, True)
        update_symbology.rdpoly_f_count = 10
        update_symbology.esu_f_count = 1
        count = update_symbology.calculate_total_feature_count()
        self.assertEqual(count, 1,
                         'Total feature count was not 1 ({})'.format(count))

    def test_total_feature_count_both_true(self):
        update_symbology = self.update_symbology_rdpoly_esu_booleans(True, True)
        update_symbology.rdpoly_f_count = 10
        update_symbology.esu_f_count = 1
        count = update_symbology.calculate_total_feature_count()
        self.assertEqual(count, 11,
                         'Total feature count was not 11 ({})'.format(count))

    def test_total_feature_count_neither_true(self):
        update_symbology = self.update_symbology_rdpoly_esu_booleans(False, False)
        update_symbology.rdpoly_f_count = 10
        update_symbology.esu_f_count = 1
        count = update_symbology.calculate_total_feature_count()
        self.assertEqual(count, 0,
                         'Total feature count was not 0 ({})'.format(count))

    @staticmethod
    def update_symbology_rdpoly_esu_booleans(run_rd_poly, run_esu):
        db = Mock()
        rdpoly_layer = Mock()
        esu_layer = Mock()
        update_symbology = UpdateSymbologyThread(db, rdpoly_layer, esu_layer, run_rd_poly, run_esu)
        return update_symbology


class TestUpdateSymbologyRdPolySymbology(unittest.TestCase):
    def setUp(self):
        self.p_init_data = patch.object(UpdateSymbologyThread, '_init_data')
        self.p_init_data.start()
        db = Mock()
        rdpoly_layer = Mock()
        esu_layer = Mock()
        run_rd_poly = True
        run_esu = False
        self.update_symbology = UpdateSymbologyThread(db, rdpoly_layer,
                                                      esu_layer, run_rd_poly,
                                                      run_esu)

    def tearDown(self):
        self.p_init_data.stop()
        self.update_symbology = None


    def test_calculate_rdpoly_symbology_value_unassigned(self):
        maint_ids = MAINT_IDS_LIST['unassigned']
        symbol = self.update_symbology.calculate_rdpoly_symbology_value(maint_ids)
        self.assertEqual(symbol, 1,
                         "Unassigned polygon did not get symbol 0 {}.".format(symbol))

    @patch.object(UpdateSymbologyThread, 'get_road_status_ref')
    def test_calculate_rdpoly_symbology_value_single(self, mock_road_status):
        mock_road_status.return_value = 2
        maint_ids = MAINT_IDS_LIST['single']
        symbol = self.update_symbology.calculate_rdpoly_symbology_value(maint_ids)

        mock_road_status.assert_called_once_with(maint_ids[0])
        expected = 12
        self.assertEqual(expected, symbol,
                         "Symbology value incorrect. "
                         "Expected {}, got {}".format(expected, symbol))

    def test_calculate_rdpoly_symbology_value_multiple(self):
        maint_ids = MAINT_IDS_LIST['multiple']
        symbol = self.update_symbology.calculate_rdpoly_symbology_value(maint_ids)
        self.assertEqual(symbol, 2,
                         "Polygon with multiple links did not get symbol 2 {}.".format(symbol))

class TestUpdateSymbologyGetRoadStatusRef(unittest.TestCase):
    def setUp(self):
        self.p_init_data = patch.object(UpdateSymbologyThread, '_init_data')
        self.p_init_data.start()
        db = Mock()
        rdpoly_layer = Mock()
        esu_layer = Mock()
        run_rd_poly = True
        run_esu = False
        self.update_symbology = UpdateSymbologyThread(db, rdpoly_layer,
                                                      esu_layer, run_rd_poly,
                                                      run_esu)

    def tearDown(self):
        self.p_init_data.stop()
        self.update_symbology = None

    @patch.object(sym, 'QSqlQuery')
    def test_get_road_status_sends_correct_query(self, mock_query):
        maint_id = 9999
        expected_sql = """
            SELECT road_status_ref FROM tblMAINT
            WHERE maint_id = 9999
            AND currency_flag = 0
            ;"""
        self.update_symbology.get_road_status_ref(maint_id)
        mock_query.assert_called_once_with(expected_sql,
                                           self.update_symbology.db)

    def test_fail_if_invalid_road_status(self):
        with self.assertRaises(ValueError):
            maint_id = 999
            road_status_ref = 5
            self.update_symbology.fail_if_invalid_road_status_ref(
                maint_id, road_status_ref)

if __name__ == '__main__':
    unittest.main()
