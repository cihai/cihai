"""Cihai core functionality."""
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class Database(object):
    """
    Cihai SQLAlchemy instance
    """

    def __init__(self, config):
        self.engine = create_engine(config['database']['url'])

        self.metadata = MetaData()
        self.metadata.bind = self.engine
        self.reflect_db()

        self.session = Session(self.engine)

    def reflect_db(self):
        """
        No-op to reflect db info.

        This is available as a method so the database can be reflected
        outside initialization (such bootstrapping unihan during CLI usage).
        """
        self.metadata.reflect(views=True, extend_existing=True)
        self.base = automap_base(metadata=self.metadata)
        self.base.prepare()

    #: :class:`sqlalchemy.engine.Engine` instance.
    engine = None

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata = None

    #: :class:`sqlalchemy.orm.session.Session` instance.
    session = None

    #: :class:`sqlalchemy.ext.automap.AutomapBase` instance.
    base = None
