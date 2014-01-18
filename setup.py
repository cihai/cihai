#!/usr/bin/env python
# -*- coding: utf8 - *-
"""cihai lives at <https://github.com/tony/cihai>.

cihai
~~~~~

Unihan abstraction layer.

"""
import os
import sys
from setuptools import setup, find_packages


with open('requirements.pip') as f:
    install_reqs = [line for line in f.read().split('\n') if line]
    tests_reqs = []

if sys.version_info < (2, 7):
    install_reqs += ['argparse']
    tests_reqs += ['unittest2']

import re
VERSIONFILE = "cihai/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name='cihai',
    version=__version__,
    url='https://github.com/tony/cihai',
    download_url='https://pypi.python.org/pypi/cihai',
    license='BSD',
    author='Tony Narlock',
    author_email='tony@git-pull.com',
    description='China fit into a python package.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=install_reqs,
    tests_require=tests_reqs,
    test_suite='cihai.testsuite',
    zip_safe=False,
    # packages=[
        # 'cihai', 'cihai.testsuite', 'cihai.datasets',
        # 'cihai._vendor', 'cihai._vendor.colorama'
    # ],
    packages=find_packages(exclude=["doc"]),
    package_data={
        'cihai': ['data/*']
    },
    entry_points=dict(console_scripts=['cihai=cihai.__main__:run']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: BSD License",
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
)
