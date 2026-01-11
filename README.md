# Copier PDM and Nox

[Copier](https://github.com/copier-org/copier) template for Python projects managed by [PDM](https://github.com/pdm-project/pdm) with the help of [Nox](https://github.com/wntrblm/nox).

## Features

- Package manager
  - [PDM](https://github.com/pdm-project/pdm) or [uv](https://github.com/astral-sh/uv)
- Task runner
  - [Nox](https://github.com/wntrblm/nox) with a pre-defined `noxfile.py`
- Documentation
  - [MkDocs](https://github.com/mkdocs/mkdocs) using [Material theme](https://github.com/squidfunk/mkdocs-material) and [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings) plugin
- Code formatting
  - [black](https://github.com/psf/black)
  - [docformatter](https://github.com/PyCQA/docformatter)
- Code quality
  - [ruff](https://github.com/charliermarsh/ruff)
- Safety vulnerabilities
  - [safety](https://github.com/pyupio/safety)
  - [bandit](https://github.com/PyCQA/bandit)
- Type annotations
  - [mypy](https://github.com/python/mypy)
- Tests
  - [pytest](https://github.com/pytest-dev/pytest) and plugins, with [coverage](https://github.com/nedbat/coveragepy) support
  - Documentation coverage with [interrogate](https://github.com/econchick/interrogate)
- Git hooks
  - [pre-commit](https://github.com/pre-commit/pre-commit)
- `CHANGELOG.md`
  - [git-changelog](https://github.com/pawamoy/git-changelog)
- Git providers
  - GitHub, Azure DevOps, Bitbucket or GitLab
- Licenses
  - [choosealicense.com](https://choosealicense.com/appendix/)
- Python versions
  - 3.11 or above

## Prerequisites

To use the template's development tasks, the following command-line tools are required:

- [PDM](https://github.com/pdm-project/pdm) (>= 2.9.0) or [uv](https://github.com/astral-sh/uv) (>= 0.1.0)
- [Nox](https://nox.thea.codes/en/stable/) (>=2023.4.22)
- [Git](https://git-scm.com/) (>= 2.30.0)
- Optional CLI tools based on Git provider
  - [GitHub CLI](https://cli.github.com/) for GitHub
  - [GitLab CLI](https://gitlab.com/gitlab-org/cli) for GitLab
  - [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/) for Azure DevOps
  - [Atlassian CLI](https://developer.atlassian.com/cloud/acli) for Bitbucket

## Usage

To use the template for a new project:

```bash
copier copy "gh:georgedouzas/copier-modern-python.git" /path/to/your/new/project
```

To update the project using a new version of the template:

```bash
copier update
```

## Credits

This template is based on [copier-pdm](https://github.com/pawamoy/copier-pdm) from [Timothée
Mazzucotelli](https://pawamoy.github.io/). You may also check his other amazing projects.
