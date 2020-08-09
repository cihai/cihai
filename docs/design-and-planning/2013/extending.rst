:orphan:

.. _design-and-planning/2013/extending:

=========
Extending
=========

.. note::

    This document is part of brain storming the project of cihai. It's for
    historic purposes only.

*Written Late 2013*

Minimum usage
-------------

1. Create a python module
2. The module has a class with a ``get.()`` to look up characters by
   signature ``(request, response, *args, **kwargs)``.

With ``.get()``, your class may be instantiated and passed into ``Cihai``.
When a user runs ``.get()`` inside of ``Cihai``, it will check your
module's ``.get()`` also::

    +----------+
    | Cihai    |  The Cihai Class
    +----------+

It is instantiated with a database to connect to
(:class:`sqlalchemy.schema.MetaData`):

.. code-block:: python

    c = Cihai(metadata=metadata)

``MetaData`` is part of the sqlalchemy library. It holds connection and
table information. In this instance, cihai shares this information across
all plugins that attach to it.

To attach a plugin:

.. code-block:: python

    from MyCihaiModule import MyDataset
    mydata = MyDataSet()
    c.use(mydata)

``c``, the instance of :class:`Cihai`, may now access ``MyDataSet``'s
information.

Code
~~~~

.. code-block:: python

    c = Cihai()

    c.use(DatasetExample)
    print(c.reverse('hao'))
    >>> {
        'definition': 'hao'
    }

    print(c.get('你'))
    >>> {
        'definition': 'hao'
    }

Growing big
-----------

The above was an example of the minimum requirement to have your dataset
compatible.

Importing data into database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the goals of Cihai is to provide a common way to access to Chinese
data. To import the data, you must create an SQL schema / table for your
data.

The pristine format of your data may be in CSV, excel or another format.
As long as your data is normalized into a :obj:`dict` that is compatible
with the sql table, it is ok.

To accomodate this, :class:`Cihai` provides all plugins a instance of
:class:`sqlalchemy.schema.MetaData` on creation. `sqlalchemy`_ is the
swiss army knife of databases in the python programming language.

With an instance of ``MetaData``, you will be able to create SQL tables,
import and retrieve data.

Deeper
~~~~~~

In previous examples, the plugin class with ``.get`` and ``.reverse``
character lookups was merged with 1 SQL table.

As said previously, it doesn't matter how or where the data comes from.
As long as :class:`Cihai` can retrieve data via ``.get`` with the correct
arguments and response. The prior example had the data class combined with
a single table.

In databases that use multiple tables, you may create a central dataset
class with ``.get()`` and access the tables from there.

.. _sqlalchemy: http://www.sqlalchemy.org
