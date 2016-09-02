import unittest

import Roadnet.tests.integration.qgis_interface as qgis_interface
import Roadnet


class QgisTestCase(unittest.TestCase):
    def setUp(self):
        self.qgs = qgis_interface.start_app(gui_flag=True)
        self.iface = qgis_interface.get_mock_iface()

    def tearDown(self):
        # Do not call self.qgs.exitQgis() here; it causes segfault.
        self.iface = None


class RoadnetTestCase(QgisTestCase):
    def setUp(self):
        super(RoadnetTestCase, self).setUp()
        self.setup_roadnet()

    def setup_roadnet(self):
        self.rn = Roadnet.classFactory(self.iface)

    def tearDown(self):
        super(RoadnetTestCase, self).tearDown()
        self.tear_down_roadnet()

    def tear_down_roadnet(self):
        self.rn.unload()
        self.rn = None

if __name__ == '__main__':
    unittest.main()
