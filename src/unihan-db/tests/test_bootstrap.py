# -*- coding: utf8 - *-

from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn


def test_reflect_db(tmpdb_file, unihan_options, metadata):
    assert not bootstrap.is_bootstrapped(metadata)


def test_import_object(session, engine):
    Base.metadata.create_all(engine)
    session.add(Unhn(char=u'好', ucn='U+4E09'))
    session.commit()

    assert session.query(Unhn)
    assert session.query(Unhn).count() == 1


def test_import_unihan(zip_file, session, engine, unihan_options):
    Base.metadata.bind = engine
    Base.metadata.create_all()
    # bootstrap.bootstrap_unihan(Base.metadata, unihan_options)


def test_import_unihan_raw(zip_file, session, engine, unihan_options):
    Base.metadata.bind = engine
    Base.metadata.create_all()

    bootstrap.bootstrap_unihan(session, unihan_options)

    session.commit()
