# AGENTS.md

Guidance for AI coding agents working in this repository. Humans should read `CONTRIBUTING.md`;
the two are kept consistent.

## What this project is

A test project.

It is a library: an importable package under `src/test_repo/`, distributed to others.
## Tasks

Development tasks are [nox](https://nox.thea.codes) sessions. Run them, do not reach for the underlying tools directly:

- `pdm formatting` — format the code and docstrings.
- `pdm checks` — run every quality check (see below).
- `pdm tests` — run the test suite with coverage.
- `pdm docs` — serve the documentation locally (`pdm docs build` to build it).

## The quality floor

`checks` enforces, and you MUST NOT weaken any of them to make a change pass:

- **ruff** — linting and import order.
- **mypy** — static types.
- **bandit** — security issues (reads `pyproject.toml`).
- **pip-audit** — known vulnerabilities in dependencies.
- **deptry** — dependencies that are declared and unused, or used and undeclared.
- **pydoclint** — docstrings that match the signature.
- **interrogate** — docstring coverage.

If a check is wrong for a specific line, suppress it narrowly and say why in the same change; do not
relax the rule for the whole project. Tool configuration lives in `pyproject.toml`.

Before proposing a change as done, run `pdm checks` and `pdm tests` and make them pass.

## Dependencies

Do not add a dependency unless something in the project uses it. Runtime dependencies belong in
`[project.dependencies]`; tools belong in the appropriate development group. The lock file is committed,
so update it when you change dependencies.

## Commits

Commit messages follow the Angular convention, enforced on commit. The type MUST be one of: `feat`, `fix`,
`docs`, `style`, `refactor`, `tests`, `chore`. The subject is capitalized, has no trailing period, and the
body explains why the change is correct, not merely what changed.

## Releases

`pdm release` is the local half of a release: it writes the changelog, opens and merges the release
pull request, and pushes the tag. The pipeline is the only publisher and will not publish a tag whose checks
and tests have not passed. Do not build and upload distributions by hand.
