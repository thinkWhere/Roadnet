from textwrap import dedent
import unittest
import xml.etree.ElementTree as ETree

from mock import call, patch, MagicMock, mock_open, sentinel

from Roadnet.tests.integration.roadnet_test_cases import QgisTestCase
import Roadnet.params_and_settings as p_and_s


class TestParamsFileHandler(unittest.TestCase):
    def setUp(self):
        xml_string = """
        <TwParams>
        <Application id="Roadnet">
            <Parameter name="RNDataStorePath">/home/tw-johns/Roadnet/database_files</Parameter>
            <Parameter name="DbName">roadnet_demo.sqlite</Parameter>
            <Parameter name="RNPolyEdit">true</Parameter>
            <Parameter name="RNsrwr">true</Parameter>
            <Parameter name="Language">ENG</Parameter>
            <Parameter name="UserName">thinkwhere</Parameter>
            <Parameter name="Blank"></Parameter>
        </Application>
        </TwParams>"""
        xml_string = dedent(xml_string)
        self.test_root = ETree.fromstring(xml_string)

    def test_init(self):
        file_path = 'testtesttest'
        pfh = p_and_s.ParamsFileHandler(file_path)
        self.assertEqual(
            pfh.xmlfile_path, file_path,
            "xmlfile_path was not {} ({})".format(
                file_path, pfh.xmlfile_path))

    @patch.object(p_and_s.ParamsFileHandler, '_update_tree')
    def test_read_to_dictionary(self, mock_update_tree):
        file_path = 'testtesttest'
        pfh = p_and_s.ParamsFileHandler(file_path)
        pfh.root = self.test_root
        params = pfh.read_to_dictionary()
        expected = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                    "DbName": 'roadnet_demo.sqlite',
                    "RNPolyEdit": 'true',
                    "RNsrwr": 'true',
                    "Language": 'ENG',
                    "UserName": 'thinkwhere'}

        mock_update_tree.assert_called_once_with()
        for key in expected:
            self.assertEqual(
                params[key], expected[key],
                "Wrong value read for params {}: {}, not {}".format(
                    key, params[key], expected[key]))

    @patch.object(p_and_s.ParamsFileHandler, '_update_tree')
    def test_update_xml_file(self, mock_update_tree):
        file_path = 'testtesttest'
        pfh = p_and_s.ParamsFileHandler(file_path)
        pfh.root = self.test_root
        pfh.tree = MagicMock()
        test_params = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                    "DbName": 'roadnet_demo.sqlite',
                    "RNPolyEdit": 'true',
                    "Language": 'ENG',
                    "RNsrwr": 'true',
                    "Blank": 'true',
                    "UserName": 'thinkwhere',
                    "ShouldNotBeUsed": 'should not appear in output'}
        m = mock_open()
        with patch('Roadnet.params_and_settings.open', m, create=True):
            pfh.update_xml_file(test_params)
            # Check that the file is opened
            m.assert_called_once_with(file_path, 'w')
            mock_outfile = m()
            # Check data is written to correct file
            pfh.tree.assert_has_calls([call.write(mock_outfile)])

    @patch.object(p_and_s.os.path, 'isfile')
    @patch.object(p_and_s.rn_except.QMessageBoxWarningError, 'show_message_box')
    @patch.object(p_and_s.ParamsFileHandler, 'read_to_dictionary')
    def test_validate_missing_fields(self,
                                     mock_read_dictionary,
                                     mock_show_warning,
                                     mock_isfile):
        file_path = 'testtesttest'
        test_params = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                       "DbName": 'roadnet_demo.sqlite',
                       "RNPolyEdit": 'true',
                       "RNsrwr": 'true',
                       "Blank": 'true',
                       "UserName": 'thinkwhere',
                       "RAMP_output_directory": '',
                       "PreventOverlappingPolygons": 'true',
                       "ShouldNotBeUsed": 'should not appear in output'}
        mock_isfile.return_value = True
        mock_read_dictionary.return_value = test_params
        pfh = p_and_s.ParamsFileHandler(file_path)

        with self.assertRaises(p_and_s.rn_except.InvalidParamsKeysPopupError):
            pfh.validate_params_file()

    @patch.object(p_and_s.os.path, 'isfile')
    @patch.object(p_and_s.rn_except.QMessageBoxWarningError, 'show_message_box')
    @patch.object(p_and_s.ParamsFileHandler, 'read_to_dictionary')
    def test_validate_extra_fields(self,
                                   mock_read_dictionary,
                                   mock_show_warning,
                                   mock_isfile):
        file_path = 'testtesttest'
        test_params = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                       "DbName": 'roadnet_demo.sqlite',
                       "RNPolyEdit": 'true',
                       "RNsrwr": 'true',
                       "Language": 'EN',
                       "RAMP": 'true',
                       "RAMP_output_directory": '',
                       "AutoSplitESUs": 'true',
                       "Blank": 'true',
                       "UserName": 'thinkwhere',
                       "PreventOverlappingPolygons": 'true',
                       "ShouldNotBeUsed": 'should not appear in output'}
        mock_isfile.return_value = True
        mock_read_dictionary.return_value = test_params
        pfh = p_and_s.ParamsFileHandler(file_path)

        with self.assertRaises(p_and_s.rn_except.ExtraParamsKeysPopupError):
            pfh.validate_params_file()

    @patch.object(p_and_s.os.path, 'isfile')
    @patch.object(p_and_s.rn_except.QMessageBoxWarningError, 'show_message_box')
    def test_validate_missing_file(self,
                                   mock_show_warning,
                                   mock_isfile):
        file_path = 'testtesttest'
        mock_isfile.return_value = False
        pfh = p_and_s.ParamsFileHandler(file_path)

        with self.assertRaises(p_and_s.rn_except.MissingParamsFilePopupError):
            pfh.validate_params_file()


