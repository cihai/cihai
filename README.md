_cihai_ - Python library for
[CJK](https://cihai.git-pull.com/glossary.html#term-cjk) (chinese,
japanese, korean) data

[![Python Package](https://img.shields.io/pypi/v/cihai.svg)](http://badge.fury.io/py/cihai)
[![Docs](https://github.com/cihai/cihai/workflows/Publish%20Docs/badge.svg)](https://github.com/cihai/cihai/actions?query=workflow%3A%22Publish+Docs%22)
[![Build Status](https://github.com/cihai/cihai/workflows/test/badge.svg)](https://github.com/cihai/cihai/actions?query=workflow%3A%22test%22)
[![Code Coverage](https://codecov.io/gh/cihai/cihai/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/cihai)
[![License](https://img.shields.io/github/license/cihai/cihai.svg)](https://github.com/cihai/cihai/blob/master/LICENSE)

This project is under active development. Follow our progress and check
back for updates!

## Usage

### API / Library (this repository)

```sh
$ pip install --user cihai
```

```python
from cihai.core import Cihai

c = Cihai()

if not c.unihan.is_bootstrapped:  # download and install Unihan to db
    c.unihan.bootstrap(unihan_options)

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

```sh
$ pip install --user cihai[cli]
```

```sh
# character lookup
$ cihai info 好
char: 好
kCantonese: hou2 hou3
kDefinition: good, excellent, fine; well
kHangul: 호
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kTang: '*xɑ̀u *xɑ̌u'
kTotalStrokes: '6'
kVietnamese: háo
ucn: U+597D

# reverse lookup
$ cihai reverse library
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

All datasets that cihai uses have stand-alone tools to export their
data. No library required.

- [unihan-etl](https://unihan-etl.git-pull.com) -
  [UNIHAN](http://unicode.org/charts/unihan.html) data exports for
  csv, yaml and json.

## Developing

[poetry](https://python-poetry.org/) is a required package to develop.

`git clone https://github.com/cihai/cihai.git`

`cd cihai`

`poetry install -E "docs test coverage lint format"`

Makefile commands prefixed with `watch_` will watch files and rerun.

### Tests

`poetry run py.test`

Helpers: `make test` Rerun tests on file change: `make watch_test`
(requires [entr(1)](http://eradman.com/entrproject/))

### Documentation

Default preview server: <http://localhost:8035>

`cd docs/` and `make html` to build. `make serve` to start http server.

Helpers: `make build_docs`, `make serve_docs`

Rebuild docs on file change: `make watch_docs` (requires
[entr(1)](http://eradman.com/entrproject/))

Rebuild docs and run server via one terminal: `make dev_docs` (requires
above, and a `make(1)` with `-J` support, e.g. GNU Make)

### Formatting / Linting

The project uses [black](https://github.com/psf/black) and
[isort](https://pypi.org/project/isort/) (one after the other) and runs
[flake8](https://flake8.pycqa.org/) via CI. See the configuration in
<span class="title-ref">pyproject.toml</span> and \`setup.cfg\`:

`make black isort`: Run `black` first, then `isort` to handle import
nuances `make flake8`, to watch (requires `entr(1)`):
`make watch_flake8`

### Releasing

As of 0.10, [poetry](https://python-poetry.org/) handles virtualenv
creation, package requirements, versioning, building, and publishing.
Therefore there is no setup.py or requirements files.

Update <span class="title-ref">\_\_version\_\_</span> in <span
class="title-ref">\_\_about\_\_.py</span> and \`pyproject.toml\`:

    git commit -m 'build(cihai): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags
    poetry build
    poetry deploy

## Quick links

- [Usage](https://cihai.git-pull.com/usage.html)
- [Datasets](https://cihai.git-pull.com/datasets.html) a full list of
  current and future data sets
- Python [API](https://cihai.git-pull.com/api.html)
- [Roadmap](https://cihai.git-pull.com/design-and-planning/)
- Python support: >= 3.6, pypy
- Source: <https://github.com/cihai/cihai>
- Docs: <https://cihai.git-pull.com>
- Changelog: <https://cihai.git-pull.com/history.html>
- API: <https://cihai.git-pull.com/api.html>
- Issues: <https://github.com/cihai/cihai/issues>
- Test coverage: <https://codecov.io/gh/cihai/cihai>
- pypi: <https://pypi.python.org/pypi/cihai>
- OpenHub: <https://www.openhub.net/p/cihai>
- License: MIT
