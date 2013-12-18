.. _extending:

=========
Extending
=========

``cihai/testsuite/test_middleware/simple/__init__.py``:

.. literalinclude:: ../cihai/testsuite/test_middleware/simple/__init__.py
    :language: python
    :lines: 12-

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
