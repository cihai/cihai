:orphan:

.. _design-and-planning/2013/spec:

========
Planning
========

.. note::

    This document is part of brain storming the project of cihai. It's for
    historic purposes only.

*Written Late 2013*

Scribblings on cihai dev.

Configuration
-------------

It can accept a custom configuration file via command line with ``-c``:

.. code-block :: bash

    $ python -m cihai -c myconfig.yml

Where your configuration file overrides the default settings. You can see
the default settings in the ``cihai`` package as ``config.yml``.

Developers may use ``dev/config.yml``. The TestCase will use the
``test_config.yml``.

.. code-block:: bash

    $ python -m cihai

Will start up cihai with normal configuration settings. A configuration
file may also be used.

.. code-block:: bash

    $ python -m cihai -c dev/config.yml

History of CJK libraries
------------------------

Unihan
~~~~~~

Unihan, which is short for "Han Unification" is a standard published by the
Unicode Consortium for CJK ideographs (also interchangeable referred to as
"glyphs", "characters", "chars").

`Unihan's History`_ goes into greater detail on this. The first electronic
release was in July 1995 as `CJKXREF.TXT`_ (961 kB). The second release, which
resembles the formatting used in modern versions, was released in July 1996
with Unicode 2.0 as `Unihan-1.txt`_. In an accident, the ``Unihan-1.txt``
(7.9MB) file was missing the final pieces after ``U+8BC1``, no corrected
version was made availabe. In May 1998, `Unihan-2.txt`_ was released with
Unicode 2.1.2.

Unihan Inc. is the center of the universe for all glyphs. For those who study
Egyptian hieroglyphics, which are still mysterious, they are covered in
Unicode block `U+13000..U+1342F`_.

.. _U+13000..U+1342F: Fhttp://en.wikipedia.org/wiki/Egyptian_Hieroglyphs_(Unicode_block)
.. _Unihan's History: http://www.unicode.org/reports/tr38/#History
.. _CJKXREF.TXT: http://www.unicode.org/Public/1.1-Update/CJKXREF.TXT
.. _Unihan-1.txt: http://www.unicode.org/Public/2.0-Update/Unihan-1.txt
.. _Unihan-2.txt: http://www.unicode.org/Public/2.1-Update/Unihan-2.txt

cjklib
~~~~~~

`cjklib`_ is a major python library created by Christoph Burgmer for han
character research.

"Cjklib provides language routines related to Han characters (characters based
on Chinese characters named Hanzi, Kanji, Hanja and chu Han respectively) used
in writing of the Chinese, the Japanese, infrequently the Korean and formerly
the Vietnamese language(s). Functionality is included for character
pronunciations, radicals, glyph components, stroke decomposition and variant
information. Cjklib is implemented in Python."

.. cjklib: https://code.google.com/p/cjklib/

Cihai
~~~~~

Early iterations of Cihai focused on external API as a first. Every data set
was to be a plugin.

The idea was, `Hanzi`_, a similar project in nodejs could share a similar API
and datasets could be universal. The potential would be to provide two
high-quality libraries for python and node, which are extendable to new data
sets and reduce duplication.

It is better to take the time to discover the variable nature of datasets and
how they interconnect.

Current
~~~~~~~

The next iteration of cihai is to grasp an understand of:

- what different data sets look like, how they return data?
- is their commonality between all?
- how their results can illicit deeper research and exploring of chinese
  characters

This is an exploration phase.

External API
------------

Cihai Spec
~~~~~~~~~~

Both Cihai and Hanzi libraries can use a similar API.

- Reduce duplicated effort
- Provide a main, tested CJK library to Python and node
- Collaborate to assure both projects have access to open data sets and
  chinese character techniques.

Larger charter:

- Workgroup to develop a specification for core, pluggable CJK library
  across various programming languages.

  - follow best practices.
    
    - documentation
    - unit tests / ci
    - consistent with coding idiom's / pragmas (pythonic / pocoo / reits,
      connect / underscore / node)
  - be available on package archives (npm, pypi).
  - Across languages, core tools should have similar API method names,
    creating instance of data retrieval object
  - Extendable to new datasets as middleware.
  - Documentation for creating a new middleware.
