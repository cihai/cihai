#!/usr/bin/env python
# -*- coding: utf8 - *-
"""libunihan lives at <https://github.com/tony/libunihan>.

libunihan
---------

Mass update git, hg and svn repos simultaneously from YAML / JSON file.

"""
import os
import sys
import glob
from setuptools import setup
try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve

with open('requirements.pip') as f:
    install_reqs = [line for line in f.read().split('\n') if line]
    tests_reqs = []

if sys.version_info < (2, 7):
    install_reqs += ['argparse']
    tests_reqs += ['unittest2']

import re
VERSIONFILE = "libunihan/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

UNIHAN_ZIP = 'http://www.unicode.org/Public/UNIDATA/Unihan.zip'
PACKAGE_DATA = []

if not os.path.exists('libunihan/data'):
    os.makedirs('./libunihan/data')

if not glob.glob('./libunihan/data/Unihan*.txt'):
    urlretrieve(UNIHAN_ZIP, os.path.join('./libunihan/data', 'Unihan.zip'))

setup(
    name='libunihan',
    version=__version__,
    url='http://github.com/tony/libunihan/',
    download_url='https://pypi.python.org/pypi/libunihan',
    license='BSD',
    author='Tony Narlock',
    author_email='tony@git-pull.com',
    description='Unihan abstraction layer.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=install_reqs,
    tests_require=tests_reqs,
    test_suite='libunihan.testsuite',
    zip_safe=False,
    packages=['libunihan', 'libunihan.testsuite'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: BSD License",
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
)
