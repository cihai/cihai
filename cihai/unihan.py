# -*- coding: utf8 - *-
"""Unihan file parsing, importing and codec handling.

cihai.unihan
~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import zipfile
import csv
import logging
import hashlib

from sqlalchemy import create_engine, MetaData, Table, String, Column, \
    Integer, Index

from . import conversion
from .cihai import cihai_config, cihai_db, engine
from .util import get_datafile
from ._compat import PY2, text_type, configparser

log = logging.getLogger(__name__)

UNIHAN_FILENAMES = [
    'Unihan_DictionaryIndices.txt',
    'Unihan_DictionaryLikeData.txt',
    'Unihan_IRGSources.txt',
    'Unihan_NumericValues.txt',
    'Unihan_OtherMappings.txt',
    'Unihan_RadicalStrokeCounts.txt',
    'Unihan_Readings.txt',
    'Unihan_Variants.txt'
]


def get_metadata():
    """Return new MetaData object."""
    metadata = MetaData(bind=engine)
    metadata.reflect()

    return metadata


def get_table(table_name):
    """Return :class:`~sqlalchemy.schema.Table`.

    :param table_name: name of sql table
    :type table_name: string
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    table = Table(table_name, get_metadata(), autoload=True)

    return table


def table_exists(table_name):
    """Return True if table exists in unihan.db."""

    table = Table(table_name, get_metadata())

    return table.exists()


def check_raw_install():
    """Verify csv information from Unihan is installed in unihan.db."""
    config = configparser.ConfigParser()

    if not os.path.exists(cihai_config):
        install_raw_csv()

    config.read(cihai_config)

    for csv_filename in UNIHAN_FILENAMES:
        if not config.has_section(csv_filename):
            install_raw_csv(csv_filename)


def install_raw_csv(csv_filename=None):
    """Install the raw csv information into CSV, return table.

    :param csv_filename: filename in /data dir.
    :type csv_filename: string
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    if not csv_filename:
        return install_raw_csv(UNIHAN_FILENAMES)
    elif isinstance(csv_filename, list):
        for csv_filename in csv_filename:
            return install_raw_csv(csv_filename)
    else:
        table_name = csv_filename.split('.')[0]

        if not table_exists(table_name):

            table = csv_to_table(
                engine=engine,
                csv_filename=csv_filename,
                table_name=table_name,
            )
        else:
            log.debug('{0} already installed.'.format(table_name))
            table = get_table(table_name)
        return table


def csv_to_table(engine, csv_filename, table_name):
    """Create table from CSV.

    :param engine: sqlalchemy engine
    :type engine: :class:`sqlalchemy.engine.Engine`
    :param csv_filename: csv file name inside data, e.g. ``Unihan_Readings.txt``.
    :type csv_filename: string
    :param table_name: name of table
    :type table_name: string
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    table = create_table(table_name, engine)
    unihan_csv = get_datafile(csv_filename)

    with open(unihan_csv, 'r') as csv_file:
        csv_md5 = hashlib.sha256(unihan_csv.encode('utf-8')).hexdigest()
        csv_data = filter(lambda row: row[0] != '#', csv_file)
        delim = b'\t' if PY2 else '\t'

        config = configparser.ConfigParser()
        config.read(cihai_config)
        if not config.has_section(csv_filename):
            config.add_section(csv_filename)

        if (
            not os.path.exists(cihai_config) or
            not config.has_option(csv_filename, 'csv_rowcount') or
            (
                config.has_option(csv_filename, 'csv_rowcount') and
                table.select().count().execute().scalar() != config.getint(csv_filename, 'csv_rowcount')
            )
        ):

            r = RawReader(
                csv_data,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )
            r = list(r)

            results = engine.execute(table.insert(), r)
            config.set(csv_filename, 'csv_rowcount', text_type(len(r)))
        else:
            log.debug('Rows populated, all is well!')

        config.set(csv_filename, 'csv_md5', csv_md5)
        config_file = open(cihai_config, 'w+')
        config.write(config_file)
        config_file.close()
    return table


def create_table(table_name, engine):
    """Create table and return  :sqlalchemy:class:`sqlalchemy.Table`.

    :param table_name: name of table to create
    :type table_name: string
    :param engine: sqlalchemy engine
    :type engine: :sqlalchemy:`sqlalchemy.Engine`
    :returns: Newly created table with columns and index.
    :rtype: :class:`sqlalchemy.schema.Table`

    """
    metadata = MetaData(bind=engine)
    table = Table(table_name, metadata)
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

    if not table.exists():
        table.create()

    return table


class RawReader(csv.DictReader):
    """Read from Unihan CSV resource."""
    def __init__(self, *args, **kwargs):
        csv.DictReader.__init__(self, *args, **kwargs)

    def __next__(self):
        row = csv.DictReader.__next__(self)

        return self.row(row)

    def next(self):
        row = csv.DictReader.next(self)

        return self.row(row)

    def row(self, row):
        for key in row.keys():
            if not isinstance(row[key], text_type):
                row[key] = text_type(row[key].decode('utf-8'))

        return row


class UnihanReader(csv.DictReader):
    """Read from Unihan CSV resource."""
    def __init__(self, *args, **kwargs):
        csv.DictReader.__init__(self, *args, **kwargs)

    def __next__(self):
        row = csv.DictReader.__next__(self)

        return self.row(row)

    def next(self):
        row = csv.DictReader.next(self)

        return self.row(row)

    def row(self, row):
        if row['char'].startswith('U+'):
            row['char'] = conversion.ucn_to_unicode(row['char'])

        if not isinstance(row['field'], text_type):
            try:
                row['field'] = text_type(row['field'])
            except UnicodeDecodeError as e:
                log.info(row['field'])
                raise e
        return row
