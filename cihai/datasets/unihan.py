# -*- coding: utf8 - *-
"""Cihai dataset for `Unihan`_, Han Unification from Unicode, Inc.

cihai.datasets.unihan
~~~~~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import sys
import glob
import hashlib
import fileinput
try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve
import logging

from sqlalchemy import Table, String, Column, Integer, Index, select, or_, and_

from .. import conversion
from ..cihai import cihai_config, cihai_db, CihaiDataset
from ..util import get_datafile, UnicodeReader
from .._compat import PY2, text_type, configparser

__copyright__ = 'Copyright 2013 Tony Narlock.'
__license__ = 'BSD, see LICENSE for details.'

log = logging.getLogger(__name__)

# This is the Unihan_DictionaryLikeData as of 6.3.0
# The format is { 'FILENAME': ['fields'] }
UNIHAN_DATASETS = {
    'Unihan_DictionaryIndices.txt': [
        'kCheungBauerIndex',
        'kCowles',
        'kDaeJaweon',
        'kFennIndex',
        'kGSR',
        'kHanYu',
        'kIRGDaeJaweon',
        'kIRGDaiKanwaZiten',
        'kIRGHanyuDaZidian',
        'kIRGKangXi',
        'kKangXi',
        'kKarlgren',
        'kLau',
        'kMatthews',
        'kMeyerWempe',
        'kMorohashi',
        'kNelson',
        'kSBGY',
    ],
    'Unihan_DictionaryLikeData.txt': [
        'kCangjie',
        'kCheungBauer',
        'kCihaiT',
        'kFenn',
        'kFourCornerCode',
        'kFrequency',
        'kGradeLevel',
        'kHDZRadBreak',
        'kHKGlyph',
        'kPhonetic',
        'kTotalStrokes',
    ],
    'Unihan_IRGSources.txt': [
        'kIICore',
        'kIRG_GSource',
        'kIRG_HSource',
        'kIRG_JSource',
        'kIRG_KPSource',
        'kIRG_KSource',
        'kIRG_MSource',
        'kIRG_TSource',
        'kIRG_USource',
        'kIRG_VSource',
    ],
    'Unihan_NumericValues.txt': [
        'kAccountingNumeric',
        'kOtherNumeric',
        'kPrimaryNumeric',
    ],
    'Unihan_OtherMappings.txt': [
        'kBigFive',
        'kCCCII',
        'kCNS1986',
        'kCNS1992',
        'kEACC',
        'kGB0',
        'kGB1',
        'kGB3',
        'kGB5',
        'kGB7',
        'kGB8',
        'kHKSCS',
        'kIBMJapan',
        'kJis0',
        'kJis1',
        'kJIS0213',
        'kKPS0',
        'kKPS1',
        'kKSC0',
        'kKSC1',
        'kMainlandTelegraph',
        'kPseudoGB1',
        'kTaiwanTelegraph',
        'kXerox',
    ],
    'Unihan_RadicalStrokeCounts.txt': [
        'kRSAdobe_Japan1_6',
        'kRSJapanese',
        'kRSKangXi',
        'kRSKanWa',
        'kRSKorean',
        'kRSUnicode',
    ],
    'Unihan_Readings.txt': [
        'kCantonese',
        'kDefinition',
        'kHangul',
        'kHanyuPinlu',
        'kHanyuPinyin',
        'kJapaneseKun',
        'kJapaneseOn',
        'kKorean',
        'kMandarin',
        'kTang',
        'kVietnamese',
        'kXHC1983',
    ],
    'Unihan_Variants.txt': [
        'kCompatibilityVariant',
        'kSemanticVariant',
        'kSimplifiedVariant',
        'kSpecializedSemanticVariant',
        'kTraditionalVariant',
        'kZVariant',
    ]

}

UNIHAN_URL = 'http://www.unicode.org/Public/UNIDATA/Unihan.zip'
PACKAGE_DATA = []

thisdir = os.path.join(os.path.dirname(__file__))

datadir = os.path.join(thisdir, './cihai/data')

if not os.path.exists(datadir):
    os.makedirs(datadir)


def _dl_progress(count, block_size, total_size):
    """
    MIT License: https://github.com/okfn/dpm-old/blob/master/dpm/util.py
    """
    def format_size(bytes):
        if bytes > 1000 * 1000:
            return '%.1fMb' % (bytes / 1000.0 / 1000)
        elif bytes > 10 * 1000:
            return '%iKb' % (bytes / 1000)
        elif bytes > 1000:
            return '%.1fKb' % (bytes / 1000.0)
        else:
            return '%ib' % bytes

    if not count:
        print('Total size: %s' % format_size(total_size))
    last_percent = int((count - 1) * block_size * 100 / total_size)
    # may have downloaded less if count*block_size > total_size
    maxdownloaded = count * block_size
    percent = min(int(maxdownloaded * 100 / total_size), 100)
    if percent > last_percent:
        # TODO: is this acceptable? Do we want to do something nicer?
        sys.stdout.write(
            '%3d%% [%s>%s]\r' % (
                percent,
                int(percent / 2) * '=',
                int(50 - percent / 2) * ' '
            )
        )
        sys.stdout.flush()
    if maxdownloaded >= total_size:
        print('\n')


def save(url, filename):
    urlretrieve(url, filename, _dl_progress)

keys = ['char', 'field', 'value']
in_columns = lambda c, columns: c in columns
not_junk = lambda line: line[0] == '#' and line != '\n'


def download():
    import zipfile
    UNIHAN_DATAFILE = os.path.join(datadir, 'Unihan.zip')
    if not glob.glob(os.path.join(datadir, 'Unihan*.txt')):
        if not os.path.exists(os.path.join(datadir, 'Unihan.zip')):
            print('Downloading Unihan.zip...')
            save(UNIHAN_URL, UNIHAN_DATAFILE)
        try:
            z = zipfile.ZipFile(UNIHAN_DATAFILE)
        except zipfile.BadZipfile as e:
            print('%s. Unihan.zip incomplete or corrupt. Redownloading...' % e)
            save(UNIHAN_URL, UNIHAN_DATAFILE)
            z = zipfile.ZipFile(UNIHAN_DATAFILE)
        z.extractall(datadir)


def csv_to_dictlists(csv_files, columns):
    """Return dict from Unihan CSV files.

    :param csv_files: file names in data dir
    :type csv_files: list
    :return: List of tuples for data loaded

    """

    data = fileinput.FileInput(files=csv_files, openhook=fileinput.hook_encoded('utf-8'))
    items = []
    for l in data:
        if not_junk(l) and in_columns(l[1], columns):
            items.append(dict(zip(keys, l.strip().split('\t'))))

    return items
    # return [dict(zip(keys, l.strip().split('\t'))) for l in data if filter_junk(l)]
    # return [dict(zip(keys, l.strip().split('\t'))) for l in data if l[0] != '#' and l != '\n']


class Unihan(CihaiDataset):

    """Cihai dataset for `Unihan`_, Han Unification from Unicode, Inc.

    :meth:`~.install` creates the tables, :meth:`~.import_csv_to_table`
    dumps csv to database.

    This module is used by adding to a :class:`cihai.Cihai` instance:

    .. code-block:: python

        from cihai import Cihai

        c = Cihai()
        c.use(Unihan)
        c.get('好')
        >>> {
            'definition': 'good'
        }

    .. _Unihan: http://www.unicode.org/reports/tr38/

    :todo: Add a :obj:`dict` instance variable for the available lookups
        tables to search) and have a default that only searches certain keys.
    :todo: Specify desired result fields to search (e.g. 'kDefinition').

    """

    def __init__(self, cihai, engine, metadata, fields=None, *args, **kwargs):
        """Start an instance of Unihan to :meth:`~.get` or :meth:`reverse` data.

        :param fields: (optional, default: None) Unihan fields to search for by
            default. By default all columns in the installed CSV's are
            retrieved.
        :type fields: list

        """
        super(Unihan, self).__init__(cihai, engine, metadata)

        """
        from sqlalchemy.
            msg = "%s is not bound to an Engine or Connection.  "\
                   "Execution can not proceed without a database to execute "\
                   "against." % item
            bind = _bind_or_error(metadata,
                    msg="No engine is bound to this Table's MetaData. "
                    "Pass an engine to the Table via "
                    "autoload_with=<someengine>, "
                    "or associate the MetaData with an engine via "
                    "metadata.bind=<someengine>")
        """

        try:
            self.fields = [f for t, f in UNIHAN_DATASETS.items() if t in ['Unihan']]
        except:
            self.fields = [f for t, f in UNIHAN_DATASETS.items()]
        self.default_fields = self.fields

    def install(self, install_dict=None):
        """Install the raw csv information into CSV, return table.

        :param install_dict: (optional, default=None) filename in /data dir and
            the field names to install. You can view all in ``UNIHAN_DATASETS``
            installs all CSV's and fields by default.

            .. code-block:: python

                {
                    'Unihan_DictionaryIndices.txt': [
                        'kCheungBauerIndex',
                        'kCowles'
                    ],
                }

        :type csv_filename: dict
        :rtype: :class:`sqlalchemy.schema.Table`

        """

        if not install_dict:
            install_dict = UNIHAN_DATASETS

        table_name = 'Unihan'
        files = tuple(self.get_datapath(f) for f in install_dict.keys())

        columns = [col for csvfile, col in install_dict.items()]

        data = csv_to_dictlists(files, columns)

        table = self._create_table(table_name)

        def insert_rows(table_name, data, fields):

            andfields = [(table.c.field == t) for t in fields]
            andstmt = or_(*andfields)
            return self.metadata.bind.execute(table.insert(), data)

        insert_rows(table, data, self.fields)

        return table

    def _create_table(self, table_name):
        """Create table and return  :class:`sqlalchemy.Table`.

        :param table_name: name of table to create
        :type table_name: string
        :returns: Newly created table with columns and index.
        :rtype: :class:`sqlalchemy.schema.Table`

        """
        table = Table(table_name, self.metadata)
        fields = [
            ('char', String(12)),
            ('field', String(36)),
            ('value', String(256)),
        ]

        col = Column('id', Integer, primary_key=True)
        table.append_column(col)

        field_names = [field for (field, t) in fields]

        for (field, type_) in fields:
            col = Column(field, type_)
            table.append_column(col)

        Index('%s_unique_char_field_value' % table_name, table.c.char, table.c.field, table.c.value, unique=True)
        Index('%s_unique_char_field' % table_name, table.c.char, table.c.field, unique=True)
        Index('%s_field' % table_name, table.c.field)

        self.metadata.create_all()

        return table

    def get(self, request, response, *args, **kwargs):
        """Return chinese character data from Unihan data.

        :param request:
        :type request: string
        :param response:
        :type response: dict
        :param fields: (default:None) list of fields, e.g. ['kDefinition']
        :type fields: list
        :returns: Cihai response dictionary
        :rtype: dict

        """

        if not request.startswith('U+'):
            request = conversion.python_to_ucn(request)

        if not 'fields' in kwargs:
            fields = self.default_fields
        else:
            fields = kwargs['fields']

        table = Table('Unihan', self.metadata)
        andfields = [(table.c.field == t) for t in fields]
        andstmt = and_(*andfields)

        q = select([
            table.c.field
        ]).where(andstmt)

        query = select([table.c.value, table.c.char, table.c.field]).where(
            table.c.field == q,
        ).where(table.c.value == request)

        query = query.execute()

        if query:
            if not 'unihan' in response:
                response['unihan'] = {}
            for r in query:
                response['unihan'][r['field']] = r['value']

        if not response['unihan']:
            # don't return empty lists.
            del response['unihan']

        return response

    def reverse(self, request, response, *args, **kwargs):
        """Return reverse look-up of chinese characters from Unihan data.

        :param request:
        :type request: string
        :param response:
        :type response: dict
        :param fields: (default:None) list of fields, e.g. ['kDefinition']
        :type fields: list
        :returns: Cihai response dictionary
        :rtype: dict

        """

        if not 'fields' in kwargs:
            fields = self.default_fields
        else:
            fields = kwargs['fields']

        table = Table('Unihan', self.metadata)
        andfields = [(table.c.field == t) for t in fields]
        andstmt = and_(*andfields)

        q = select([
            table.c.field
        ]).where(andstmt)

        query = select([table.c.value, table.c.char, table.c.field]).where(
            table.c.field == q,
        ).where(table.c.value.like(request))

        query = query.execute()

        if query:
            if not 'unihan' in response:
                response['unihan'] = {}
            for r in query:
                char = conversion.ucn_to_unicode(r['char'])
                if not char in response['unihan']:
                    response['unihan'][char] = {}
                response['unihan'][char][r['field']] = r['value']

        if not response['unihan']:
            # don't return empty lists.
            del response['unihan']

        return response
