"""Regenerate the golden fixtures under `tests/expected` by rendering the template.

Fixtures are the specification: they are always produced by rendering, never edited by hand
to match an expectation. This script is the only supported way to update them, and it is the
single source of truth for which combinations exist -- `tests/test_copier.bats` reads the same
set back by iterating the directories this writes.

Coverage is the full cross product of the three structural dimensions -- project layout, git
provider and package manager -- because the pipeline and packaging templates branch on all
three and their interactions are where rendering bugs hide (a package manager renders different
CI commands for each provider, and each layout declares different dependency groups). Two extra
fixtures cover the orthogonal publish and license paths.

The rendered `.copier-answers.yml` is not kept: it records a `_commit` that changes on every
tag, so storing it would churn the fixtures for no reason. The answers each fixture was built
from are recoverable from its directory name, which is what the bats suite does.
"""

import itertools
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

# Each dimension maps a name segment to the answer it stands for. The segment is what appears in
# the fixture directory name; the value is what is passed to copier.
LAYOUTS = {
    'library': 'library',
    'script': 'script',
    'ml': 'ml',
    'dataeng': 'dataeng',
    'service': 'service',
}
GIT_PROVIDERS = {
    'github': 'GitHub',
    'gitlab': 'GitLab',
    'azure-devops': 'Azure DevOps',
    'bitbucket': 'Bitbucket',
    'none': 'None',
}
PACKAGE_MANAGERS = {
    'pdm': 'PDM',
    'uv': 'uv',
}


def build_fixtures() -> dict[str, dict[str, str]]:
    """Build the fixture name to answers mapping.

    Returns:
        The full cross product of the structural dimensions, plus the publish and license edges.
    """
    fixtures: dict[str, dict[str, str]] = {}
    for (lseg, lval), (pseg, pval), (mseg, mval) in itertools.product(
        LAYOUTS.items(),
        GIT_PROVIDERS.items(),
        PACKAGE_MANAGERS.items(),
    ):
        name = f'layout-{lseg}-git-provider-{pseg}-package-manager-{mseg}'
        fixtures[name] = {
            'project_layout': lval,
            'git_provider': pval,
            'package_manager': mval,
        }

    base = 'layout-library-git-provider-github-package-manager-pdm'
    defaults = {'project_layout': 'library', 'git_provider': 'GitHub', 'package_manager': 'PDM'}
    fixtures[f'{base}-publish-pypi-disabled'] = {**defaults, 'publish_pypi': 'False'}
    fixtures[f'{base}-license-none'] = {**defaults, 'copyright_license': 'None'}
    return fixtures


FIXTURES = build_fixtures()


def render(name: str, answers: dict[str, str], destination: Path) -> None:
    """Render one fixture into `destination`.

    Arguments:
        name: The fixture name.
        answers: The answers that define this fixture.
        destination: Directory to render into.
    """
    command = ['copier', 'copy', str(REPO), str(destination), '--defaults', '--vcs-ref=HEAD']
    for key, value in {**COMMON, **answers}.items():
        command += ['--data', f'{key}={value}']
    result = subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603
    if result.returncode != 0 or not destination.is_dir():
        sys.exit(f'Rendering fixture {name!r} failed:\n{result.stdout}\n{result.stderr}')


def install(rendered: Path, target: Path) -> None:
    """Replace the fixture directory with freshly rendered output, minus the answers file.

    Arguments:
        rendered: The freshly rendered tree.
        target: The fixture directory to replace.
    """
    (rendered / ANSWERS).unlink(missing_ok=True)
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(rendered, target)


def main() -> None:
    """Regenerate every fixture, removing any that are no longer defined."""
    EXPECTED.mkdir(parents=True, exist_ok=True)
    stale = {p.name for p in EXPECTED.iterdir() if p.is_dir()} - set(FIXTURES)
    for name in sorted(stale):
        shutil.rmtree(EXPECTED / name)
        print(f'removed stale {name}')

    for name, answers in FIXTURES.items():
        with tempfile.TemporaryDirectory() as tmp:
            rendered = Path(tmp) / name
            render(name, answers, rendered)
            install(rendered, EXPECTED / name)
    print(f'{len(FIXTURES)} fixtures regenerated')


if __name__ == '__main__':
    main()