- Find more data sets and encourage data providers / data owners to use an
  open data license.
- Find more libraries across various programming language with a CJK tool.
  
  - If project is a duplicate effort, notify that there is another
    effort underway and they can participate.
  - If project is a new tool:
    
    - see if they have a dataset. If it does, see license of ODC/OBDC.
    - see if their library is BSD or MIT. If not see if they're willing to
      license as such. *
    - see if they are willing to use the Workgroup's API specification.
    - If willing, but no time, offer to patch.
    - If not interested at all, create an adapter for the project as a
      separate effort.

* if the library is GPL, it can cause conflict down the road, if the
  project author does not have the time / interest in adopting
  specification, even creating an adapter to their project could trigger
  GPL.

Licensing
---------

Core software
~~~~~~~~~~~~~

BSD or MIT. The Core apps should be BSD 3-clause to protect the name of
the app (Cihai or Hanzi).

Extensions / Contrib licensing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Middleware can be included in the project as officially supported.
Contrib and third party plugins can be available under BSD or MIT.

Data sets
~~~~~~~~~

Data for chinese should be available under the most permissive license
possible.


How should data be looked up?
-----------------------------

I would like to try to encourage use of a single, simple hook,
``.get``.

After ``.get`` is used, the arguments may then be passed through
middleware classes / methods.

The same principle applies for ``.reverse`` matches.

Chinese character
~~~~~~~~~~~~~~~~~

Currently, Hanzi uses: 

.. code-block:: javascript

    hanzi.decompose('爱')

    // transition to:
    hanzi.get('爱')

    hanzi.reverse('爱')  // to look up any indices / decompositions / words
    where 爱 may match.

Currently cjklib uses:

.. code-block:: python

    cjk.getStrokeOrder(u'说')
    #  transition to:
    cjk.get('说')

.. code-block:: python

    Cihai.get('好')

String of Chinese Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``.get`` too. This may seem problematic, but checking the
``.length`` or ``len()`` of the argument can suffice.

.. code-block:: javascript

    var decomposition = hanzi.decomposeMany('爱橄黃');
    // transition to
    var decomposition = hanzi.get('爱橄黃');

.. code-block:: python

    Cihai.get('爱橄黃')

How should data returned look? Schema.
--------------------------------------

Questions:

- Is there already an open standard that can be adopted?
- Should ``.get`` return an raw object / dict or an object::

    c = c.get('你')  # return a ResultObject / Backbone.Model / mongoose
                     # document type of object.
    c.toJSON()  # backbone / sqlalchemy style

The data should follow the same schema. What would an API response for
these possibilities look like?

If something generic like .get() is entered,

- character decomposition
- a unihan field ('kDefinition', 'kStrokes', 'kFrequency', ...)
- https://github.com/tsroten/zhon
- https://github.com/fxsjy/jieba

If ``.get`` is the only way to retrieve hits, more possibilities
exist.

For hanzi/node:

.. code-block:: javascript

    results = hanzi.get('你好。怎么样？')

or for cihai/python:

.. code-block:: python

    results = cihai.get('你好。怎么样？')

