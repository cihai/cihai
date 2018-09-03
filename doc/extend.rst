.. _extend:

Extending cihai
===============
Use cihai's abstraction and your dataset's users can receive easy configuration,
SQL access, and be available in a growing list of CJKV information.

Creating new dataset
--------------------
Expand cihai's knowledge!

You can also make your dataset available in open source so other cihai
users can use it! If you do, bring it up on the `issue tracker`_!

*examples/dataset.py*:

.. literalinclude:: ../examples/dataset.py
   :language: python

In addition, view our reference implementation of UNIHAN, which is
incorporated as a dataset. See :class:`cihai.unihan.Unihan`

.. _issue tracker: https://github.com/cihai/cihai/issues

Plugins: Adding features to a dataset
-------------------------------------
TODO - Dataset Extensions

See our reference implementation of :class:`cihai.unihan.UnihanVariants`

Datasets can be augmented with computed methods.

These utilize a dataset to pull information out, but are frequently used /
generic enough to write a 

An example of this would be the `suggestion to add variant lookups
for UNIHAN <https://github.com/cihai/cihai/pull/131>`_.

Combining datasets
------------------
Combining general datasets in general is usually considered general library 
usage. But if you're usage is common, saves from repetition, it's worth
considering making into a reuseable extension and open sourcing it.

Using the library to mix and match data from various sources is what cihai
is meant to do! If you have a way you're using cihai that you think would
be helpful, definitely create an issue, a gist, github repo, etc! License
it permissively please (MIT, BSD, ISC, etc!)
