# -*- coding: utf-8 -*-

from cihai.cli import cli

from click.testing import CliRunner


def test_cli(test_config_file):
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    result = runner.invoke(cli, '-c', test_config_file)
    result = runner.invoke(cli, 'info')
    assert result.exit_code == 2
    # result = runner.invoke(cli, ['info', '好'])
    # assert result.exit_code == 0
