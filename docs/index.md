(index)=

# cihai

Python library for {term}`CJK` (Chinese, Japanese, Korean)
character data. Look up readings, definitions, and variants from the
[UNIHAN](datasets/unihan.md) database and beyond.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and make your first lookup in 5 minutes.
:::

:::{grid-item-card} Topics
:link: topics/index
:link-type: doc
Features, examples, extending, troubleshooting.
:::

:::{grid-item-card} API Reference
:link: api/index
:link-type: doc
Every public class, function, and exception.
:::

::::

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Datasets
:link: datasets/index
:link-type: doc
UNIHAN and planned data sources.
:::

:::{grid-item-card} Internals
:link: internals/index
:link-type: doc
Private APIs -- no stability guarantee.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, release process.
:::

::::

## Install

```console
$ pip install cihai
```

```console
$ uv add cihai
```

## At a glance

```python
from cihai.core import Cihai

c = Cihai()

if not c.unihan.is_bootstrapped:  # download and install UNIHAN to db
    c.unihan.bootstrap()

query = c.unihan.lookup_char('好')
glyph = query.first()
print("lookup for 好: %s" % glyph.kDefinition)
# lookup for 好: good, excellent, fine; well

query = c.unihan.reverse_char('good')
print('matches for "good": %s ' % ', '.join([glph.char for glph in query]))
# matches for "good": 㑘, 㑤, 㓛, 㘬, 㙉, 㚃, ...
```

See [Quickstart](quickstart.md) for detailed installation and first steps.

```{toctree}
:hidden:

quickstart
topics/index
api/index
datasets/index
internals/index
project/index
design-and-planning/index
history
glossary
GitHub <https://github.com/cihai/cihai>
```
