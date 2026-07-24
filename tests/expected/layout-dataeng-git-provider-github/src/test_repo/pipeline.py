"""The data pipeline for `test_repo`.

Built from Kedro nodes, which are plain functions wired into a directed graph. The pipeline
runs locally against an in-memory catalog with no warehouse, scheduler or other service to
provision; swap the catalog entries in `conf/base/catalog.yml` for real datasets when there
are real datasets to read.
"""

from kedro.pipeline import Pipeline, node


def clean(rows: list[dict[str, int]]) -> list[dict[str, int]]:
    """Drop rows with no value.

    Arguments:
        rows: The raw rows.

    Returns:
        The rows that carry a value.
    """
    return [row for row in rows if row.get('value') is not None]


def summarise(rows: list[dict[str, int]]) -> int:
    """Total the values.

    Arguments:
        rows: The cleaned rows.

    Returns:
        The sum of the values.
    """
    return sum(row['value'] for row in rows)


def create_pipeline() -> Pipeline:
    """Build the pipeline.

    Returns:
        The pipeline wiring the nodes together.
    """
    return Pipeline(
        [
            node(clean, inputs='raw_rows', outputs='clean_rows', name='clean'),
            node(summarise, inputs='clean_rows', outputs='total', name='summarise'),
        ],
    )
