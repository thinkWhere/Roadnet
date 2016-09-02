import datetime
import os
import subprocess
from textwrap import dedent
import unittest
import xml.etree.ElementTree as ETree

import boto3
from mock import MagicMock, mock_open, Mock, patch, call
import Roadnet.bin.deploy as deploy


class TestDeploy(unittest.TestCase):

    def test_write_plugins(self):
        with patch.object(deploy, 'dt') as dt:
            with patch.object(deploy, 'write_plugin') as write_plugin:
                dt.datetime.now.return_value = datetime.datetime(2015, 4, 5, 12, 0)
                build_name = 'build_99'
                version = 'testtesttest'
                deploy.write_plugins_xml(build_name, version)
                args, kwargs = write_plugin.call_args
                output_xml = args[0]

        # Parse xml and check correct values are inserted
        root = ETree.fromstring(output_xml)
        for plugin in root.findall('pyqgis_plugin'):
            attrib_version = plugin.get('version')
            download_url = plugin.find('download_url').text
            body_version = plugin.find('version').text
            update_date = plugin.find('update_date').text
        self.assertEqual(
            attrib_version, version,
            "Version in plugin attributes was "
            "not {} ({})".format(version, attrib_version))
        expected_url = (
            "http://roadnet-builds.s3-website-eu-west-1.amazonaws.com/"
            "build_99/Roadnet.zip")
        self.assertEqual(
            download_url, expected_url,
            "Incorrect download URL in plugin attributes ({})".format(
                download_url))
        self.assertEqual(
            body_version, version,
            "Version in plugin body was "
            "not {} ({})".format(version, body_version))
        expected_date = '2015-04-05'
        self.assertEqual(
            update_date, expected_date,
            "Update date in plugin attributes was "
            "not {} ({})".format(expected_date, update_date))

    def test_drop_unwanted(self):
        file_list = ['fred', '.gitignore', 'tests/my_test.py', 'binary.py']
        new_list = deploy.drop_unwanted_files(file_list)
        expected = ['fred', 'binary.py']
        self.assertEqual(new_list, expected,
                         "New list != {} ({})".format(expected, new_list))

    def test_get_file_list_no_git(self):
        with patch.object(subprocess, 'check_output') as check_output:
            check_output.side_effect = subprocess.CalledProcessError(0, Mock())
            with self.assertRaises(subprocess.CalledProcessError):
                deploy.get_file_list()

    def test_get_file_list_git_works(self):
        with patch.object(subprocess, 'check_output') as check_output:
            git_files_str = 'x.py\ny.py\n'
            check_output.return_value = git_files_str
            expected = ['x.py', 'y.py']
            result = deploy.get_file_list()
            self.assertEqual(
                expected, result,
                "Result was not {} ({})".format(expected, result))

    def test_update_repos_no_branch(self):
        deploy.boto = Mock()
        with patch.object(os, 'getenv') as getenv:
            with patch.object(deploy, 'deploy_to_s3') as deploy_to_s3:
                getenv.return_value = None
                build_name = 'testtesttest'
                deploy.update_repos(build_name)
                call_count = deploy_to_s3.call_count
                self.assertEqual(
                    call_count, 2,
                    "deploy_to_s3 not called 2 time ({})".format(call_count))

    def test_update_repos_is_pull_request(self):
        deploy.boto = Mock()
        with patch.object(os, 'getenv') as getenv:
            with patch.object(deploy, 'deploy_to_s3') as deploy_to_s3:
                getenv.side_effect = ['true', 'master']
                build_name = 'testtesttest'
                deploy.update_repos(build_name)
                call_count = deploy_to_s3.call_count
                self.assertEqual(
                    call_count, 0,
                    "deploy_to_s3 should not be called for "
                    "pull request commit".format(call_count))

    def test_update_repos_master_branch(self):
        deploy.boto = Mock()
        with patch.object(os, 'getenv') as getenv:
            with patch.object(deploy, 'deploy_to_s3') as deploy_to_s3:
                getenv.side_effect = ['false', 'master']
                build_name = 'testtesttest'
                deploy.update_repos(build_name)

                deploy_to_s3.assert_has_calls([call('testtesttest'),
                                               call('latest_push'),
                                               call('latest_master')])

    def test_update_repos_develop_branch(self):
        deploy.boto = Mock()
        with patch.object(os, 'getenv') as getenv:
            with patch.object(deploy, 'deploy_to_s3') as deploy_to_s3:
                getenv.side_effect = ['false', 'develop']
                build_name = 'testtesttest'
                deploy.update_repos(build_name)

                deploy_to_s3.assert_has_calls([call('testtesttest'),
                                               call('latest_push'),
                                               call('latest_develop')])

    def test_update_metadata(self):
        with patch.object(deploy, 'replace_line_in_file') as replace_line:
            deploy.update_metadata('testtesttest')
            args, kwargs = replace_line.call_args
            expected = ('metadata.txt', 'version=', 'version=testtesttest')
            self.assertEqual(expected, args,
                             "replace_line_in_file was not called with "
                             "{} ({})".format(expected, args))

    def test_disable_debug_mode(self):
        with patch.object(deploy, 'replace_line_in_file') as replace_line:
            deploy.disable_debug_mode()
            args, kwargs = replace_line.call_args
            expected = ('config.py', 'DEBUG_MODE', 'DEBUG_MODE = False')
            self.assertEqual(expected, args,
                             "replace_line_in_file was not called with "
                             "{} ({})".format(expected, args))

    def test_replace_line_in_file(self):
        file_lines = dedent("""\
            one
            change_me
            two""")
        filename = 'test.txt'
        line_start = 'change_me'
        replacement = 'line is changed'
        m = mock_open(read_data=file_lines)
        with patch('Roadnet.bin.deploy.open', m, create=True):
            print(__name__)
            deploy.replace_line_in_file(filename, line_start, replacement)

        self.assertEqual(len(m.call_args_list), 2,
                         "File not opened twice ({} times)".format(m.call_count))

        in_call, out_call = m.call_args_list
        in_file = in_call[0][0]
        out_file = out_call[0][0]
        self.assertEqual(in_file, filename,
                         "Input file was not {} ({})".format(filename, in_file))
        self.assertEqual(out_file, filename,
                         "Output file was not {} ({})".format(filename, out_file))

        handle = m()  # Handle required to access write method
        output_lines = [line[0][0] for line in handle.write.call_args_list]
        expected = ['one\n', replacement + '\n', 'two']
        self.assertItemsEqual(
            output_lines, expected,
            "Output lines were not'{}' ({})".format(expected, output_lines))

    def test_clean_up(self):
        with patch.object(os, 'remove') as mock_remove:
            deploy.clean_up()
            remove_calls = [arg[0][0] for arg in mock_remove.call_args_list]
            expected = ['Roadnet.zip', 'plugins.xml']
            self.assertItemsEqual(
                remove_calls, expected,
                'Files removed were not {} ({})'.format(expected, remove_calls))

    @patch.object(boto3, 'client')
    def test_deploy_to_s3(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        build_name = 'testtesttest'
        deploy.deploy_to_s3(build_name)

        mock_s3.assert_has_calls(
            [call.upload_file('Roadnet.zip', 'roadnet-builds',
                              'testtesttest/Roadnet.zip'),
             call.upload_file('plugins.xml', 'roadnet-builds',
                              'testtesttest/plugins.xml')],
            any_order=False)


if __name__ == '__main__':
    unittest.main()
