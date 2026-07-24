"""Test the `test_repo` module."""

from pathlib import Path

from metaflow import Runner

import test_repo.flow

FLOW_FILE = str(Path(test_repo.flow.__file__))
EXPECTED_TOTAL = 6


def test_flow_runs_locally():
    """The flow runs end to end with no account, server or other infrastructure."""
    with Runner(FLOW_FILE, show_output=False).run() as running:
        assert running.status == 'successful'
        assert running.run.data.total == EXPECTED_TOTAL
