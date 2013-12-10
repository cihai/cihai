# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_sqlalchemy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Index

from .helpers import TestCase, unittest
from .._compat import PY2
from ..unihan import get_datafile, UnihanReader

log = logging.getLogger(__name__)

sqlite_db = get_datafile('unihan.db')


def csv_to_table(engine, csv_file, table_name, fields):
    """Create table from CSV.

    :param engine: sqlalchemy engine
    :type engine: :sqlalchemy:class:`sqlalchemy.engine.Engine`
    :param csv_file: csv file
    :type csv_file: string
    :param table_name: name of table
    :type table_name: string
    :param fields: csv / table fields and sqlalchemy type.
        from ``sqlalchemy.types``.
    :type fields: tuple

    """

    metadata = MetaData(bind=engine)

    table = Table(table_name, metadata)

    col = Column('id', Integer, primary_key=True)
    table.append_column(col)

    field_names = [field for (field, t) in fields]
    field_types = {
        'string': String(256)
    }

    for (field, type_) in fields:
        col = Column(field, field_types[type_])
        table.append_column(col)

    Index('unique', table.c.char, table.c.char, table.c.value, unique=True)

    if os.path.exists(sqlite_db):
        print('db exists: %s' % sqlite_db)
    try:
        if table.exists():
            # print('table exists')
            pass
        if not table.exists():
            # print('table does not exist. create.')
            table.create()

            pass
    except Exception as e:
        print(e)
        table.create()

    with open(csv_file, 'r') as csvfile:

        delim = b'\t' if PY2 else '\t'
        csvfile = filter(lambda row: row[0] != '#', csvfile)
        r = UnihanReader(
            csvfile,
            fieldnames=['char', 'field', 'value'],
            delimiter=delim
        )

        r = list(r)[:500]

        for row in r:
            try:
                table.insert().execute(row)
            except Exception as e:
                print(e)
                print(row)
                print(type(row['char']), type(row['field']), type(row['value']))
            #table.insert().execute(dict(zip(field_names, row)))


class UnihanSQLAlchemy(TestCase):

    @unittest.skip('Postpone until CSV reader decodes and returns Unicode')
    def test_create_data(self):

        if not os.path.exists(sqlite_db):
            pass

        engine = create_engine('sqlite:///%s' % sqlite_db, echo=True)
        csv_to_table(
            engine=engine,
            csv_file=get_datafile('Unihan_Readings.txt'),
            table_name='Unihan',
            fields=[
                ('char', 'string'),
                ('field', 'string'),
                ('value', 'string')
            ]
        )

        with open(get_datafile('Unihan_Readings.txt'), 'r') as csvfile:
            # py3.3 regression http://bugs.python.org/issue18829
            delim = b'\t' if PY2 else '\t'
            csvfile = filter(lambda row: row[0] != '#', csvfile)
            r = UnihanReader(
                csvfile,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )

            r = list(r)[:5]
            print('\n')

            for row in r:
                rowlines = []
                for key in row.keys():
                    rowlines.append(row[key])
                try:
                    rowline = '\t'.join(rowlines)
                except UnicodeDecodeError as e:
                    log.info('row: %s (%s) gives:\n%s' % (row, row['char'], e))

                print('%s' % rowline)
