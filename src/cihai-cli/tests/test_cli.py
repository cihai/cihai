import pytest

import yaml
from click.testing import CliRunner

from cihai_cli import cli


def test_cli(test_config_file):
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    result = runner.invoke(cli.cli, '-c', test_config_file)
    result = runner.invoke(cli.cli, 'info')
    assert result.exit_code == 2
    # result = runner.invoke(cli, ['info', '好'])
    # assert result.exit_code == 0


def test_cli_reflects_after_bootstrap(tmpdir, tmpdb_file, unihan_options):
    config = {
        'database': {'url': 'sqlite:///{tmpdb_file}s'.format(tmpdb_file=tmpdb_file)},
        'unihan_options': unihan_options,
    }
    config_file = tmpdir.join('config.yml')
    config_file.write(yaml.dump(config, default_flow_style=False))
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['-c', str(config_file), 'info', u'㐀'])
    assert 'Bootstrapping Unihan database' in result.output
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ['-c', str(config_file)], 'info')


@pytest.mark.parametrize('flag', ['-V', '--version'])
def test_cli_version(flag):
    runner = CliRunner()
    result = runner.invoke(cli.cli, [flag])
    assert 'cihai-cli' in result.output
    assert 'cihai' in result.output
    assert 'unihan-etl' in result.output
