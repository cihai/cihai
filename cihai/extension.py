# -*- coding: utf8 - *-
"""
Cihai Extension System

Status: Experimental, API can change

As a pilot, the UNIHAN library, and an extension for it, in #131 [1]_

You can bring any data layout / backend you like to cihai.

For convenience, you can use cihai's configuration namespace and
SQLAlchemy settings.

You can also create extensions which extend another. So if Unihan
doesn't have a lookup for variant glyphs, this can be added.

Extensions
----------
The provisional recommended naming convention is this:

cihai_{dataset}(?_{extension})
cihai_unihan
cihai_unihan_variants

Benefits
--------
Automatic configuration
Datasets are automatically namespaced as configs. Recipricocally, they have access to
the instance of cihai's configuration.

With the database mixin, your dataset can be automatically configured and work with
your user's configured DB backend. By default, it's SQLite! Reciprocally, you can also
access databases and tables connected to cihai.

c = Cihai()
c.add_dataset('unihan')  # install package
c.unihan.lookup('好')
# bootstraps
c.add_dataset('unihan', namespace='unihan2')  # install package
# checks
c.unihan2.lookup('好')

The optional namespace= allows for cihai to allow root-level access to datasets, while
being able to deprecate / move a dataset (however unlikely) if it were to conflict
with a new method name / property on the main cihai object.

It also allows namespacing a forked dataset, and adding it:

c.add_dataset('my_forked_unihan', namespace='unihan')  # install package

In the future, with libvcs:

c.add_dataset(Unihan, namespace='unihan')  # raw class

Future possibilities:

This makes it possible to develop locally, make a touch adjustment, maintain a VCS
branch, in the event a dataset fall out of sync or you want to hack on it / fork it.

c.add_dataset('package.to.unihan.Unihan', namespace='unihan')  # import string

Versioning
----------
Please provide a __version__ on your package if you distribute it. This is to make
sure cihai <-> dataset <-> extension have the fresh / new features and data, but can
also lock API's so production cases don't break.

Extending datasets
------------------
You can also create packages, or even pure functions, that extend datasets.

Extensions for datasets have access to the dataset's configuration, the sqlalchemy
database (if it used it), and any other data-access it made available. For instance,
if it had a custom data backend, it could make that available to the extension for
it to use.

c.add_dataset('unihan')
c.unihan.add_extension(Variants)

The same optional namespace= is possible:

c.unihan.variants.lookup('好')

c.unihan.add_extension(Variants, namespace='variants2')

c.unihan.variants2.lookup('好')

For the first draft, pointing straight to the package -> module -> object via import
string it the surest thing (since this is compatible with the user's local python
package environment and works well regardless of developing or general usage):

c.unihan.add_extension('package.to.import.unihan.Unihan')

This is similar to the way FLASK_CONFIG points to an object inside of a python module.

Todo
----
- Allow cihai to install packages via pip.

History
-------
Early cihai ideas made SQLAlchemy a requirement.

The initial plan was to keep everything under a single namespace, database, and be
able to reduce queries by building big queries. This is phased out in turn of making
cihai easy to hack on.

Idea: pip-based add_dataset/add_extension
-----------------------------------------
For development / hacking purposes, all of the same file, and vcs
still exist:

# import string
c.add_dataset('package.to.unihan', classname='Unihan', namespace='unihan')
c.add_dataset(
    'git+https://github.com/moo/cihai-unihan#test-branch',
    classname='Unihan',
    namespace='unihan'
)
c.add_dataset('./path/to/dataset', classname='Unihan', namespace='unihan')

c.unihan.add_extension('cihai_unihan_variants')
c.unihan.add_extension(
    'git+https://github.com/moo/cihai-unihan#test-branch', namespace='unihan'
)
c.unihan.add_extension('./path/to/dataset', classname=Unihan, namespace='unihan')

Idea: Namespacing
-----------------
Of the now, the idea is to avoid overengineering / bureaucracy caused by adopting
setuptools namespacing. Be like Django, which doesn't enforce package naming.

cihai.extensions.datasetname.extensionname, but that has difficulties [2]_

This namespace / organzation makes it possible for cihai to detect. [3]_

cihai-contrib makes packages available under cihaicontrib, similar to sphinx-contrib's
structure [4]_ uses Python's namespaces [5]_

See Also
--------
.. [1] Add variant methods. Github issues for cihai.
   https://github.com/cihai/cihai/pull/131. Accessed September 1st, 2018.
.. [2] Flask's deprecration of flask.ext and flask_ext:
   http://flask.pocoo.org/docs/1.0/extensiondev/
.. [3] Sphinx extensions
   http://www.sphinx-doc.org/en/master/extdev/index.html#dev-extensions.
.. [4]
   https://github.com/sphinx-contrib/documentedlist/tree/master/sphinxcontrib
"""
from __future__ import absolute_import, print_function, unicode_literals

