"""
Cihai Plugin System

Status: Experimental, API can change

As a pilot, the UNIHAN library, and an plugin for it, in #131 [1]_

You can bring any data layout / backend you like to cihai.

For convenience, you can use cihai's configuration namespace and SQLAlchemy settings.

You can also create plugins which extend another. So if Unihan doesn't have a lookup
for variant glyphs, this can be added.
"""
import typing as t

from . import utils

if t.TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.ext.automap import AutomapBase
    from sqlalchemy.orm.session import Session
    from sqlalchemy.sql.schema import MetaData

    from cihai.db import Database

    DSP = t.TypeVar("DSP", bound=t.Type["DatasetPlugin"])


class ConfigMixin:
    """
    This piggybacks cihai's global config state, as well as your datasets.

    Cihai will automatically manage the user's config, as well as your datasets,
    neatly in XDG.

    Raises
    ------
    Functions inside, and what you write relating to dataset config should return

    CihaiDatasetConfigException (CihaiDatasetException)

    config.cihai = links directly back to Cihai's configuration dictionary
    (todo note: make this non-mutable property)

    config : dict
        your local user's config

    check() : function, optional
        this is ran on start. it can raise DatasetConfigException

    default_config : your dataset's default configuration

    get_default_config : override function in case you'd like custom configs (for
        instance if you want a platform to use a different db driver, or do version
        checks, etc.)

        internal functions use get_default_config()
    """


class SQLAlchemyMixin:
    """Your dataset can use any backend you'd like, we provide a backend for you, that
    automatically piggybacks on cihai's zero-config, XDG / SQLAchemy configuration. So
    it's preconfigured for the user.

    In addition, this mixin gives you access to any other of the user's sqlalchemy
    sql that use this mixin. So if you want a dataset that utilizes UNIHAN, you can
    access that easily.

    This will provide the following instance-level properties in methods:

    When you have access, it's expected to keep your tables / databases namespaced so
    they don't clobber.
    """

    sql: "Database"

    #: :class:`sqlalchemy.engine.Engine` instance.
    engine: "Engine"

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata: "MetaData"

    #: :class:`sqlalchemy.orm.session.Session` instance.
    session: "Session"

    #: :class:`sqlalchemy.ext.automap.AutomapBase` instance.
    base: "AutomapBase"


class Dataset:
    """
    Cihai dataset, e.g. UNIHAN.

    See Also
    --------
    cihai.data.unihan.dataset.Unihan : reference implementation
    """

    def bootstrap(self) -> None:
        pass

    def add_plugin(
        self,
        _cls: t.Union["DSP", str],
        namespace: str,
        bootstrap: bool = True,
    ) -> None:
        cls = utils.import_string(_cls) if isinstance(_cls, str) else _cls
        setattr(self, namespace, cls())
        plugin = getattr(self, namespace)

        if hasattr(self, "sql") and isinstance(self, SQLAlchemyMixin):
            plugin.sql = self.sql

        if bootstrap and hasattr(plugin, "bootstrap") and callable(plugin.bootstrap):
            plugin.bootstrap()


class DatasetPlugin:
    """
    Extend the functionality of datasets with custom methods, actions, etc.

    See Also
    --------
    cihai.data.unihan.dataset.UnihanVariants : reference implementation
    """
