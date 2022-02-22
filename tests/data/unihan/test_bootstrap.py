# -*- coding: utf8 - *-
from cihai.core import Cihai
from cihai.data.unihan import bootstrap


def test_reflect_db(tmpdb_file, unihan_options):
    c = Cihai(
        {"database": {"url": "sqlite:///{tmpdb_file}".format(tmpdb_file=tmpdb_file)}}
    )
    assert not c.unihan.is_bootstrapped
    bootstrap.bootstrap_unihan(c.sql.metadata, unihan_options)
    assert not hasattr(c.sql.base.classes, "Unihan")
    c.unihan.sql.reflect_db()
    assert hasattr(c.sql.base.classes, "Unihan")