from enum import Enum


from ._compat import with_metaclass


class DatasetConfigMixin(object):
    """
    This piggybacks cihai's global config state, as well as your datasets.

    Cihai will automatically manage the user's config, as well as your datasets,
    neatly in XDG.

    Raises
    -------
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
        instnace if you want a platform to use a different db driver, or do version
        checks, etc.)

        internal functions use get_default_config()
    """
    pass


class DatasetSQLAlchemyMixin(object):
    """Your dataset can use any backend you'd like, we provide a backend for you, that
    automatically piggybacks on cihai's zero-config, XDG / SQLAchemy configuration. So
    it's preconfigured for the user.

    In addition, this mixin gives you access to any other of the user's sqlalchemy 
    sql that use this mixin. So if you want a dataset that utilitizes UNIHAN, you can
    access that easily.

    This will provide the following instance-level properties in methods:

    When you have access, it's expected to keep your tables / databases namespaced so
    they don't clobber.
    """
    #: :class:`sqlalchemy.engine.Engine` instance.
    engine = None

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata = None

    #: :class:`sqlalchemy.orm.session.Session` instance.
    session = None

    #: :class:`sqlalchemy.ext.automap.AutomapBase` instance.
    base = None

    def bootstrap(self):
        pass

    def check(self):
        pass

    def db(self):
        pass


class Dataset(object):
    """Core for a dataset, e.g. UNIHAN."""

    def bootstrap(self):
        pass

    def add_extension(self, _cls, namespace):
        setattr(self, namespace, _cls())
        dataset = getattr(self, namespace)

        if hasattr(self, 'sql') and isinstance(dataset, DatasetSQLAlchemyMixin):
            dataset.sql = self.sql

        if hasattr(dataset, 'bootstrap') and callable(dataset.bootstrap):
            dataset.bootstrap()

    def check(self):
        """Can check to see if bootstrapped, can be updated."""
        raise NotImplemented

    def get_config(self):
        raise NotImplemented


class Stability(Enum):
    """Based on PyPI trove classifiers [1]_.

    See Also
    --------
    .. [1] PyPI Trove Classifiers. https://pypi.org/pypi?%3Aaction=list_classifiers.
       Accessed September 1st, 2018.
    .. [2] Node.js Stability Index. https://nodejs.org/api/documentation.html.
       https://nodejs.org/api/documentation.html
    """
    Planning = 1
    PreAlpha = 2
    Alpha = 3
    Beta = 4
    Draft = 4
    Production = 5 # Production/Stable
    Mature = 6
    Inactive = 0  # This is 7 on PyPI

    def is_stable(self):
        return self > 5


class Unihan(Dataset, DatasetConfigMixin, DatasetSQLAlchemyMixin):
    """Example dataset"""
    version = '0.1'

    # optional: stability
    # This helps you inform a user that extends / works with your dataset that your
    # backend is subject to change. Make this stable sends a signal you're going to
    # stick with it (or at least, you're going to continue to service / provide 
    # compatiblity / security / bug fixes into the future.
    stability_level = Stability.Draft


class ExtensionMeta(type):
    """Core metaclass for an extension"""


class ExtensionBase(object):
    pass


class Extension(with_metaclass(ExtensionMeta, ExtensionBase)):
    def bootstrap(self):
        pass

    @property
    def config(self):
        """Easy access to config."""
        return self.get_config()
