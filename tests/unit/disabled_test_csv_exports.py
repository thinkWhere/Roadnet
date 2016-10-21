import unittest
import Roadnet.exports.export_csv as export_csv


class TestExportCsv(unittest.TestCase):
    def test_add_quotes_to_second_field(self):
        # Arrange
        original = [124, 'I', '2001-01-01', 1.2]
        expected = [124, '"I"', '2001-01-01', 1.2]

        # Act
        result = export_csv.add_quotes_to_second_field(original)

        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
