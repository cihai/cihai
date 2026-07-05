# Extending

Extension classes let advanced users add datasets or dataset-specific behavior to
{class}`cihai.core.Cihai`. Start with {class}`cihai.extend.Dataset`; use
{class}`cihai.extend.DatasetPlugin` when the behavior belongs under an existing dataset.
{class}`cihai.extend.ConfigMixin` and {class}`cihai.extend.SQLAlchemyMixin` are available when an
extension needs shared configuration or the application database handle.

```{eval-rst}
.. automodule:: cihai.extend
   :members:
   :undoc-members:
   :show-inheritance:
```
