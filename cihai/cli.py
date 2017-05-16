# -*- coding: utf8 - *-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import os
import sys
import click


from .__about__ import __version__
from ._compat import string_types

def get_cwd():
    return os.getcwd()


@click.group(context_settings={'obj': {}})
@click.version_option(
    __version__, '-V', '--version', message='%(prog)s %(version)s'
)
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('--log_level', default='INFO',
              help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
def cli(config, log_level):
    """cihai

    Pass the "--help" argument to any command to see detailed help.
    See detailed documentation and examples at:
    http://cihai.git-pull.com"""
    print('hi')
    setup_logger(
        level=log_level.upper()
    )
    pass



@cli.command(name='info', short_help='Get details on a CJK character')
@click.pass_context
def command_info(ctx):
    """Hi"""
    print('load')



def setup_logger(logger=None, level='INFO'):
    """Setup logging for CLI use.

    :param logger: instance of logger
    :type logger: :py:class:`Logger`

    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)

