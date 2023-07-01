"""Cihai core functionality."""
import typing as t

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from cihai.types import ConfigDict

if t.TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.ext.automap import AutomapBase


class Database:
    """Cihai SQLAlchemy instance"""

    #: :class:`sqlalchemy.engine.Engine` instance.
    engine: "Engine"

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata: MetaData

    #: :class:`sqlalchemy.orm.session.Session` instance.
    session: Session

    #: :class:`sqlalchemy.ext.automap.AutomapBase` instance.
    base: "AutomapBase"

    def __init__(self, config: ConfigDict) -> None:
        self.engine = create_engine(config["database"]["url"])

        self.metadata = MetaData()
        self.reflect_db()

        self.session = Session(self.engine)

    def reflect_db(self) -> None:
        """
        No-op to reflect db info.

        This is available as a method so the database can be reflected
        outside initialization (such bootstrapping unihan during CLI usage).
        """
        self.metadata.reflect(bind=self.engine, views=True, extend_existing=True)
        self.base = automap_base(metadata=self.metadata)
        self.base.prepare()
