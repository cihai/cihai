.. _datasets:

========
Datasets
========

Current Datasets
----------------

- `cihaidata-unihan`_ - `UNIHAN`_ data package, included in cihai by
  default.

Planned datasets
----------------

For all data sets, the goal is to achieve:

- Clear and permissive a licensing for public and private use
- Compatibilty with `Data Packages`_, for data to be language
  agnostic and consistent
- Open source scripting used to process data into a common format

============== =============== ================== ===============
Set            License         Data Package       Project
============== =============== ================== ===============
Unihan         OK [Unhn-L]_    OK [Unhn-D]_       OK [Unhn-P]_
edict          OK              TODO               TODO
cedict         OK [CDCT-L]_    TODO               TODO
cedictgr       OK              TODO               TODO
handedict      OK              TODO               TODO
cfdict         OK              TODO               TODO
============== =============== ================== ===============

.. _UNIHAN: http://www.unicode.org/charts/unihan.html
.. _Data Packages: http://frictionlessdata.io/data-packages/
.. _cihaidata-unihan: https://cihaidata-unihan.git-pull.com

.. [Unhn-L] http://unicode.org/charts/unihan.html#Disclaimers
.. [Unhn-D] https://raw.githubusercontent.com/cihai/cihaidata-unihan/master/datapackage.json
.. [Unhn-P] https://cihaidata-unihan.git-pull.com/
.. [CDCT-L] https://www.mdbg.net/chinese/dictionary?page=cedict
