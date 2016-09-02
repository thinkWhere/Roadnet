"""
This script can be run from the command line from the directory above roadNet with:
python -m Roadnet.tests.test_geometry_handling
"""
import unittest

from qgis.core import QgsGeometry, QgsPoint, QgsFeature, QgsVectorLayer, QgsField
from PyQt4.QtCore import QVariant

from Roadnet.geometry.esu_edit_handler import EsuIntersectionHandler
from Roadnet.geometry import edit_handler
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase

def prepare_lines_and_geometries():
    # Define features that are used by each of the test classes
    lines = {
        'main':
            'LineString (277800.0 694700.0, '
            '277850.0 694700.0, '
            '278100.0 694700.0, '
            '278150.0 694700.0, '
            '278200.0 694700.0, '
            '278350.0 694700.0)',
        'multi_line_main':
            'MultiLineString ((277800.0 694700.0, '
            '277850.0 694700.0, '
            '278100.0 694700.0, '
            '278150.0 694700.0, '
            '278200.0 694700.0, '
            '278350.0 694700.0))',
        'misses':
            'LineString (277750.0 694750.0, '
            '277750.0 694650.0)',
        'crosses_end':
            'LineString (277800.0 694750.0, '
            '277800.0 694700.0, '
            '277800.0 694650.0)',
        'crosses_node':
            'LineString (277850.0 694750.0, '
            '277850.0 694700.0, '
            '277850.0 694650.0)',
        'crosses':
            'LineString (277900.0 694750.0, '
            '277900.0 694650.0)',
        'crosses_twice':
            'LineString (277950.0 694750.0, '
            '277950.0 694650.0, '
            '278000.0 694650.0, '
            '278000.0 694750.0)',
        'touches':
            'LineString (278100.0 694750.0, '
            '278100.0 694700.0)',
        'touches_end':
            'LineString (278350.0 694750.0, '
            '278350.0 694700.0)',
        'multi_touches_end':
            'MultiLineString ((278350.0 694750.0, '
            '278350.0 694700.0))',
        'crosses_shallow':
            'LineString (278000.0 694702.0, '
            '278500.0 694698.0)'}

    # Convert to geometries
    geometries = {}
    for key, value in lines.iteritems():
        geometries[key] = QgsGeometry.fromWkt(value)

    return lines, geometries


def prepare_features_and_vector_layer(geometries):
    # Add to vector layer
    vlayer = QgsVectorLayer("multilinestring?crs=EPSG:27700&field=name:string(25)",
                            "temp", "memory")
    provider = vlayer.dataProvider()
    features = {}
    fields = provider.fields()
    for key, value in geometries.iteritems():
        feature = QgsFeature(fields)
        feature.setGeometry(value)
        feature.setAttribute('name', key)
        features[key] = feature
    provider.addFeatures([features[k] for k in features if not k.endswith('main')])
    vlayer.updateExtents()

    return features, vlayer


