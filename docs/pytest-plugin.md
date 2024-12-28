(pytest_plugin)=

# `pytest` plugin

Download and reuse UNIHAN.zip on the fly in [pytest].

```{module} cihai.pytest_plugin

```

[pytest]: https://docs.pytest.org/

## Usage

Install `unihan-etl` via the python package manager of your choosing, e.g.

```console
$ pip install unihan-etl
```

The pytest plugin will automatically be detected via pytest, and the fixtures will be added.

## Fixtures

`pytest-unihan` works through providing {ref}`pytest fixtures <pytest:fixtures-api>` - so read up on
those!

The plugin's fixtures guarantee downloading, and then reusing UNIHAN.zip every
test without needing to redownload.

(recommended-fixtures)=

## Recommended fixtures

These are fixtures are automatically used when the plugin is enabled and `pytest` is ran.

- Creating temporary, test directories for:
  - `/home/` ({func}`home_path`)
  - `/home/${user}` ({func}`user_path`)
- Setting your home directory
  - Patch `$HOME` to point to {func}`user_path` ({func}`set_home`)
## Bootstrapping pytest in your `conftest.py`

The most common scenario is you will want to configure the above fixtures with `autouse`.

_Why doesn't the plugin automatically add them?_ It's part of being a decent pytest plugin and
python package: explicitness.

(set_home)=

### Setting a temporary home directory

```python
import pytest

@pytest.fixture(autouse=True)
def setup(
    set_home: None,
):
    pass
```

## See examples

View unihan-etl's own [tests/](https://github.com/cihai/unihan-etl/tree/master/tests)

## API reference

```{eval-rst}
.. automodule:: cihai.pytest_plugin
    :members:
    :inherited-members:
    :private-members:
    :show-inheritance:
    :member-order: bysource
```
