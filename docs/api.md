(api)=

# API

```{eval-rst}
.. automodule:: cihai.core
    :members:
```

## Configuration

```{eval-rst}
.. automodule:: cihai.config
    :members:
```

## Database

```{eval-rst}
.. automodule:: cihai.db
    :members:
```

## Extending

```{eval-rst}
.. automodule:: cihai.extend
    :members:
```

## Constants

```{eval-rst}
.. automodule:: cihai.constants
    :members:
```

## UNIHAN Dataset

### Bootstrapping

```{eval-rst}
.. automodule:: cihai.data.unihan.bootstrap
    :members:
```

```{eval-rst}
.. autoclass:: cihai.data.unihan.dataset.Unihan
   :members:
   :inherited-members:
   :show-inheritance:
```

```{eval-rst}
.. automodule:: cihai.data.unihan.constants
   :members:
   :inherited-members:
   :show-inheritance:
```

### Variants plugin

```{eval-rst}
.. autoclass:: cihai.data.unihan.dataset.UnihanVariants
   :members:
   :inherited-members:
   :show-inheritance:
```

(cihai-conversion)=

## Conversion

```{eval-rst}
.. autofunction:: cihai.conversion.euc_to_unicode
```

```{eval-rst}
.. autofunction:: cihai.conversion.euc_to_utf8
```

```{eval-rst}
.. autofunction:: cihai.conversion.gb2312_to_euc
```

```{eval-rst}
.. autofunction:: cihai.conversion.kuten_to_gb2312
```

```{eval-rst}
.. autofunction:: cihai.conversion.python_to_euc
```

```{eval-rst}
.. autofunction:: cihai.conversion.python_to_ucn
```

```{eval-rst}
.. autofunction:: cihai.conversion.ucn_to_unicode
```

```{eval-rst}
.. autofunction:: cihai.conversion.ucnstring_to_python
```

```{eval-rst}
.. autofunction:: cihai.conversion.ucnstring_to_unicode
```

## Exceptions

When using cihai via Python, you can catch Cihai-specific exceptions via
these. All Cihai-specific exceptions are catchable via
{exc}`~cihai.exc.CihaiException` since its the base exception.

```{eval-rst}
.. automodule:: cihai.exc
    :members:
    :inherited-members:
    :show-inheritance:
```

## Utilities

```{eval-rst}
.. automodule:: cihai.utils
    :members:
    :inherited-members:
    :show-inheritance:
```
