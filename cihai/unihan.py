# -*- coding: utf8 - *-
from sqlalchemy import Column, or_

from ._compat import string_types
from .conversion import parse_untagged, parse_vars
from .extension import Dataset, DatasetSQLAlchemyMixin, Extension




def mk_unihan(Base):
    class Unihan(Base):
        __tablename__ = 'unihan'

        def tagged_vars(self, col):
            """
            Return a variant column as an iterator of (char, tag) tuples.
            """
            return parse_vars(getattr(self, col))

        def untagged_vars(self, col):
            """
            Return a variant column as an iterator of chars.
            """
            return parse_untagged(getattr(self, col))

    return Unihan


class Unihan(Dataset, DatasetSQLAlchemyMixin):

    def __init__(self):
        from cihai.unihan import mk_unihan

    def bootstrap(self):
        self.sql.reflect_db()

    def lookup_char(self, char):
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

    def reverse_char(self, hints):
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
        if isinstance(hints, string_types):
            hints = [hints]

        Unihan = self.sql.base.classes.Unihan
        columns = Unihan.__table__.columns
        return self.sql.session.query(Unihan).filter(
            or_(*[column.contains(hint) for column in columns for hint in hints])
        )

    def with_fields(self, *fields):
        """Returns list of characters with information for certain fields.

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


class UnihanVariants(Extension):
    def tagged_vars(self, col):
        """
        Return a variant column as an iterator of (char, tag) tuples.
        """
        return parse_vars(getattr(self, col))

    def untagged_vars(self, col):
        """
        Return a variant column as an iterator of chars.
        """
        return parse_untagged(getattr(self, col))
