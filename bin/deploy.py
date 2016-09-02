#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a script for packaging roadNet and deploying it to an AWS repository.

It is run by the continuous integration system following a successful build.

Files are copied to _repository_files_ directory.
"""

import datetime as dt
import os
import subprocess
from textwrap import dedent
import zipfile
import boto3

# Get environment variables used for AWS deployment.  These are stored as
# encrypted variables within the Shippable continuous integration system.

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

ZIPFILE_NAME = 'Roadnet.zip'


def main():
    # Update files with versions and dates
    build_name, version = get_build_and_version()
    update_metadata(version)
    write_plugins_xml(build_name, version)
    disable_debug_mode()

    # Package roadNet files into zip
    all_files = get_file_list()
    package_file_list = drop_unwanted_files(all_files)
    write_zipfile(ZIPFILE_NAME, package_file_list)

    # Deploy
    update_repos(build_name)
    clean_up()


def get_build_and_version():
    """
    Return timestamp in seconds since epoch as int for version number
    :return:
    """
    branch = os.getenv('BRANCH', 'local')
    build = os.getenv('BUILD_NUMBER', '0')
    commit = os.getenv('COMMIT', 'aaaaaaaa')[:8]

    build_name = '{}_{}'.format(build, branch)
    version = '{}_{}'.format(build_name, commit)
    return build_name, version


def get_file_list():
    """
    Read a list of relative paths from the .git database.
    """
    try:
        git_files_str = subprocess.check_output(['git', 'ls-files'], shell=False)
    except subprocess.CalledProcessError as err:
        print("Can't get file list from git ({})".format(err))
        raise

    git_files_str = git_files_str.strip()
    file_list = [f.strip() for f in git_files_str.split('\n')]
    return file_list


def drop_unwanted_files(file_list):
    """
    Drop files that we don't want to include in the package.
    :param file_list: files and directories to exclude.
    """
    original_list = file_list
    files_to_drop = [os.path.join('database_files', 'roadnet.sqlite'),
                     '.gitignore',
                     'scratch_space.py',
                     'setup.cfg',
                     'shippable.yml'
                     ]

    directories_to_drop = ['docker',
                           'plugin_packager',
                           'tests',
                           'bin'
                           ]

    for directory in directories_to_drop:
        directory += '/'
        files_to_drop.extend([f for f in original_list if
                              f.startswith(directory)])

    new_list = [f for f in original_list if f not in files_to_drop]
    return new_list


def disable_debug_mode():
    """
    Set DEBUG_MODE flag to False in config.py.
    """
    debug_false_line = 'DEBUG_MODE = False'
    replace_line_in_file('config.py', 'DEBUG_MODE', debug_false_line)


def update_metadata(version):
    """
    Rewrites metadata.txt with the new version number replaced.
    :param version: string with branch and build
    """
    new_version_line = 'version={}'.format(version)
    replace_line_in_file('metadata.txt', 'version=', new_version_line)


def replace_line_in_file(filename, line_start, replacement):
    """
    Rewrite a file, replacing a specific line with another.
    :param filename: file to update
    :param line_start: opening characters of line to replace
    :param replacement: string of replacement line
    """
    with open(filename, 'r') as f:
        original_text = f.readlines()
    with open(filename, 'w') as f:
        for line in original_text:
            if line.startswith(line_start):
                line = replacement + '\n'
            f.write(line)


def write_plugins_xml(build_name, version):
    """"
    Write a plugins.xml file with new version number.
    :build_name: string with branch and build
    :param version: string with branch and build and commit
    :param build_name: string with branch and build
    """
    now = dt.datetime.now().strftime('%Y-%m-%d')
    xml_string = """\
        <?xml version = '1.0' encoding = 'UTF-8'?>
        <?xml-stylesheet type='text/xsl' href='/plugins.xsl' ?>
        <plugins>
          <pyqgis_plugin name='Roadnet' version='{version}'>
            <description>Roadnet is a tool used for maintaining a local street gazetteer.</description>
            <version>{version}</version>
            <qgis_minimum_version>2.14</qgis_minimum_version>
            <homepage>http://www.thinkwhere.com</homepage>
            <file_name>Roadnet.zip</file_name>
            <author_name>thinkWhere</author_name>
            <download_url>http://roadnet-builds.s3-website-eu-west-1.amazonaws.com/{build_name}/Roadnet.zip</download_url>
            <uploaded_by>thinkWhere</uploaded_by>
            <create_date>2014-12-09</create_date>
            <update_date>{update_date}</update_date>
          </pyqgis_plugin>
        </plugins>
    """.format(version=version, update_date=now, build_name=build_name)
    xml_string = dedent(xml_string)
    write_plugin(xml_string)


def write_plugin(xml_string):  # pragma: no cover
    with open('plugins.xml', 'wt') as f:
        f.write(xml_string)


def write_zipfile(outzipfile, file_list):
    """
    Write files to to a Roadnet folder within the zip file.
    :param outzipfile: path for zip file
    :param file_list: list of files to include
    """
    with zipfile.ZipFile(outzipfile, mode='w') as zf:
        for name in file_list:
            name_in_zip = 'Roadnet/{}'.format(name)
            zf.write(name, name_in_zip)


def update_repos(build_name):
    """
    Create new repo for build, and update latest master/dev repos.
    :param build_name:
    :return:
    """
    if os.getenv('IS_PULL_REQUEST') == 'true':
        # Don't deploy when Shippable builds pull request preview
        return

    deploy_to_s3(build_name)
    deploy_to_s3('latest_push')

    branch = os.getenv('BRANCH')
    if branch is None:
        return
    elif branch == 'develop':
        deploy_to_s3('latest_develop')
    elif branch == 'RAMP':
        deploy_to_s3('latest_RAMP')
    elif branch == 'master':
        deploy_to_s3('latest_master')


def deploy_to_s3(build_name):
    """
    Upload the files to the s3 bucket at
    http://roadnet-builds.s3-website-eu-west-1.amazonaws.com/

    Bucket was created using AWS web interface.  It needed to be set as
    public and an index.html file was uploaded.
    :param build_name: string with branch and build
    """
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    files_for_repo = ['Roadnet.zip', 'plugins.xml']
    for file_name in files_for_repo:
        path_on_s3 = '{}/{}'.format(build_name, file_name)
        s3.upload_file(file_name, 'roadnet-builds', path_on_s3)


def clean_up():
    os.remove('Roadnet.zip')
    os.remove('plugins.xml')


if __name__ == '__main__':
    main()