class TestEsuSplitLine(unittest.TestCase):
    def setUp(self):
        self.lines, self.geometries = prepare_lines_and_geometries()

    def tearDown(self):
        # Do not call self.qgs.exitQgis() here; it causes segfault.
        pass

    def test_qgs_geometry(self):
        geometry = QgsGeometry.fromWkt('LineString (0 0, 0 1)')
        self.assertEqual(geometry.length(), 1,
                         'Line length was not 2.')

    def test_misses(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        misses = QgsGeometry.fromWkt(self.lines['misses'])
        parts = EsuIntersectionHandler.split_line(main, [misses])
        part = parts[0]
        self.assertEqual(len(parts), 1,
                         'Main line split into parts by line that missed.')
        # Lengths are compared to within 3 decimal places e.g. 1 mm.
        self.assertAlmostEqual(part.length(), main.length(), 3,
                               'Main line length changed by line that missed.')

    def test_crosses(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses = QgsGeometry.fromWkt(self.lines['crosses'])
        parts = EsuIntersectionHandler.split_line(main, [crosses])
        part_lengths = [100, 450]  # Should create these two lines
        self.assertEqual(len(parts), len(part_lengths),
                         'Single crossing split did not create two parts.')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Single crossing split made wrong length parts.')

    def test_crosses_node(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses_node = QgsGeometry.fromWkt(self.lines['crosses_node'])
        parts = EsuIntersectionHandler.split_line(main, [crosses_node])
        part_lengths = [50, 500]  # Should create these two lines
        self.assertEqual(len(parts), len(part_lengths),
                         'Single crossing node split did not create two parts.')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Single crossing node split made wrong length parts.')

    def test_crosses_end(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses_end = QgsGeometry.fromWkt(self.lines['crosses_end'])
        parts = EsuIntersectionHandler.split_line(main, [crosses_end])
        part_lengths = [550]  # Should create one line
        self.assertEqual(len(parts), len(part_lengths),
                         'Crossing at end split the line into many parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Crossing at end split the line into many parts')

    def test_crosses_twice(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses_twice = QgsGeometry.fromWkt(self.lines['crosses_twice'])
        parts = EsuIntersectionHandler.split_line(main, [crosses_twice])
        part_lengths = [150, 50, 350]  # Should create one line
        self.assertEqual(len(parts), len(part_lengths),
                         'Crossing twice produced wrong number of parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Crossing crossing twice produced wrong part lengths')

    def test_touches(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        touches = QgsGeometry.fromWkt(self.lines['touches'])
        parts = EsuIntersectionHandler.split_line(main, [touches])
        part_lengths = [300, 250]  # Should create two parts
        self.assertEqual(len(parts), len(part_lengths),
                         'Touching intersect produced wrong number of parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Touching intersect produced wrong part lengths')

    def test_touches_end(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        touches_end = QgsGeometry.fromWkt(self.lines['touches_end'])
        parts = EsuIntersectionHandler.split_line(main, [touches_end])
        part_lengths = [550]  # Should create one line
        self.assertEqual(len(parts), len(part_lengths),
                         'Crossing at end split the line into many parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 3,
                'Crossing at end split the line into many parts')

    def test_crosses_shallow(self):
        # This test should pick up tiny geometries that were produced by
        # shallow angle crossings in earlier versions of roadNet.
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses_shallow = QgsGeometry.fromWkt(self.lines['crosses_shallow'])
        parts = EsuIntersectionHandler.split_line(main, [crosses_shallow])
        part_lengths = [450, 100]  # Should create two parts
        self.assertEqual(len(parts), len(part_lengths),
                         'Crossing shallow produced wrong number of parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 0,
                'Crossing shallow produced wrong line lengths')

    def test_many_crossings(self):
        main = QgsGeometry.fromWkt(self.lines['main'])
        crosses_shallow = QgsGeometry.fromWkt(self.lines['crosses_shallow'])
        crosses = QgsGeometry.fromWkt(self.lines['crosses'])
        crosses_node = QgsGeometry.fromWkt(self.lines['crosses_node'])
        crosses_twice = QgsGeometry.fromWkt(self.lines['crosses_twice'])
        touches = QgsGeometry.fromWkt(self.lines['touches'])
        other_line_geometries = [crosses_shallow, touches, crosses_twice,
                                 crosses, crosses_node]
        parts = EsuIntersectionHandler.split_line(main, other_line_geometries)
        part_lengths = [50, 50, 50, 50, 100, 150, 100]  # Should create two parts
        self.assertEqual(len(parts), len(part_lengths),
                         'Many crossings produced the wrong number of parts')
        for i, part_length in enumerate(part_lengths):
            self.assertAlmostEqual(
                parts[i].length(), part_length, 0,
                'Many crossings produced parts with the wrong lengths.')


class TestIntersectionFinding(QgisTestCase):
    def setUp(self):
        super(TestIntersectionFinding, self).setUp()
        self.lines, self.geometries = prepare_lines_and_geometries()

    def test_convert_to_points_list(self):
        # Arrange
        expected = [QgsPoint(278350.0, 694750.0),
                    QgsPoint(278350.0, 694700.0)]
        # Act and assert
        for key in ['touches_end', 'multi_touches_end']:
            geometry = self.geometries[key]
            result = edit_handler.convert_to_points_list(geometry)
            self.assertEqual(expected, result)

    def test_touch_is_ends_only_true(self):
        result = edit_handler.touch_is_ends_only(self.geometries['touches_end'],
                                                 self.geometries['main'])
        self.assertTrue(result,
                        "End-touching geometry not recognised.")

    def test_touch_is_ends_only_false(self):
        result = edit_handler.touch_is_ends_only(self.geometries['touches'],
                                                 self.geometries['main'])
        self.assertFalse(result,
                         "Geometry incorrectly identified as end-touching")

    def test_find_intersections(self):
        # Arrange
        features, vlayer = prepare_features_and_vector_layer(
            self.geometries)
        expected_names = [u'crosses_end', u'crosses_node', u'crosses',
                          u'crosses_twice', u'crosses_shallow']
        expected_names.sort()

        # Act
        results = edit_handler.find_intersections(features['main'],
                                                  vlayer)
        result_names = [r['name'] for r in results]
        result_names.sort()

        # Assert
        print('\nInput:')
        print(sorted([f['name'] for f in vlayer.getFeatures()]))
        print('\nExpected:')
        print(expected_names)
        print('\nResult:')
        print(result_names)
        self.assertEquals(expected_names, result_names)


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.abspath(__file__))
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from Roadnet.geometry.esu_edit_handler import EsuIntersectionHandler
    else:
        from geometry.esu_edit_handler import EsuIntersectionHandler
    unittest.main()
