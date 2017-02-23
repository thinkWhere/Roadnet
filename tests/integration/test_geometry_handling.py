"""
This script can be run from the command line from the Roadnet directory with:
nosetests -q -s tests.integration.test_geometry_handling
"""
import unittest

from qgis.core import QgsGeometry, QgsPoint, QgsFeature, QgsVectorLayer, QgsField
from PyQt4.QtCore import QVariant

from Roadnet.geometry.esu_edit_handler import EsuIntersectionHandler
from Roadnet.geometry.rdpoly_edit_handler import RdpolyIntersectionHandler, IntersectionHandlerError
from Roadnet.geometry import edit_handler
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase

MULTI_WITH_TINY = u'MultiPolygon (((286666.19960006879409775 680663.14264002745039761, ' \
                  u'286667.41464883968001232 680660.57753706665243953, ' \
                  u'286662.32514680456370115 680656.23025407828390598, ' \
                  u'286660.93356714065885171 680656.48326856270432472, ' \
                  u'286661.84399999998277053 680660.125, ' \
                  u'286661.86099999997531995 680660.14599999994970858, ' \
                  u'286662.43800000002374873 680660.875, ' \
                  u'286662.90600000001722947 680661.31299999996554106, ' \
                  u'286663.31300000002374873 680661.68799999996554106, ' \
                  u'286663.81300000002374873 680662, ' \
                  u'286664.40600000001722947 680662.375, ' \
                  u'286665.06300000002374873 680662.68799999996554106, ' \
                  u'286665.68800000002374873 680662.93799999996554106, ' \
                  u'286666.19960006879409775 680663.14264002745039761)), ' \
                  u'((' \
                  u'286662.09704670298378915 680667.59712448180653155, ' \
                  u'286662.09729453345062211 680667.59729605680331588, ' \
                  u'286660.50515622308012098 680661.31961597572080791, ' \
                  u'286660.50515619333600625 680661.31961593753658235, ' \
                  u'286662.09704670298378915 680667.59712448180653155)))'
SINGLE_POLYGON = u'Polygon ((286666.19960006879409775 680663.14264002745039761, ' \
                  u'286667.41464883968001232 680660.57753706665243953, ' \
                  u'286662.32514680456370115 680656.23025407828390598, ' \
                  u'286660.93356714065885171 680656.48326856270432472, ' \
                  u'286661.84399999998277053 680660.125, ' \
                  u'286661.86099999997531995 680660.14599999994970858, ' \
                  u'286662.43800000002374873 680660.875, ' \
                  u'286662.90600000001722947 680661.31299999996554106, ' \
                  u'286663.31300000002374873 680661.68799999996554106, ' \
                  u'286663.81300000002374873 680662, ' \
                  u'286664.40600000001722947 680662.375, ' \
                  u'286665.06300000002374873 680662.68799999996554106, ' \
                  u'286665.68800000002374873 680662.93799999996554106, ' \
                  u'286666.19960006879409775 680663.14264002745039761))'
TINY_POLYGON = u'Multipolygon (((286662.09704670298378915 680667.59712448180653155, ' \
                  u'286662.09729453345062211 680667.59729605680331588, ' \
                  u'286660.50515622308012098 680661.31961597572080791, ' \
                  u'286660.50515619333600625 680661.31961593753658235, ' \
                  u'286662.09704670298378915 680667.59712448180653155)))'


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


class TestDropTinyGeometryParts(unittest.TestCase):
    def test_multi_with_tiny_drops_tiny_and_returns_multipolygon(self):
        # Arrange
        dirty_geom = QgsGeometry.fromWkt(MULTI_WITH_TINY)
        clean_multi_geom = QgsGeometry.fromWkt(SINGLE_POLYGON)
        clean_multi_geom.convertToMultiType()

        # Act
        clean_geom = RdpolyIntersectionHandler.clean_up_geometry(dirty_geom)

        # Assert
        print(dirty_geom.exportToWkt())
        print(clean_geom.exportToWkt())
        self.assertEqual(clean_geom.exportToWkt(),
                         clean_multi_geom.exportToWkt())

    def test_tiny_only_raises_error(self):
        # Arrange
        dirty_geom = QgsGeometry.fromWkt(TINY_POLYGON)

        # Act and assert
        with self.assertRaises(IntersectionHandlerError):
            clean_geom = RdpolyIntersectionHandler.clean_up_geometry(dirty_geom)

    def test_no_tiny_returns_original(self):
        # Arrange
        dirty_geom = QgsGeometry.fromWkt(SINGLE_POLYGON)
        clean_multi_geom = QgsGeometry.fromWkt(SINGLE_POLYGON)
        clean_multi_geom.convertToMultiType()

        # Act
        clean_geom = RdpolyIntersectionHandler.clean_up_geometry(dirty_geom)

        # Assert
        self.assertEqual(clean_geom.exportToWkt(),
                         clean_multi_geom.exportToWkt())


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
