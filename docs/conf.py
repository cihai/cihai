"""Sphinx configuration for cihai."""

from __future__ import annotations

import pathlib
import sys

from gp_sphinx.config import make_linkcode_resolve, merge_sphinx_config

import cihai

# Get the project root dir, which is the parent dir of this
cwd = pathlib.Path(__file__).parent
project_root = cwd.parent
src_root = project_root / "src"

sys.path.insert(0, str(src_root))

# package data
about: dict[str, str] = {}
with (src_root / "cihai" / "__about__.py").open() as fp:
    exec(fp.read(), about)

conf = merge_sphinx_config(
    project=about["__title__"],
    version=about["__version__"],
    copyright=about["__copyright__"],
    source_repository=f"{about['__github__']}/",
    docs_url=about["__docs__"],
    source_branch="master",
    light_logo="img/cihai.svg",
    dark_logo="img/cihai.svg",
    extra_extensions=["sphinx_autodoc_api_style"],
    intersphinx_mapping={
        "python": ("http://docs.python.org/", None),
        "sphinx": ("http://www.sphinx-doc.org/en/stable/", None),
        "sqlalchemy": ("http://docs.sqlalchemy.org/en/20/", None),
        "pandas": ("http://pandas.pydata.org/pandas-docs/stable", None),
        "unihan-etl": ("https://unihan-etl.git-pull.com/", None),
    },
    linkcode_resolve=make_linkcode_resolve(cihai, about["__github__"]),
    html_favicon="_static/favicon.ico",
    html_extra_path=["manifest.json"],
    rediraffe_redirects="redirects.txt",
)
globals().update(conf)
