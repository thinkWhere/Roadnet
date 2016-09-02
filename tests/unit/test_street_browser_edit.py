import unittest
from mock import patch, Mock, MagicMock, sentinel
from qgis.core import QgsVectorLayer
from PyQt4.QtSql import QSqlDatabase
from Roadnet.street_browser.edit import UpdateEsuSymbology


class TestUpdateSymbologyFeatureCount(unittest.TestCase):
    easy_cases = {'just_one': ([1], 10),
                  'just_two': ([2], 11),
                  'one_three': ([1, 3], 12),
                  'two_three': ([2, 3], 13),
                  'one_four': ([1, 4], 14),
                  'two_four': ([2, 4], 15),
                  'one_three_four': ([1, 3, 4], 16),
                  'two_three_four': ([2, 3, 4], 17)}

    edge_cases = {'two_ones': ([1, 1], 1),
                  'five': ([5], 1),
                  'two_twos': ([2, 2], 1),
                  'just_three': ([3], 1),
                  'just_four': ([4], 1),
                  'three_four': ([3, 4], 1),
                  'one_two_three_four': ([1, 2, 3, 4], 1),
                  'one_four_three_four': ([1, 4, 3, 4], 16),
                  'two_four_four': ([2, 4, 4], 15)}

    def setUp(self):
        db = MagicMock(spec=QSqlDatabase)
        esu_layer = MagicMock(spec=QgsVectorLayer)
        self.update_esu_symbology = UpdateEsuSymbology(db, esu_layer)

    def tearDown(self):
        del self.update_esu_symbology

    def test_calculate_symbol_from_easy_cases(self):
        for easy_case in self.easy_cases:
            types, expected = self.easy_cases[easy_case]
            symbol = self.update_esu_symbology.calculate_symbol_no(types)
            self.assertEqual(
                expected, symbol,
                "ESU with Type {} record was not assigned symbol {} ({})".format(
                    types, expected, symbol))

    def test_calculate_symbol_from_edge_cases(self):
        for edge_case in self.edge_cases:
            types, expected = self.edge_cases[edge_case]
            symbol = self.update_esu_symbology.calculate_symbol_no(types)
            self.assertEqual(
                expected, symbol,
                "ESU with Type {} record was not assigned symbol {} ({})".format(
                    types, expected, symbol))

    def test_calculate_symbol_no_types(self):
        types = []
        expected = 0
        symbol = self.update_esu_symbology.calculate_symbol_no(types)
        self.assertEqual(
            expected, symbol,
            "ESU with no records was not assigned symbol {} ({})".format(
                expected, symbol))


if __name__ == '__main__':
    unittest.main()