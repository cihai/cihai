# -*- coding: utf8 - *-
"""For accessing vcspull as a package.

libunihan.unihan
~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, with_statement

from pkg_resources \
    import resource_filename  # @UnresolvedImport #pylint: disable=E0611
import zipfile
import csv


def get_datafile(file_):
    return resource_filename(__name__, 'data/' + file_)


def main():
    print('%s' % get_datafile('Unihan.zip'))
    z = zipfile.ZipFile(get_datafile('Unihan.zip'))
    print([f.filename for f in z.filelist])

    with open(get_datafile('Unihan_Readings.txt'), 'rb') as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            print(', '.join(row))
