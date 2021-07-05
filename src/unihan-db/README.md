_unihan-db_ - database [SQLAlchemy](https://www.sqlalchemy.org/) models
for [UNIHAN](http://www.unicode.org/charts/unihan.html). Part of the
[cihai](https://cihai.git-pull.com) project. Powered by
[unihan-etl](https://unihan-etl.git-pull.com). See also:
[libUnihan](http://libunihan.sourceforge.net/).

[![Python Package](https://img.shields.io/pypi/v/unihan-db.svg)](http://badge.fury.io/py/unihan-db)
[![Docs](https://github.com/cihai/unihan-db/workflows/Publish%20Docs/badge.svg)](https://github.com/cihai/unihan-db/actions?query=workflow%3A%22Publish+Docs%22)
[![Build Status](https://github.com/cihai/unihan-db/workflows/test/badge.svg)](https://github.com/cihai/unihan-db/actions?query=workflow%3A%22test%22)
[![Code Coverage](https://codecov.io/gh/cihai/unihan-db/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/unihan-db)
![License](https://img.shields.io/github/license/cihai/unihan-db.svg)

By default, unihan-db creates a SQLite database in an [XDG data
directory](https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html).
You can specify a custom database destination by passing a database url
into
[get_session](http://unihan-db.git-pull.com/en/latest/api.html#unihan_db.bootstrap.get_session).

# Example usage

```python
#!/usr/bin/env python
import pprint

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row = session.query(Unhn).order_by(
    func.random()
).limit(1).first()

pp = pprint.PrettyPrinter(indent=0)

pp.pprint(random_row.to_dict())
```

Run:

    $ ./examples/01_bootstrap.py

Output:

```python
{'char': '鎷',
'kCantonese': [{'char_id': '鎷', 'definition': 'maa5', 'id': 24035}],
'kDefinition': [],
'kHanYu': [{'char_id': '鎷',
          'id': 24014,
          'locations': [{'character': 5,
                       'generic_indice_id': 24014,
                       'generic_reading_id': None,
                       'id': 42170,
                       'page': 4237,
                       'virtual': 0,
                       'volume': 6}],
          'type': 'kHanYu'}],
'kHanyuPinyin': [{'char_id': '鎷',
                'id': 18090,
                'locations': [{'character': 5,
                             'generic_indice_id': None,
                             'generic_reading_id': 18090,
                             'id': 42169,
                             'page': 4237,
                             'virtual': 0,
                             'volume': 6}],
                'readings': [{'generic_reading_id': 18090,
                            'id': 26695,
                            'reading': 'mǎ'}],
                'type': 'kHanyuPinyin'}],
'kMandarin': [{'char_id': '鎷', 'hans': 'mǎ', 'hant': 'mǎ', 'id': 23486}],
'ucn': 'U+93B7'}
```

# Developing

[poetry](https://python-poetry.org/) is a required package to develop.

`git clone https://github.com/cihai/unihan-etl.git`

`cd unihan-etl`

`poetry install -E "docs test coverage lint format"`

Makefile commands prefixed with `watch_` will watch files and rerun.

## Tests

`poetry run py.test`

Helpers: `make test` Rerun tests on file change: `make watch_test`
(requires [entr(1)](http://eradman.com/entrproject/))

## Documentation

Default preview server: <http://localhost:8041>

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

As of 0.1, [poetry](https://python-poetry.org/) handles virtualenv
creation, package requirements, versioning, building, and publishing.
Therefore there is no setup.py or requirements files.

Update <span class="title-ref">\_\_version\_\_</span> in <span
class="title-ref">\_\_about\_\_.py</span> and \`pyproject.toml\`:

    git commit -m 'build(unihan-db): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags
    poetry build
    poetry deploy
