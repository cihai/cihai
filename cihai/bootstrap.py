# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from .util import merge_dict
from sqlalchemy import Column, String, Table

from unihan_etl.process import UNIHAN_MANIFEST
from unihan_etl import process as unihan


UNIHAN_FILES = [
    'Unihan_DictionaryLikeData.txt',
    'Unihan_IRGSources.txt',
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

UNIHAN_ETL_DEFAULT_OPTIONS = {
    'input_files': UNIHAN_FILES,
    'fields': UNIHAN_FIELDS,
    'format': 'python',
    'expand': False
}


def bootstrap_unihan(metadata, options={}):
    """Download, extract and import unihan to database."""
    options = merge_dict(UNIHAN_ETL_DEFAULT_OPTIONS.copy(), options)

    p = unihan.Packager(options)
    p.download()
    data = p.export()
    table = create_unihan_table(UNIHAN_FIELDS, metadata)
    metadata.create_all()
    metadata.bind.execute(table.insert(), data)


TABLE_NAME = 'Unihan'


def flatten_datasets(d):
    return sorted({c for cs in d.values() for c in cs})


DEFAULT_COLUMNS = ['ucn', 'char']
try:
    DEFAULT_FIELDS = [
        f for t, f in UNIHAN_MANIFEST.items() if t in ['Unihan']]
except:
    DEFAULT_FIELDS = [f for t, f in UNIHAN_MANIFEST.items()]


def is_bootstrapped(metadata):
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_COLUMNS
    if TABLE_NAME in metadata.tables.keys():
        table = metadata.tables[TABLE_NAME]

        if set(fields) == set(c.name for c in table.columns):
            return True
        else:
            return False
    else:
        return False


def create_unihan_table(columns, metadata):
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

        return table
    else:
        return Table(TABLE_NAME, metadata)
