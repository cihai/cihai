#!/usr/bin/env python
import pprint

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row = session.query(Unhn).order_by(func.random()).limit(1).first()

pp = pprint.PrettyPrinter(indent=0)

pp.pprint(random_row.to_dict())
