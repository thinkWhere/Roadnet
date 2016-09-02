#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys


def main():
    """
    Print the number of records of different types in an SDTF file
    """

    infile = sys.argv[1]

    record_types = [10, 11, 12, 13, 14, 15, 29, 99]
    for record_type in record_types:
        count = count_records(record_type, infile)
        print("Type {}: {}".format(record_type, count))


def count_records(record_type, infile):
    """
    Call subprocess and BASH shell commands to count records of given type.
    :param record_type: int, record type
    :param infile: path to file
    :return: int, number of records
    """
    cmd = "cat {} | grep -e '^{}' | wc -l".format(infile, record_type)
    result = subprocess.check_output(cmd, shell=True)

    return int(result)


if __name__ == "__main__":
    main()
