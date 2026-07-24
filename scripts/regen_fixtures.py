"""Regenerate the golden fixtures under `tests/expected` by rendering the template.

Fixtures are the specification: they are always produced by rendering, never edited by hand
to match an expectation. This script is the only supported way to update them.

The answers file of each fixture is preserved, because `tests/test_copier.bats` excludes it
from comparison and rewriting it on every run would churn the diff for no reason.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPECTED = REPO / 'tests' / 'expected'
ANSWERS = '.copier-answers.yml'

COMMON = {
    'project_description': 'A test project.',
    'author_fullname': 'Georgios Douzas',
    'author_email': 'gdouzas@icloud.com',
    'author_username': 'gdouzas',
    'repository_name': 'test-repo',
}

# Fixture name -> the answers that differ from the defaults. Keep in step with the cases in
# `tests/test_copier.bats`; a fixture with no case, or a case with no fixture, is a gap.
FIXTURES: dict[str, dict[str, str]] = {
    'default': {},
    'no-git-provider': {'git_provider': 'None'},
    'uv-package-manager': {'package_manager': 'uv'},
    'no-publish-pypi': {'publish_pypi': 'False'},
    'no-license': {'copyright_license': 'None'},
    'azure-devops': {'git_provider': 'Azure DevOps'},
    'gitlab': {'git_provider': 'GitLab'},
    'bitbucket': {'git_provider': 'Bitbucket'},
    'script-layout': {'project_layout': 'script'},
    'ml-layout': {'project_layout': 'ml'},
}


def render(name: str, answers: dict[str, str], destination: Path) -> None:
    """Render one fixture into `destination`.

    Arguments:
        name: The fixture name.
        answers: Answers that differ from the defaults.
        destination: Directory to render into.
    """
    command = ['copier', 'copy', str(REPO), str(destination), '--defaults', '--vcs-ref=HEAD']
    for key, value in {**COMMON, **answers}.items():
        command += ['--data', f'{key}={value}']
    result = subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603
    if result.returncode != 0 or not destination.is_dir():
        sys.exit(f'Rendering fixture {name!r} failed:\n{result.stdout}\n{result.stderr}')


def install(name: str, rendered: Path) -> None:
    """Replace the fixture directory with freshly rendered output.

    Arguments:
        name: The fixture name.
        rendered: The freshly rendered tree.
    """
    target = EXPECTED / name
    previous_answers = target / ANSWERS
    saved = previous_answers.read_bytes() if previous_answers.is_file() else None
    (rendered / ANSWERS).unlink(missing_ok=True)
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(rendered, target)
    if saved is not None:
        (target / ANSWERS).write_bytes(saved)


def main() -> None:
    """Regenerate every fixture."""
    for name, answers in FIXTURES.items():
        with tempfile.TemporaryDirectory() as tmp:
            rendered = Path(tmp) / name
            render(name, answers, rendered)
            install(name, rendered)
        print(f'regenerated {name}')
    print(f'{len(FIXTURES)} fixtures regenerated')


if __name__ == '__main__':
    main()
