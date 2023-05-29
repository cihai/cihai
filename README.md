# cihai &middot; [![Python Package](https://img.shields.io/pypi/v/cihai.svg)](https://pypi.org/project/cihai/) [![License](https://img.shields.io/github/license/cihai/cihai.svg)](https://github.com/cihai/cihai/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/cihai/cihai/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/cihai)

Python library for [CJK](https://cihai.git-pull.com/glossary.html#term-cjk) (chinese, japanese,
korean) data.

This project is under active development. Follow our progress and check back for updates!

## Quickstart

### API / Library (this repository)

```console
$ pip install --user cihai
```

```python
from cihai.core import Cihai

c = Cihai()

if not c.unihan.is_bootstrapped:  # download and install Unihan to db
    c.unihan.bootstrap()

query = c.unihan.lookup_char('好')
glyph = query.first()
print("lookup for 好: %s" % glyph.kDefinition)
# lookup for 好: good, excellent, fine; well

query = c.unihan.reverse_char('good')
print('matches for "good": %s ' % ', '.join([glph.char for glph in query]))
# matches for "good": 㑘, 㑤, 㓛, 㘬, 㙉, 㚃, 㚒, 㚥, 㛦, 㜴, 㜺, 㝖, 㤛, 㦝, ...
```

See [API](https://cihai.git-pull.com/api.html) documentation and
[/examples](https://github.com/cihai/cihai/tree/master/examples).

### CLI ([cihai-cli](https://cihai-cli.git-pull.com))

```console
$ pip install --user cihai-cli
```

Character lookup:

```console
$ cihai info 好
```

```yaml
char: 好
kCantonese: hou2 hou3
kDefinition: good, excellent, fine; well
kHangul: 호
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kTang: "*xɑ̀u *xɑ̌u"
kTotalStrokes: "6"
kVietnamese: háo
ucn: U+597D
```

Reverse lookup:

```console
$ cihai reverse library
```

```yaml
char: 圕
kCangjie: WLGA
kCantonese: syu1
kCihaiT: '308.302'
kDefinition: library
kMandarin: tú
kTotalStrokes: '13'
ucn: U+5715
--------
```

### UNIHAN data

All datasets that cihai uses have stand-alone tools to export their data. No library required.

- [unihan-etl](https://unihan-etl.git-pull.com) - [UNIHAN](http://unicode.org/charts/unihan.html)
  data exports for csv, yaml and json.

## Developing

```console
$ git clone https://github.com/cihai/cihai.git`
```

```console
$ cd cihai/
```

[Bootstrap your environment and learn more about contributing](https://cihai.git-pull.com/contributing/). We use the same conventions / tools across all cihai projects: `pytest`, `sphinx`, `flake8`, `mypy`, `black`, `isort`, `tmuxp`, and file watcher helpers (e.g. `entr(1)`).

## Python versions

- 0.19.0: Last Python 3.7 release

## Quick links

- [Quickstart](https://cihai.git-pull.com/quickstart.html)
- [Datasets](https://cihai.git-pull.com/datasets.html) a full list of current and future data sets
- Python [API](https://cihai.git-pull.com/api.html)
- [Roadmap](https://cihai.git-pull.com/design-and-planning/)
- Python support: >= 3.8, pypy
- Source: <https://github.com/cihai/cihai>
- Docs: <https://cihai.git-pull.com>
- Changelog: <https://cihai.git-pull.com/history.html>
- API: <https://cihai.git-pull.com/api.html>
- Issues: <https://github.com/cihai/cihai/issues>
- Test coverage: <https://codecov.io/gh/cihai/cihai>
- pypi: <https://pypi.python.org/pypi/cihai>
- OpenHub: <https://www.openhub.net/p/cihai>
- License: MIT

[![Docs](https://github.com/cihai/cihai/workflows/docs/badge.svg)](https://cihai.git-pull.com/)
[![Build Status](https://github.com/cihai/cihai/workflows/tests/badge.svg)](https://github.com/cihai/cihai/actions?query=workflow%3A%22tests%22)
