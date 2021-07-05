import logging
import sys

import click
import yaml

import cihai
from cihai._compat import PY2
from cihai.core import Cihai
from unihan_etl.__about__ import __version__ as __unihan_etl_version__

from .__about__ import __title__, __version__

#: fields which are human friendly
HUMAN_UNIHAN_FIELDS = [
    'char',
    'ucn',
    'kDefinition',
    'kCantonese',
    'kHangul',
    'kJapaneseOn',
    'kKorean',
    'kMandarin',
    'kVietnamese',
    'kTang',
    'kTotalStrokes',
]


@click.group(context_settings={'obj': {}})
@click.version_option(
    __version__,
    '-V',
    '--version',
    message='''
{prog} %(version)s, cihai {cihai_version}, unihan-etl {unihan_etl_version}
'''.format(
        prog=__title__,
        cihai_version=cihai.__version__,
        unihan_etl_version=__unihan_etl_version__,
    ).strip(),
)
@click.option(
    '-c',
    '--config',
    type=click.Path(exists=True),
    metavar='<config-file>',
    help="path to custom config file",
)
@click.option(
    '--log_level',
    default='INFO',
    metavar='<log-level>',
    help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)',
)
@click.pass_context
def cli(ctx, config, log_level):
    """Retrieve CJK information via CLI.

    For help and example usage, see documentation:

    https://cihai-cli.git-pull.com and https://cihai.git-pull.com"""
    setup_logger(level=log_level.upper())
    if config:
        c = Cihai.from_file(config)
    else:
        c = Cihai()

    if not c.unihan.is_bootstrapped:
        click.echo("Bootstrapping Unihan database")
        c.unihan.bootstrap(options=c.config.get('unihan_options', {}))

    ctx.obj['c'] = c  # pass Cihai object down to other commands


INFO_SHORT_HELP = (
    u'Get details on a CJK character'
    if PY2
    else u'Get details on a CJK character, e.g. "好"'
)


@cli.command(name='info', short_help=INFO_SHORT_HELP)
@click.argument('char', metavar='<character>')
@click.option(
    '-a', '--all', 'show_all', is_flag=True, help="Show all character details"
)
@click.pass_context
def command_info(ctx, char, show_all):
    c = ctx.obj['c']
    query = c.unihan.lookup_char(char).first()
    attrs = {}
    if not query:
        click.echo("No records found for %s" % char, err=True)
        sys.exit()
    for c in query.__table__.columns._data.keys():
        value = getattr(query, c)
        if value:
            if PY2:
                value = value.encode('utf-8')
            if not show_all and str(c) not in HUMAN_UNIHAN_FIELDS:
                continue
            attrs[str(c)] = value
    click.echo(
        yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip('\n')
    )


@cli.command(
    name='reverse', short_help='Search all info for character matches, e.g. "good"'
)
@click.argument('char', metavar='<character>')
@click.option(
    '-a', '--all', 'show_all', is_flag=True, help="Show all character details"
)
@click.pass_context
def command_reverse(ctx, char, show_all):
    c = ctx.obj['c']
    query = c.unihan.reverse_char([char])
    if not query.count():
        click.echo("No records found for %s" % char, err=True)
        sys.exit()
    for k in query:
        attrs = {}
        for c in k.__table__.columns._data.keys():
            value = getattr(k, c)
            if value:
                if PY2:
                    value = value.encode('utf-8')
                if not show_all and str(c) not in HUMAN_UNIHAN_FIELDS:
                    continue
                attrs[str(c)] = value
        click.echo(
            yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip(
                '\n'
            )
        )
        click.echo('--------')


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
