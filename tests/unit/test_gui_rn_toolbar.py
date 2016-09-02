import unittest

from mock import MagicMock, call

from Roadnet.gui.toolbar import RoadnetToolbar
from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase

class TestRoadnetToolbar(QgisTestCase):
    def setUp(self):
        super(TestRoadnetToolbar, self).setUp()
        self.rn_buttons = ['sb_btn', 'street_sel_btn']
        self.ramp_buttons = ['mcl_select_btn', 'mcl_auto_number_btn',
                             'rdpoly_select_btn']
        self.rn_menu_items = ['start_rn', 'stop_rn', 'change_db_path', 'settings',
                              'create_restore', 'change_pwd', 'help', 'exp_lgs',
                              'exp_srwr', 'exp_lsg_shp', 'exp_maintain_poly',
                              'exp_list_roads', 'meta_menu', 'edit_lsg_lu',
                              'edit_srwr_lu', 'validation_rpt', 'street_rpt',
                              'clean_rdpoly']
        self.ramp_menu_items = ['load_layers', 'road_length', 'export_wdm']
        self.init_items = ['start_rn', 'change_db_path', 'help', 'about']
        self.readonly_items = ['stop_rn', 'settings', 'create_restore',
                               'help', 'about', 'street_sel_btn',
                               'sb_btn', 'exp_menu', 'admin_menu', 'meta_menu',
                               'validation_rpt', 'street_rpt']
        self.editor_items = ['stop_rn', 'settings', 'create_restore',
                             'change_pwd', 'edit_lsg_lu', 'edit_srwr_lu',
                             'help', 'about', 'street_sel_btn',
                             'sb_btn', 'exp_menu', 'admin_menu', 'meta_menu',
                             'validation_rpt', 'street_rpt']
        self.readonly_items += self.ramp_buttons
        self.editor_items += self.ramp_buttons

    def test_toolbar_buttons_with_ramp(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for button in self.rn_buttons + self.ramp_buttons:
            button_not_set = getattr(tb, button) is None
            self.assertFalse(button_not_set,
                             "{} button has not been set".format(button))

    def test_menu_items_with_ramp(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for item in self.rn_menu_items + self.ramp_menu_items:
            item_not_set = getattr(tb, item) is None
            self.assertFalse(item_not_set,
                             "{} menu item has not been set.".format(item))

    def test_toolbar_buttons_without_ramp(self):
        with_ramp = False
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for button in self.rn_buttons:
            button_not_set = getattr(tb, button) is None
            self.assertFalse(button_not_set,
                             "{} button has not been set".format(button))

    def test_menu_items_without_ramp(self):
        with_ramp = False
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for item in self.rn_menu_items:
            item_not_set = getattr(tb, item) is None
            self.assertFalse(item_not_set,
                             "{} menu item has not been set.".format(item))

    def test_set_state_editor(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        all_buttons = self.rn_buttons + self.ramp_buttons
        for attr in all_buttons:
            setattr(tb, attr, MagicMock())

        tb.set_state('editor')

        for attr in all_buttons:
            current = getattr(tb, attr)
            expected_calls = [call.setEnabled(False), call.setEnabled(True)]
            current.assert_has_calls(expected_calls)

    def test_set_state_init(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for attr in self.init_items:
            setattr(tb, attr, MagicMock())

        tb.set_state('init')

        for attr in self.init_items:
            current = getattr(tb, attr)
            expected_calls = [call.setEnabled(False), call.setEnabled(True)]
            print('Testing {}'.format(attr))
            current.assert_has_calls(expected_calls)

    def test_set_state_readonly(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for attr in self.readonly_items:
            setattr(tb, attr, MagicMock())

        tb.set_state('readonly')

        for attr in self.readonly_items:
            current_attr = getattr(tb, attr)
            expected_calls = [call.setEnabled(False), call.setEnabled(True)]
            print('Testing {}'.format(attr))
            current_attr.assert_has_calls(expected_calls)

    def test_set_state_editor(self):
        with_ramp = True
        tb = RoadnetToolbar(self.iface, './', with_ramp)
        for attr in self.editor_items:
            setattr(tb, attr, MagicMock())

        tb.set_state('editor')

        for attr in self.editor_items:
            current_attr = getattr(tb, attr)
            expected_calls = [call.setEnabled(False), call.setEnabled(True)]
            print('Testing {}'.format(attr))
            current_attr.assert_has_calls(expected_calls)

if __name__ == '__main__':
    unittest.main()
