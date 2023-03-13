# Copier PDM and Nox

[Copier](https://github.com/copier-org/copier) template for Python projects managed by [PDM](https://github.com/pdm-project/pdm)
with the help of [Nox](https://github.com/wntrblm/nox).

## Features

- [PDM](https://github.com/pdm-project/pdm) is used as a dependency manager, with pre-defined `pyproject.toml`.
- [Nox](https://github.com/wntrblm/nox) for running development tasks in multiple Python environments, with a pre-defined
  `noxfile.py`.
- Documentation built with [MkDocs](https://github.com/mkdocs/mkdocs) using [Material
  theme](https://github.com/squidfunk/mkdocs-material).
- Tools for code formatting:
    - [black](https://github.com/psf/black)
    - [docformatter](https://github.com/PyCQA/docformatter)
- Tools for checking code quality:
    - [ruff](https://github.com/charliermarsh/ruff)
- Tools for checking safety vulnerabilities:
    - [safety](https://github.com/pyupio/safety)
- Tools for checking type annotations:
    - [mypy](https://github.com/pyupio/safety)
- Tests run with [pytest](https://github.com/pytest-dev/pytest) and plugins, with [coverage](https://github.com/nedbat/coveragepy)
  support.
- `CHANGELOG.md` managed by [towncrier](https://github.com/twisted/towncrier).
- Support for [GitHub Actions](https://github.com/features/actions).
- All licenses from [choosealicense.com](https://choosealicense.com/appendix/)
- Python 3.8 or above.

## Installation

```bash
copier "gh:georgedouzas/copier-pdm-nox.git" /path/to/your/new/project
```

See the [documentation](https://georgedouzas.github.io/copier-pdm-nox) for more details.
