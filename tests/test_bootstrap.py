# -*- coding: utf8 - *-

from cihai import bootstrap
from cihai.core import Cihai


def test_reflect_db(tmpdb_file, unihan_options):
    c = Cihai(
        {'database': {'url': 'sqlite:///{tmpdb_file}'.format(tmpdb_file=tmpdb_file)}}
    )
    assert not c.sql.is_bootstrapped
    bootstrap.bootstrap_unihan(c.sql.metadata, unihan_options)
    assert not hasattr(c.sql.base.classes, 'Unihan')
    c.sql.reflect_db()
    assert hasattr(c.sql.base.classes, 'Unihan')
