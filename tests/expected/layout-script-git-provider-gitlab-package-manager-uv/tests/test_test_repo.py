"""Test the `test_repo` module."""

from click.testing import CliRunner

from test_repo.cli import main


def test_main():
    """The command runs and greets."""
    result = CliRunner().invoke(main, ['--name', 'test'])
    assert result.exit_code == 0
    assert 'Hello, test!' in result.output
