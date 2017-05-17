# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


import sys
import pytest
from cihai import cli
from click.testing import CliRunner


def test_cli(test_config_file):
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    result = runner.invoke(cli.cli, '-c', test_config_file)
    result = runner.invoke(cli.cli, 'info')
    assert result.exit_code == 2
    # result = runner.invoke(cli, ['info', '好'])
    # assert result.exit_code == 0


@pytest.mark.skipif(sys.version_info <= (2, 7, 15),
                    reason="python2.7 + click unicode fails")
def test_cli_reflects_after_bootstrap(tmpdir, tmpdb_file, unihan_options):
    config = {
        'database': {
            'url': 'sqlite:///{tmpdb_file}s'.format(tmpdb_file=tmpdb_file)
        },
        'unihan_options': unihan_options
    }
    config_file = tmpdir.join('config.yml')
    import yaml
    config_file.write(yaml.dump(config, default_flow_style=False))
    runner = CliRunner()
    # result = runner.invoke(cli.cli, ['-c', str(config_file)])
    # WTF: https://github.com/pallets/click/issues/792
    result = runner.invoke(cli.cli, ['-c', str(config_file), 'info', '㐀'])
    assert 'Bootstrapping Unihan database' in result.output
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ['-c', str(config_file)], 'info')
