_cihai-cli_ - Command line interface to the
[cihai](https://cihai.git-pull.com)
[CJK](https://cihai.git-pull.com/glossary.html#term-cjk)-language
library

[![Python Package](https://img.shields.io/pypi/v/cihai_cli.svg)](http://badge.fury.io/py/cihai_cli)
[![Docs](https://github.com/cihai/cihai-cli/workflows/Publish%20Docs/badge.svg)](https://github.com/cihai/cihai-cli/actions?query=workflow%3A%22Publish+Docs%22)
[![Build Status](https://github.com/cihai/cihai-cli/workflows/tests/badge.svg)](https://github.com/cihai/cihai-cli/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/cihai/cihai-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/cihai-cli)
![License](https://img.shields.io/github/license/cihai/cihai-cli.svg)

This project is under active development. Follow our progress and check
back for updates!

# Installation

```sh
$ pip install --user cihai[cli]
```

# Character lookup

See [CLI](https://cihai-cli.git-pull.com/cli.html) in the documentation
for full usage information.

```sh
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
ucn: U+597D

# retrieve all character information (including book indices)
$ cihai info 好 -a
char: 好
kCangjie: VND
kCantonese: hou2 hou3
kCihaiT: '378.103'
kDefinition: good, excellent, fine; well
kFenn: 552A
kFourCornerCode: '4744.7'
kFrequency: '1'
kGradeLevel: '1'
kHKGlyph: 0871
kHangul: 호
kHanyuPinlu: hǎo(6060) hāo(142) hào(115)
kHanyuPinyin: 21028.010:hǎo,hào
kJapaneseKun: KONOMU SUKU YOI
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kPhonetic: '481'
kRSAdobe_Japan1_6: C+1975+38.3.3 C+1975+39.3.3
kRSKangXi: '38.3'
kTang: '*xɑ̀u *xɑ̌u'
kTotalStrokes: '6'
kVietnamese: háo
kXHC1983: 0445.030:hǎo 0448.030:hào
ucn: U+597D
```

# Reverse lookup

```sh
$ cihai reverse library
char: 圕
kCantonese: syu1
kDefinition: library
kJapaneseOn: TOSHOKAN SHO
kMandarin: tú
kTotalStrokes: '13'
ucn: U+5715
--------
char: 嫏
kCantonese: long4
kDefinition: the place where the supreme stores his books; library
kJapaneseOn: ROU
kMandarin: láng
kTotalStrokes: '11'
ucn: U+5ACF
--------
```

# Developing

[poetry](https://python-poetry.org/) is a required package to develop.

`git clone https://github.com/cihai/cihai-cli.git`

`cd cihai-cli`

`poetry install -E "docs test coverage lint format"`

Makefile commands prefixed with `watch_` will watch files and rerun.

## Tests

`poetry run py.test`

Helpers: `make test` Rerun tests on file change: `make watch_test`
(requires [entr(1)](http://eradman.com/entrproject/))

## Documentation

Default preview server: <http://localhost:8037>

`cd docs/` and `make html` to build. `make serve` to start http server.

Helpers: `make build_docs`, `make serve_docs`

Rebuild docs on file change: `make watch_docs` (requires
[entr(1)](http://eradman.com/entrproject/))

Rebuild docs and run server via one terminal: `make dev_docs` (requires
above, and a `make(1)` with `-J` support, e.g. GNU Make)

## Formatting / Linting

The project uses [black](https://github.com/psf/black) and
[isort](https://pypi.org/project/isort/) (one after the other) and runs
[flake8](https://flake8.pycqa.org/) via CI. See the configuration in
<span class="title-ref">pyproject.toml</span> and \`setup.cfg\`:

`make black isort`: Run `black` first, then `isort` to handle import
nuances `make flake8`, to watch (requires `entr(1)`):
`make watch_flake8`

## Releasing

As of 0.6, [poetry](https://python-poetry.org/) handles virtualenv
creation, package requirements, versioning, building, and publishing.
Therefore there is no setup.py or requirements files.

Update <span class="title-ref">\_\_version\_\_</span> in <span
class="title-ref">\_\_about\_\_.py</span> and \`pyproject.toml\`:

    git commit -m 'build(cihai-cli): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags
    poetry build
    poetry deploy

# Quick links

- [Usage](https://cihai-cli.git-pull.com/usage.html)
- Python [API](https://cihai-cli.git-pull.com/api.html)
- [2017
  roadmap](https://cihai.git-pull.com/design-and-planning/2017/spec.html)
- Python support: >= 3.6, pypy
- Source: <https://github.com/cihai/cihai-cli>
- Docs: <https://cihai-cli.git-pull.com>
- Changelog: <https://cihai-cli.git-pull.com/history.html>
- API: <https://cihai-cli.git-pull.com/api.html>
- Issues: <https://github.com/cihai/cihai-cli/issues>
- Test coverage <https://codecov.io/gh/cihai/cihai-cli>
- pypi: <https://pypi.python.org/pypi/cihai-cli>
- OpenHub: <https://www.openhub.net/p/cihai-cli>
- License: MIT
