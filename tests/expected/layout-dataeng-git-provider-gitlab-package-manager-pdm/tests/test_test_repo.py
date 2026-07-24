"""Test the `test_repo` module."""

from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from test_repo.pipeline import create_pipeline

EXPECTED_TOTAL = 3


def test_pipeline_runs_locally():
    """The pipeline runs end to end against an in-memory catalog, with nothing provisioned."""
    catalog = DataCatalog({'raw_rows': MemoryDataset([{'value': 1}, {'value': None}, {'value': 2}])})
    SequentialRunner().run(create_pipeline(), catalog)
    assert catalog.load('total') == EXPECTED_TOTAL
