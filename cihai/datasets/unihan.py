# -*- coding: utf8 - *-
"""Cihai dataset for `Unihan`_, Han Unification from Unicode, Inc.

cihai.datasets.unihan
~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import hashlib
import logging

from sqlalchemy import Table, String, Column, Integer, Index

from .. import conversion
from ..cihai import cihai_config, cihai_db, CihaiDatabase
from ..util import get_datafile, UnicodeReader
from .._compat import PY2, text_type, configparser

__copyright__ = 'Copyright 2013 Tony Narlock.'
__license__ = 'BSD, see LICENSE for details.'

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


class Unihan(CihaiDatabase):

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

    """

    def install(self, csv_filename=None):
        """Install the raw csv information into CSV, return table.

        :param csv_filename: (optional, default=None) filename in /data dir.
        :type csv_filename: string
        :rtype: :class:`sqlalchemy.schema.Table`

        """

        if not csv_filename:
            return self.install(UNIHAN_FILENAMES)
        elif isinstance(csv_filename, list):
            for csv_filename in csv_filename:
                return self.install(csv_filename)

        table_name = csv_filename.split('.')[0]

        if not self.table_exists(table_name):

            table = self._create_table(table_name)
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

                    r = UnicodeReader(
                        csv_data,
                        fieldnames=['char', 'field', 'value'],
                        delimiter=delim
                    )
                    r = list(r)

                    results = self.metadata.bind.execute(table.insert(), r)
                    config.set(csv_filename, 'csv_rowcount', text_type(len(r)))
                else:
                    log.debug('Rows populated, all is well!')

                config.set(csv_filename, 'csv_md5', csv_md5)
                config_file = open(cihai_config, 'w+')
                config.write(config_file)
                config_file.close()
        else:
            log.debug('{0} already installed.'.format(table_name))
            table = self.get_table(table_name)

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

        if not table.exists():
            self.metadata.create_all()

        return table