class TestSettingsDialogHandler(QgisTestCase):
    @patch.object(p_and_s, 'SettingsDlg')
    def test_settings_dialog_created(self, mock_dlg):
        params = {'test': 123}
        settings_dialog_handler = p_and_s.SettingsDialogHandler(params)
        mock_dlg.assert_called_once_with()

    @patch.object(p_and_s.SettingsDialogHandler,
                  'show_ramp_settings_changed_warning')
    @patch.object(p_and_s.SettingsDialogHandler, 'get_params_from_checkboxes')
    @patch.object(p_and_s, 'SettingsDlg')
    def test_update_via_dialog(self, mock_dlg, mock_get_params, mock_warning):
        checkbox_params = {"AutoSplitESUs": 'true',
                           "PreventOverlappingPolygons": 'false',
                           "RAMP": 'true'}
        mock_get_params.return_value = checkbox_params
        test_input = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                      "DbName": 'roadnet_demo.sqlite',
                      "RNPolyEdit": 'true',
                      "RNsrwr": 'true',
                      "Language": 'ENG',
                      "UserName": 'thinkwhere',
                      "AutoSplitESUs": 'false',
                      "PreventOverlappingPolygons": 'true',
                      "RAMP": 'false'}
        expected = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                    "DbName": 'roadnet_demo.sqlite',
                    "RNPolyEdit": 'true',
                    "RNsrwr": 'true',
                    "Language": 'ENG',
                    "UserName": 'thinkwhere',
                    "AutoSplitESUs": 'true',
                    "PreventOverlappingPolygons": 'false',
                    "RAMP": 'true'}
        settings_handler = p_and_s.SettingsDialogHandler(test_input)
        params = settings_handler.show_dialog_and_update_params()

        # Check results
        for key in expected:
            self.assertEqual(expected[key], params[key],
                             "{} parameter was not updated to {} ({})".format(
                                 key, expected[key], params[key]))
        mock_warning.assert_called_once_with(checkbox_params)

    @patch.object(p_and_s, 'SettingsDlg')
    def test_checkboxes_updated_from_params(self, mock_settings_dlg):
        mock_dlg = MagicMock()
        mock_settings_dlg.return_value = mock_dlg
        test_params = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                       "AutoSplitESUs": 'false',
                       "PreventOverlappingPolygons": 'true',
                       "RAMP": 'true'}
        settings_dialog_handler = p_and_s.SettingsDialogHandler(test_params)
        settings_dialog_handler.set_checkboxes_from_params()
        expected_calls = [call.ui.esuCheckBox.setChecked(False),
                          call.ui.rdpolyCheckBox.setChecked(True),
                          call.ui.rampCheckBox.setChecked(True)]
        mock_dlg.assert_has_calls(expected_calls, any_order=True)

    @patch.object(p_and_s, 'SettingsDlg')
    def test_checkboxes_updated_from_params_raises_value_error(
            self, mock_settings_dlg):
        mock_dlg = MagicMock()
        mock_settings_dlg.return_value = mock_dlg
        test_params = {"RNDataStorePath": '/home/tw-johns/Roadnet/database_files',
                       "AutoSplitESUs": 'false',
                       "PreventOverlappingPolygons": 'true',
                       "RAMP": 'test'}
        with self.assertRaises(ValueError):
            settings_dialog_handler = p_and_s.SettingsDialogHandler(test_params)
            settings_dialog_handler.set_checkboxes_from_params()

    @patch.object(p_and_s, 'SettingsDlg')
    def test_get_params_from_checkboxes(self, mock_settings_dlg):
        mock_dlg = MagicMock()
        mock_dlg.ui.esuCheckBox.isChecked.return_value = True
        mock_dlg.ui.rdpolyCheckBox.isChecked.return_value = False
        mock_dlg.ui.rampCheckBox.isChecked.return_value = True
        mock_settings_dlg.return_value = mock_dlg
        expected = {"AutoSplitESUs": 'true',
                    "PreventOverlappingPolygons": 'false',
                    "RAMP": 'true'}

        input_params = {'test': 123}
        settings_dialog_handler = p_and_s.SettingsDialogHandler(input_params)
        params = settings_dialog_handler.get_params_from_checkboxes()
        for key in expected:
            self.assertEqual(expected[key], params[key],
                             "{} checkbox was not {} ({})".format(
                                 key, expected[key], params[key]))

if __name__ == '__main__':
    unittest.main()
