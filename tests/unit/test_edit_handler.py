import unittest
from mock import patch, Mock, sentinel
import Roadnet.geometry.edit_handler as edit_handler

class MockDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.p_databasehandler = patch.object(edit_handler, 'DatabaseHandler')
        self.p_databasehandler.start()

        self.p_config = patch.object(edit_handler, 'config')
        self.config = self.p_config.start()
        self.config.DEBUG_MODE = False

        iface = Mock()
        vlayer = Mock()
        db = Mock()
        params = {}
        handle_intersect_flag = False

        self.eh_obj = edit_handler.EditHandler(iface, vlayer, db, params, handle_intersect_flag)

    def tearDown(self):
        self.p_databasehandler.stop()
        self.p_config.stop()


class TestEditHandlerAddsCommitted(MockDatabaseHandler):

    def test_edit_handler_instantiates(self):
        self.assertTrue(hasattr(self.eh_obj, 'handle_intersect_flag'))

    def test_no_added_features(self):
        with patch.object(edit_handler.EditHandler, 'handle_intersections') as handle:
            layer_id = sentinel.layer
            added_features = []
            self.eh_obj.adds_committed(layer_id, added_features)
            self.assertFalse(handle.called)

    @patch.object(edit_handler.EditHandler, 'handle_intersections')
    def test_no_added_features_decorated(self, p_handle_intersections):
        layer_id = sentinel.layer
        added_features = []
        self.eh_obj.adds_committed(layer_id, added_features)
        self.assertFalse(p_handle_intersections.called)

    def test_intersections_true(self):
        self.eh_obj.handle_intersect_flag = True
        with patch.object(edit_handler.EditHandler, 'handle_intersections') as handle:
            with patch.object(edit_handler.EditHandler, 'check_for_intersections') as check_intersections:
                check_intersections.return_value = True
                layer_id = Mock()
                feature = Mock()
                added_features = [feature]
                self.eh_obj.adds_committed(layer_id, added_features)
                self.assertTrue(handle.called)


if __name__ == '__main__':
    unittest.main()
