# Core

{class}`cihai.core.Cihai` is the application object that owns configuration, database access, and
datasets. Most code creates one instance, runs {meth}`cihai.core.Cihai.bootstrap` when needed, then
queries the attached datasets.

```{eval-rst}
.. automodule:: cihai.core
   :members:
   :undoc-members:
   :show-inheritance:
```
