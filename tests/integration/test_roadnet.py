import unittest

from Roadnet.tests.integration.roadnet_test_cases import RoadnetTestCase


class TestRoadnet(RoadnetTestCase):
    def test_mock_iface(self):
        # mapCanvas is set manually during mocking process
        self.assertEqual(hasattr(self.rn.iface, 'mapCanvas'), True)
        # setActiveLayer is created automatically by mock
        self.assertEqual(hasattr(self.rn.iface, 'setActiveLayer'), True)

    def test_roadnet_loaded(self):
        self.assertEqual(hasattr(self.rn, 'roadnet_started'), True)

if __name__ == '__main__':
    unittest.main()
