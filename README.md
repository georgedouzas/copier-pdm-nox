# Copier Modern Python

[Copier](https://github.com/copier-org/copier) template for modern Python projects.

This template provides a comprehensive, production-ready Python project structure with modern tooling and best practices. It
supports both [PDM](https://github.com/pdm-project/pdm) and [uv](https://github.com/astral-sh/uv) package managers, includes
automated testing and quality checks, comprehensive documentation setup, and CI/CD workflows for multiple Git providers.

The template is designed to help you quickly bootstrap Python projects with industry-standard tools and configurations, allowing
you to focus on writing code rather than setting up infrastructure.

## Features

During the Copier generation process, you'll be prompted to select your preferences for package management, Git provider,
licensing, and other options. The template then generates a customized project structure with only the tools and configurations
you need.

### Package Management

Choose between two modern Python package managers. **PDM** offers cutting-edge dependency management with PEP 582 support,
allowing you to avoid virtual environments entirely. **uv** provides blazing-fast package installation and resolution,
significantly reducing setup times. Both managers handle dependency locking, virtual environment management, and script execution
seamlessly.

### Task Runner

**Nox** replaces traditional Makefiles with Python-based automation. The template includes pre-configured sessions for testing
across multiple Python versions, code formatting, quality checks, and documentation building. This ensures consistent development
workflows across different environments and team members.

### Documentation

Automatic documentation generation using **MkDocs** with the beautiful **Material theme**. The **mkdocstrings** plugin extracts
API documentation directly from your docstrings, keeping documentation in sync with code. Includes example pages, custom CSS, and
responsive design out of the box.

### Code Quality & Formatting

Enforce consistent code style with **black** for uncompromising formatting and **docformatter** for PEP 257 compliant docstrings.
**Ruff** provides extremely fast linting with hundreds of rules, replacing multiple tools like flake8, isort, and pyupgrade in a
single, performant package. **interrogate** ensures your code is properly documented by checking docstring coverage.

### Security & Safety

Proactive security scanning with **safety** to detect known vulnerabilities in dependencies and **bandit** to identify common
security issues in your code. These tools integrate into CI/CD pipelines to catch security problems before deployment.

### Type Checking

**mypy** provides static type analysis to catch type-related bugs before runtime. The template includes sensible defaults and
excludes common directories like tests and generated documentation.

### Testing

Comprehensive testing setup with **pytest** and essential plugins. **coverage** tracks code coverage with HTML reports.
Tests run in parallel for faster feedback during development.

### Development Workflow

**pre-commit** hooks automatically run quality checks before each commit, preventing broken code from entering the repository.
**git-changelog** generates beautiful changelogs from conventional commit messages, automating release documentation.

### Platform Support

Supports all major Git providers with pre-configured CI/CD workflows. Choose from GitHub Actions, GitLab CI, Azure Pipelines, or
Bitbucket Pipelines. Includes automated testing, quality checks, documentation deployment, and PyPI publishing. License selection
covers all popular open-source licenses with proper SPDX identifiers.

## Prerequisites

Before using this template, ensure you have the following tools installed:

### Required Tools

- **[Python](https://www.python.org/)** (>= 3.11)
- **[Git](https://git-scm.com/)** (>= 2.30.0)
- **[Copier](https://github.com/copier-org/copier)**

### Package Manager

Choose one of the following:

- **[PDM](https://github.com/pdm-project/pdm)** (>= 2.9.0)
- **[uv](https://github.com/astral-sh/uv)** (>= 0.1.0)

### Git Provider CLI Tools

Depending on your chosen Git provider, install the corresponding CLI tool for automated releases:

- **[GitHub CLI](https://cli.github.com/)**
- **[GitLab CLI](https://gitlab.com/gitlab-org/cli)**
- **[Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)**
- **[Atlassian CLI](https://developer.atlassian.com/cloud/acli)**

## Usage

### Creating a New Project

To create a new Python project using this template:

```bash
copier copy "gh:georgedouzas/copier-modern-python.git" /path/to/your/new/project
```

The template will prompt you for various configuration options including:

- Project name and description
- Author information
- Package manager preference (PDM or uv)
- Git provider (GitHub, GitLab, Azure DevOps, Bitbucket, or None)
- License selection
- Python version requirements
- Publishing preferences

### Updating an Existing Project

To update your project with the latest template version:

```bash
cd /path/to/your/project
copier update
```

This will apply any template updates while preserving your project-specific configurations.
