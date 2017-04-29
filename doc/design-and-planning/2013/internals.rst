:orphan:

.. _design-and-planning/2013/internals:

=========================
Internal Design decisions
=========================

Convenient relational, cohesive output of datasets
--------------------------------------------------

Whether you are Cihai, python, creating a CJK tool in another programming
language, or simple looking to use a dataset, cihai will provide tools
to turn raw datasets into a familiar table / relational friendly format.

Certain datasets may also offer to download the latest datasets from a
server as well.

Cihai is a tool to convert CJK datasets to a common, relational format
and provide a convient Python API for studying deeply.

Bootstrapping
-------------

Cihai's core functionality relies on a ``ForeignKeyRestraint`` against
an entry on a master table of chinese characters / string which are
assigned an integer ID for use as a ``ForeignKey``. This way, datasets
added to Cihai can achieve fast lookups and JOIN's via integers instead of
unicode characters.

If the word has multiple characters, Cihai will create the character ID
for you and cite it for you and all future entries added to your dataset
will reference it.

This makes installing datasets in Cihai expensive (requiring a lookup of a
unicode string in a central table) before inserting into database, with
the benefit of potentially returning a huge cross-section of available CJK
data in one swift stroke.

