#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""China fit in to a python package.

Cihai
-----

:class:`Cihai` is a python client for accessing relational CJK datasets.

Cihai also includes utilities for converting current datasets into relational
data (for query by SQL, joins, etc.).

Internals
~~~~~~~~~

An instance of ``Cihai`` may use one or more ``dataset``. The dataset
provides a primary datasource (from the internet, or a CSV) in form friendly
to relational databases.

.. code-block:: python

    from cihai import Cihai
    from cihai.datasets.unihan import Unihan

    c = Cihai()  # creates a new Cihai instance.
    c.use(Unihan())  # Cihai to use Unihan plugin.

A new cihai instance is bound to :class:`sqlalchemy.schema.MetaData` - this
holds database connection information and :class:`sqlalchemy.schema.Table`'s.

This means plugins like :class:`~.datasets.unihan.Unihan` have full access to
relational sqlalchemy MetaData.

:copyright: Copyright 2013-2014 Tony Narlock.
:license: BSD, see LICENSE for details

"""
