import unittest

from mock import patch
from qgis.core import QgsVectorLayer

from Roadnet.tests.integration.roadnet_test_cases import RoadnetTestCase
from Roadnet.roadnet import Roadnet
from Roadnet.ramp import ramp
import Roadnet.roadnet_exceptions as rn_except


class TestRamp(RoadnetTestCase):
    def test_mock_iface(self):
        # mapCanvas is set manually during mocking process
        self.assertEqual(hasattr(self.rn.iface, 'mapCanvas'), True)
        # setActiveLayer is created automatically by mock
        self.assertEqual(hasattr(self.rn.iface, 'setActiveLayer'), True)

    @patch.object(ramp, 'show_messagebox')
    def test_run_ramp_mcl_select_no_mcl(self, mock_error):
        # Arrange
        test_ramp = ramp.Ramp(self.rn)
        test_ramp.mcl = None

        # Act
        # Patched error required because user gets warning if no mcl set.
        test_ramp.run_ramp_mcl_select()  # Should return early as mcl not set

        # Assert
        self.rn.iface.setActiveLayer.assert_not_called()

if __name__ == '__main__':
    unittest.main()