May return hits jieba middleware (jieba doesn't exist in node yet)::

    results.words = [
    '你好',
    '怎么样'
    ]

The user may then further tool:

.. code-block:: python

    for word in results.words:
        print(cihai.get(word))

or

.. code-block:: javascript

    for _.each(results.words, function(word) {
        console.log(hanzi.get(word))
    });

.. warning::

    If dictionaries / datasets are extensible, there may be collision
    if they can reserve keys in the official result namespace.

Two plugins may could try to reserve ``.words`` as a name. Many
dictionaries would want to reserve ``.definition`` as a name.

To counteract this, a namespace can be adopted for middleware, we can have
the Core resolve the conflict:

1.  Append underscore + number on conflict, etc.
    (``c.definition_1``, ``c.definition_2``):
   
    The first middleware using ``words`` can get ``result.words``. The
    middleware called after will get ``results.words_1``.

    This is seen in `SQLAlchemy's labels`_ to `avoid label collisions`_.

2.  Middleware / datasets use namespace with ``_``
    (``c.unihan_kDefinition``):

    Pros:

    - iterable access to python ``c.keys()`` and ``for var key in dict``
      in js.
    - all data returned can be accessed without nesting into dotted
      namespaces.

    Cons:

    - ``result.unihan_kDefinition_these_things_getlong``
    - extension name and word separation can be confused.

3.  Middleware may use dot namespace (``c.unihan.kDefinition``)

    Pros:

    - Internal Core API is far simpler and lighter
    - Easier to look at
    - More common practice, `aws_cli`_.
    - Middleware is a package module, symbolically ``.``'s are used to
      separate modules and packages (java, python, informally in JS).

.. _SQLAlchemy's labels: https://github.com/zzzeek/sqlalchemy/blob/347e89044ce53ef0ec8d07937cd8279e9c4e5226/lib/sqlalchemy/sql/elements.py#L2393
.. _avoid label collisions: https://github.com/zzzeek/sqlalchemy/blob/347e89044ce53ef0ec8d07937cd8279e9c4e5226/test/sql/test_compiler.py#L2549
.. _aws_cli: https://github.com/aws/aws-cli

Extension philosophy
--------------------

The middleware approach provides the best practice to get the job done.

`Connect`_ in node represents the best practice in plugin architecture in
JS. Middleware is added as a way to provide a lite, dead-simple framework.

Cihai / Hanzi can take a similar approach.

Hanzi can take example directly from connect's approach. It is clean and
proven. Cihai can note middleware is already used in Django, packages can
be maintained using pattern for Flask extensions and sphinx. Flask already
has experience / lesson's heard from packaging and namespacing extensions.

It can use the same data sets, similar API and extension strategy.

.. _Connect: https://github.com/senchalabs/connect

Accessing extensions directly?
------------------------------

Perhaps extensions can also be searched directly::

    c.unihan.get('好')

Third party API's can specify optional extra arguments, for instance,
unihan may allow searching by one field::

    c.unihan.get('好', 'kDefinition')

This allows a simple way to "drill down" cjk data across extensions.

API examples
------------

Example:

.. code-block:: python

    obj = unihan.get('好') retrieves all rows. it will create a keyed object:
    obj.kDefinition
    obj['kDefinition']
    obj.keys()
    ['kDefinition',]

    obj = unihan.get('好', 'kDefinition', ...)
    >>> obj.kDefinition
    good
    >>> obj.kStrokes
    None


Creating a cihai plugin
-----------------------

.. code-block:: python

    class Unihan(Cihai.Contrib):

        """
        Utilizing a parent class can allow raising ``NotImplementedError``
        errors. Further, this can provide access to a ``db``.

        However, ultimately, the only thing that's really required is::

            class Example(object):

                def get(self, char):
                    return {
                        'char': char
                    }

        """

        def get(self):
            pass

        def install(self):
            pass

    cihai = Cihai()
    cihai.use(Unihan)  # register the middleware with
    c = cihai.get('好')
    >>> c.keys()
    ['unihan']
    >>> c.get('好')
    <Cihai.Contrib.Unihan>
    >>> print(c.get('好'))
    >>> print(c.get('好').parent)

    # Below this point, libunihan splits into subplugins for its libraries.
    >>> print(dict(c.get('好')))


Cihai will allows extensibility to new dictionaries, vocabularies and data.

Middleware allows an arbitrary plugin to make data available.

By default, ``Cihai()`` creates an instance of Cihai with access to :meth:`Cihai.get`.

However, since no middleware are included with Cihai, no results are returned.

With ``Cihai(middleware=[Cihai.Unihan])``

or ``c = Cihai()``

``c.use(Cihai.Unihan)``

the Cihai_Unihan is available. What is Cihai_Unihan? Simply an object
with:

.. code-block:: python

    class Unihan(Cihai.Contrib):

        pass

.. _Hanzi: https://github.com/nieldlr/Hanzi
