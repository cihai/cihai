# -*- coding: utf8 - *-

import os

from appdirs import AppDirs

#: XDG App directory locations
dirs = AppDirs("unihan_db", "cihai team")  # appname  # app author


if not os.path.exists(dirs.user_data_dir):
    os.makedirs(dirs.user_data_dir)
