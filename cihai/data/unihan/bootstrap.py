from sqlalchemy import Column, String, Table

from unihan_etl import process as unihan
from unihan_etl.process import UNIHAN_MANIFEST

from ...utils import merge_dict
from .constants import UNIHAN_ETL_DEFAULT_OPTIONS, UNIHAN_FIELDS


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
    DEFAULT_FIELDS = [f for t, f in UNIHAN_MANIFEST.items() if t in ['Unihan']]
except Exception:
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

    Parameters
    ----------
    columns : list
        columns for table, e.g. ``['kDefinition', 'kCantonese']``
    metadata : :class:`sqlalchemy.schema.MetaData`
        Instance of sqlalchemy metadata

    Returns
    -------
    :class:`sqlalchemy.schema.Table` :
        Newly created table with columns and index.
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
