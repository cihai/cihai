# -*- coding: utf8 - *-
"""For accessing vcspull as a package.

libunihan.unihan
~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, with_statement

import os
import zipfile
import csv

from . import conversion


def get_datafile(file_):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/', file_)


def unichr3(*args):
    return [unichr(int(i[2:7], 16)) for i in args if i[2:7]][0]


def main():
    print('%s' % get_datafile('Unihan.zip'))
    z = zipfile.ZipFile(get_datafile('Unihan.zip'))
    print([f.filename for f in z.filelist])

    with open(get_datafile('Unihan_Readings.txt'), 'rb') as csvfile:
        csvfile = filter(lambda row: row[0] != '#', csvfile)
        #r = csv.reader(csvfile)
        r = UnihanReader(
            csvfile,
            fieldnames=['char', 'field', 'value'],
            delimiter='\t'
        )

        r = list(r)[:5]

        for row in r:
            rowlines = []
            for key in row.keys():
                rowlines.append(row[key])
            try:
                rowline = '\t'.join(rowlines)
            except UnicodeDecodeError as e:
                print(
                    'row: %s (%s) gives:\n%s' % (
                        row, row['char'], e
                    )
                )

            print('%s\n' % rowline)


class UnihanReader(csv.DictReader):
    def __init__(self, *args, **kwargs):
        csv.DictReader.__init__(self, *args, **kwargs)

    def next(self):
        row = csv.DictReader.next(self)
        for key in self.fieldnames:
            if None:
                row[key] = unichr3(row[key])

        if row['char'].startswith('U+'):
            row['char'] = conversion.ucn_to_python(row['char'])

        if (
            row['field'] == 'kDefinition' or
            row['field'] == 'kMandarin'
        ):
            row['value'] = row['value'].decode('utf-8')

        return row

#  _neilg | borneo: you should be able to use regular expressions to convert
#  U+([a-f0-9]+)\b to \U[a-f0-9]{8}
