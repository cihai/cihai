"""Module for UNIHAN Dataset for cihai."""

import typing as t

from sqlalchemy import or_
from sqlalchemy.sql.schema import Column

from cihai.conversion import parse_untagged, parse_vars
from cihai.extend import Dataset, DatasetPlugin, SQLAlchemyMixin

from . import bootstrap

if t.TYPE_CHECKING:
    from sqlalchemy.orm.query import Query
    from sqlalchemy.sql.schema import Table

    from cihai.conversion import ParsedVars, UntaggedVars
    from unihan_etl.options import Options as UnihanOptions


class Unihan(Dataset, SQLAlchemyMixin):
    """UNIHAN Dataset for cihai."""

    char: str
    kDefinition: str
    kTraditionhalVariant: str
    kSimplifiedVariant: str
    tagged_vars: t.Callable[[str], "ParsedVars"]
    untagged_vars: t.Callable[[str], "UntaggedVars"]

    def bootstrap(
        self,
        options: t.Optional[t.Union[dict[str, object], "UnihanOptions"]] = None,
    ) -> None:
        """Fetch, extract, import UNIHAN to DB, and initialize DB mapping."""
        if options is None:
            options = {}

        bootstrap.bootstrap_unihan(
            engine=self.sql.engine,
            metadata=self.sql.metadata,
            options=options,
        )
        self.sql.reflect_db()  # automap new table created during bootstrap

    def lookup_char(self, char: str) -> "Query[Unihan]":
        """Return character information from datasets.

        Parameters
        ----------
        char : str
            character / string to lookup

        Returns
        -------
        :class:`sqlalchemy.orm.query.Query` :
            list of matches
        """
        Unihan = self.sql.base.classes.Unihan
        return self.sql.session.query(Unihan).filter_by(char=char)

    def reverse_char(self, hints: t.Union[str, list[str]]) -> "Query[Unihan]":
        """Return QuerySet of objects from SQLAlchemy of results.

        Parameters
        ----------
        hints: list of str
            strings to lookup

        Returns
        -------
        :class:`sqlalchemy.orm.query.Query` :
            reverse matches
        """
        if isinstance(hints, str):
            hints = [hints]

        Unihan = self.sql.base.classes.Unihan
        columns = Unihan.__table__.columns
        return self.sql.session.query(Unihan).filter(
            or_(*[column.contains(hint) for column in columns for hint in hints]),
        )

    def with_fields(self, fields: list[str]) -> "Query[Unihan]":
        """Return list of characters with information for certain fields.

        Parameters
        ----------
        *fields : list of str
            fields for which information should be available

        Returns
        -------
        :class:`sqlalchemy.orm.query.Query` :
            list of matches
        """
        Unihan = self.sql.base.classes.Unihan
        query = self.sql.session.query(Unihan)
        for field in fields:
            query = query.filter(Column(field).isnot(None))
        return query

    @property
    def is_bootstrapped(self) -> bool:
        """Return True if UNIHAN and database is set up.

        Returns
        -------
        bool :
            True if Unihan application fixture data installed.
        """
        return bootstrap.is_bootstrapped(self.sql.metadata)


class UnihanVariants(DatasetPlugin, SQLAlchemyMixin):
    """Support for CJK Variant lookups through UNIHAN dataset."""

    def bootstrap(self) -> None:
        """Map custom lookup for UNIHAN variants to Unihan SQLAlchemy table."""

        def tagged_vars(table: "Table", col: str) -> "ParsedVars":
            """Return a variant column as an iterator of (char, tag) tuples."""
            return parse_vars(getattr(table, col))

        def untagged_vars(table: "Table", col: str) -> "UntaggedVars":
            """Return a variant column as an iterator of chars."""
            return parse_untagged(getattr(table, col))

        if hasattr(self.sql.base.classes, "Unihan"):
            self.sql.base.classes.Unihan.tagged_vars = tagged_vars
            self.sql.base.classes.Unihan.untagged_vars = untagged_vars
