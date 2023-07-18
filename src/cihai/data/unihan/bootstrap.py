import dataclasses
import typing as t

import sqlalchemy
import sqlalchemy.sql.schema
from sqlalchemy import Column, String, Table

from unihan_etl import core as unihan
from unihan_etl.constants import UNIHAN_MANIFEST
from unihan_etl.util import merge_dict

from .constants import UNIHAN_ETL_DEFAULT_OPTIONS, UNIHAN_FIELDS

if t.TYPE_CHECKING:
    from unihan_etl.options import Options as UnihanOptions


def bootstrap_unihan(
    engine: sqlalchemy.Engine,
    metadata: sqlalchemy.sql.schema.MetaData,
    options: t.Optional[t.Union[t.Dict[str, object], "UnihanOptions"]] = None,
) -> None:
    if options is None:
        options = {}

    """Download, extract and import unihan to database."""
    options = merge_dict(
        UNIHAN_ETL_DEFAULT_OPTIONS.copy(),
        options if isinstance(options, dict) else dataclasses.asdict(options),
    )

    unihan_pkgr = unihan.Packager(options)
    unihan_pkgr.download()
    data = unihan_pkgr.export()
    table = create_unihan_table(UNIHAN_FIELDS, metadata)

    metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(sqlalchemy.insert(table), data)
        conn.commit()


TABLE_NAME = "Unihan"


DEFAULT_COLUMNS = ["ucn", "char"]
try:
    DEFAULT_FIELDS = [f for c, f in UNIHAN_MANIFEST.items() if c in ["Unihan"]]
except Exception:
    DEFAULT_FIELDS = list(UNIHAN_MANIFEST.values())


def is_bootstrapped(metadata: sqlalchemy.sql.schema.MetaData) -> bool:
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_COLUMNS
    if TABLE_NAME in metadata.tables:
        table = metadata.tables[TABLE_NAME]

        return set(fields) == {c.name for c in table.columns}
    else:
        return False


def create_unihan_table(
    columns: t.List[str], metadata: sqlalchemy.sql.schema.MetaData
) -> sqlalchemy.sql.schema.Table:
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

        table.append_column(Column("char", String(12), primary_key=True))
        table.append_column(Column("ucn", String(12), primary_key=True))

        for column_name in columns:
            col = Column(column_name, String(256), nullable=True)
            table.append_column(col)

        return table
    else:
        return Table(TABLE_NAME, metadata)
