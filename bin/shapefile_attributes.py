#! /usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import shutil
import subprocess
import sys
import tempfile

"""
Script to get attributes from shapefile
"""


def main():
    """
    Open shape file, convert to csv, get attributes, print to stdout
    """
    infiles = sys.argv[1:]
    for f in infiles:
        print("-----------------------------\n{}\n".format(f))
        try:
            attr = get_ogr2csv(f)
            for row in attr:
                print("|".join(row))
                print("\n")
        except IOError:
            print("No features.\n")
            raise


def get_ogr2csv(shp_file_path):
    """
    Get shapefile attributes using ogr2ogr to convert to csv.
    :param shp_file_path: File path for *.shp
    :return: List of csv rows of shapefile attributes
    """
    csv_file_path = "{}.csv".format(shp_file_path[:-4])
    export_shapefile_to_csv(shp_file_path, csv_file_path)
    attr = get_attributes(csv_file_path)

    return attr


def export_shapefile_to_csv(shp_file_path, csv_file_path):
    """
    Use ogr2ogr to export shapefile as csv
    :param shp_file_path:
    :param csv_file_path:
    """
    cmd = ['ogr2ogr', '-f', 'CSV', csv_file_path, shp_file_path, '-overwrite']
    subprocess.check_call(cmd)


def get_attributes(csv_file_path):
    """
    Read csv file attributes
    :param csv_file_path: Path to csv file
    :return: List of csv rows (tuples)
    """
    with open(csv_file_path) as infile:
        reader = csv.reader(infile)
        reader.next()  # skip header row
        attr = [row for row in reader]

    return attr


if __name__ == '__main__':
    main()
