.. _troubleshooting:

===============
Troubleshooting
===============

Python 2.7 and UCS
------------------

Note, to get this working on python 2.7, you must have python built with
*UCS4* via ``--enable-unicode=ucs4``. You can test for UCS4 with:

.. code-block:: python

   >>> import sys
   >>> sys.maxunicode > 0xffff
   True

Most packaged and included python distributions will already be build with
UCS4 (such as Ubuntu's system python). On python 3.3 and greater, this
distinction no longer exists, no action is needed.
