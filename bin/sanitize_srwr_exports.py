#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import sys


def main():
    """
    Read CSV file and write output to new file
    :return:
    """
    print(sys.argv)

    infile = sys.argv[1]
    directory, name = os.path.split(infile)
    basename, extension = os.path.splitext(name)
    outfile = os.path.join(directory, basename + '_nocount' + extension)

    drop_count_column_and_sort(infile, outfile)


def drop_count_column_and_sort(infile, outfile):
    with open(infile, 'r') as src:
        with open(outfile, 'w') as dest:
            reader = csv.reader(src)

            rows = []
            for row in reader:
                # Drop row with column count
                row = row[:2] + row[3:]
                # Type 14 have no date in old version
                if row[0] == '14':
                    row = row[:6] + ['', '', '']
                rows.append(row)

            rows.sort()
            writer = csv.writer(dest)
            writer.writerows(rows)


if __name__ == "__main__":
    main()