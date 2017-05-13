# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from . import conversion
from .util import merge_dict
from sqlalchemy import Column, Index, String, Table, and_, select

from unihan_tabular.process import UNIHAN_MANIFEST
from unihan_tabular import process as unihan


UNIHAN_FILES = [
    'Unihan_DictionaryLikeData.txt',
    'Unihan_NumericValues.txt',
    'Unihan_RadicalStrokeCounts.txt',
    'Unihan_Readings.txt', 'Unihan_Variants.txt'
]

UNIHAN_FIELDS = [
    'kAccountingNumeric', 'kCangjie', 'kCantonese', 'kCheungBauer',
    'kCihaiT', 'kCompatibilityVariant', 'kDefinition', 'kFenn',
    'kFourCornerCode', 'kFrequency', 'kGradeLevel', 'kHDZRadBreak',
    'kHKGlyph', 'kHangul', 'kHanyuPinlu', 'kHanyuPinyin',
    'kJapaneseKun', 'kJapaneseOn', 'kKorean', 'kMandarin',
    'kOtherNumeric', 'kPhonetic', 'kPrimaryNumeric',
    'kRSAdobe_Japan1_6', 'kRSJapanese', 'kRSKanWa', 'kRSKangXi',
    'kRSKorean', 'kRSUnicode', 'kSemanticVariant',
    'kSimplifiedVariant', 'kSpecializedSemanticVariant', 'kTang',
    'kTotalStrokes', 'kTraditionalVariant', 'kVietnamese', 'kXHC1983',
    'kZVariant'
]

UNIHAN_TABULAR_DEFAULT_OPTIONS = {
    'input_files': UNIHAN_FILES,
    'fields': UNIHAN_FIELDS,
    'format': 'python'
}


def bootstrap_unihan(metadata, options={}):
    """Download, extract and import unihan to database."""
    options = merge_dict(UNIHAN_TABULAR_DEFAULT_OPTIONS.copy(), options)

    p = unihan.Packager(options)
    p.download()
    print(p.options['fields'])
    # hi = p.export()


TABLE_NAME = 'Unihan'


def flatten_datasets(d):
    return sorted({c for cs in d.values() for c in cs})


DEFAULT_COLUMNS = ['ucn', 'char']
try:
    DEFAULT_FIELDS = [
        f for t, f in UNIHAN_MANIFEST.items() if t in ['Unihan']]
except:
    DEFAULT_FIELDS = [f for t, f in UNIHAN_MANIFEST.items()]


def is_bootstrapped(metadata, install_dict=None):
    """Return True if cihai is correctly bootstrapped."""
    if not install_dict:
        install_dict = UNIHAN_MANIFEST

    columns = flatten_datasets(install_dict) + DEFAULT_COLUMNS

    if TABLE_NAME in metadata.tables.keys():
        table = metadata.tables[TABLE_NAME]
        if set(columns) == set(c.name for c in table.columns):
            return True
        else:
            return False
    else:
        return False


def create_table(columns, metadata):
    """Create table and return  :class:`sqlalchemy.Table`.

    :param columns: columns for table, i.e. ['kDefinition', 'kCantonese']
    :type columns: list
    :param metadata: Instance of sqlalchemy metadata
    :type metadata: :class:`sqlalchemy.schema.MetaData`
    :returns: Newly created table with columns and index.
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    if TABLE_NAME not in metadata.tables:
        table = Table(TABLE_NAME, metadata)

        table.append_column(Column('char', String(12), primary_key=True))
        table.append_column(Column('ucn', String(12), primary_key=True))

        for column_name in columns:
            col = Column(column_name, String(256), nullable=True)
            table.append_column(col)

        Index('%s_unique_char' % TABLE_NAME, table.c.char, unique=True)
        Index(
            '%s_unique_char_ucn' % TABLE_NAME, table.c.char, table.c.ucn,
            unique=True
        )

        return table
    else:
        return Table(TABLE_NAME, metadata)


def get(char, metadata, **kwargs):
    if not char.startswith('U+'):
        char = conversion.python_to_ucn(char)

    if 'fields' not in kwargs:
        fields = DEFAULT_FIELDS
    else:
        fields = kwargs['fields']

    table = Table('Unihan', metadata)
    andfields = [(table.c.field == t) for t in fields]
    andstmt = and_(*andfields)

    q = select([
        table.c.field
    ]).where(andstmt)

    query = select([table.c.value, table.c.char, table.c.field]).where(
        table.c.field == q,
    ).where(table.c.value == char)

    query = query.execute()

    if query:
        response = {}
        for r in query:
            response[r['field']] = r['value']

    return response
