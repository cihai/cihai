#!/usr/bin/env python
# -*- coding: utf8 - *-
"""Cihai dataset for `Unihan`_, Han Unification from Unicode, Inc."""

import os
import sys
import zipfile
import glob
import hashlib
import fileinput

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    string_types = (str, unicode)
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve
    text_type = str
    string_types = (str,)

not_junk = lambda line: line[0] != '#' and line != '\n'
in_columns = lambda c, columns: c in columns + default_columns
default_columns = ['ucn', 'char']

def ucn_to_unicode(ucn):
    """Convert a Unicode Universal Character Number (e.g. "U+4E00" or "4E00") to Python unicode (u'\\u4e00')"""
    if isinstance(ucn, string_types):
        ucn = ucn.strip("U+")
        if len(ucn) > int(4):
            char = b'\U' + format(int(ucn, 16), '08x').encode('latin1')
            char = char.decode('unicode_escape')
        else:
            char = unichr(int(ucn, 16))
    else:
        char = unichr(ucn)

    assert isinstance(char, text_type)

    return char


def save(url, filename, urlretrieve=urlretrieve, reporthook=None):
    """Separate download function for testability.

    :param url: URL to download
    :type url: str
    :param filename: destination to download to.
    :type filename: string
    :param urlretrieve: function to download file
    :type urlretrieve: function
    :param reporthook: callback for ``urlretrieve`` function progress.
    :type reporthook: function
    :returns: Result of ``urlretrieve`` function

    """

    if reporthook:
        return urlretrieve(url, filename, reporthook)
    else:
        return urlretrieve(url, filename)


def download(url, dest, urlretrieve=urlretrieve, reporthook=None):
    """Download a file to a destination.

    :param url: URL to download from.
    :type url: str
    :param destination: file path where download is to be saved.
    :type destination: str
    :param reporthook: Function to write progress bar to stdout buffer.
    :type reporthook: function
    :returns: destination where file downloaded to
    :rtype: str

    """

    datadir = os.path.dirname(dest)
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    no_unihan_files_exist = lambda: not glob.glob(
        os.path.join(datadir, 'Unihan*.txt')
    )

    not_downloaded = lambda: not os.path.exists(
        os.path.join(datadir, 'Unihan.zip')
    )

    if no_unihan_files_exist():
        if not_downloaded():
            print('Downloading Unihan.zip...')
            if reporthook:
                save(url, dest, urlretrieve, reporthook)
            else:
                save(url, dest, urlretrieve)

    return dest


def extract(zip_filepath):
    """Extract zip file. Return :class:`zipfile.ZipFile` instance.

    :param zip_filepath: file to extract.
    :type zip_filepath: string
    :returns: The extracted zip.
    :rtype: :class:`zipfile.ZipFile`

    """

    datadir = os.path.dirname(zip_filepath)
    try:
        z = zipfile.ZipFile(zip_filepath)
    except zipfile.BadZipfile as e:
        print('%s. Unihan.zip incomplete or corrupt. Redownloading...' % e)
        download()
        z = zipfile.ZipFile(zip_filepath)
    z.extractall(datadir)

    return z


def convert(csv_files, columns):
    """Return dict from Unihan CSV files.

    :param csv_files: file names in data dir
    :type csv_files: list
    :return: List of tuples for data loaded

    """

    data = fileinput.FileInput(files=csv_files, openhook=fileinput.hook_encoded('utf-8'))
    items = {}
    for l in data:
        if not_junk(l):
            l = l.strip().split('\t')
            if in_columns(l[1], columns):
                item = dict(zip(['ucn', 'field', 'value'], l))
                char = ucn_to_unicode(item['ucn'])
                if not char in items:
                    items[char] = dict.fromkeys(columns)
                    items[char]['ucn'] = item['ucn']
                items[char][item['field']] = item['value']
    return items



