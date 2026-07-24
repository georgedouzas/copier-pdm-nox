"""A minimal Metaflow pipeline for `test_repo`.

Runs locally with `python -m test_repo.flow run`. No account, server or
other infrastructure is needed: Metaflow's local mode is the default, and it stores runs under
`.metaflow` in the working directory.
"""

from metaflow import FlowSpec, step


class ExampleFlow(FlowSpec):
    """A two step flow, kept trivial so it is fast to run and obvious to replace."""

    @step
    def start(self) -> None:
        """Produce the data the next step consumes."""
        self.values = [1, 2, 3]
        self.next(self.end)

    @step
    def end(self) -> None:
        """Reduce the data the previous step produced."""
        self.total = sum(self.values)


if __name__ == '__main__':
    ExampleFlow()
