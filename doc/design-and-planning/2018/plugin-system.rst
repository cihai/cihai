:orphan:

.. _design-and-planning/2018/plugin-system:

Extensions
----------
Initially discussed in #131 [1]_

The provisional recommended naming convention is this:

::

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

.. code-block:: python

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

.. code-block:: python

   c.add_dataset('my_forked_unihan', namespace='unihan')  # install package

In the future, with libvcs:

.. code-block:: python

   c.add_dataset(Unihan, namespace='unihan')  # raw class

Future possibilities:

This makes it possible to develop locally, make a touch adjustment, maintain a VCS
branch, in the event a dataset fall out of sync or you want to hack on it / fork it.

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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
   Accessed September 1st, 2018.
.. [3] Sphinx extensions
   http://www.sphinx-doc.org/en/master/extdev/index.html#dev-extensions.
   Accessed September 1st, 2018.
.. [4] sphinx-contrib
   https://github.com/sphinx-contrib/documentedlist/tree/master/sphinxcontrib
   Accessed September 1st, 2018.
.. [5] Python namespaces.
   https://packaging.python.org/guides/packaging-namespace-packages/
   Accessed September 7th, 2018.
