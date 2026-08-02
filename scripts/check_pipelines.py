"""Structurally validate the generated fixtures under `tests/expected` by parsing them."""

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    sys.exit('PyYAML is required. Install it with `make install`, or `pip install pyyaml`.')

REPO = Path(__file__).resolve().parent.parent
EXPECTED = REPO / 'tests' / 'expected'
SWALLOWED_KEY = re.compile(r'^\s*(name|displayName|uses|with|env|run|script|steps|jobs):', re.MULTILINE)
UNRENDERED = re.compile(r'(?<!\$)\{\{|\{%|\{#')
SKIP_SUFFIXES = {'.png', '.jpg', '.gif', '.ico', '.pyc'}


def find_swallowed_keys(path: Path, node: Any, trail: str = '') -> list[str]:
    """Walk a parsed document looking for keys swallowed into string values.

    Args:
        path: The file being checked, for reporting.
        node: The current node of the parsed document.
        trail: Human readable path to the current node.

    Returns:
        A list of failure messages.
    """
    failures = []
    if isinstance(node, dict):
        for key, value in node.items():
            failures += find_swallowed_keys(path, value, f'{trail}.{key}')
    elif isinstance(node, list):
        for index, value in enumerate(node):
            failures += find_swallowed_keys(path, value, f'{trail}[{index}]')
    elif isinstance(node, str) and (found := SWALLOWED_KEY.search(node)):
        failures.append(
            f'{path.relative_to(REPO)}: at {trail or "<root>"} the value contains a line '
            f'starting `{found.group(1)}:`, so a YAML key was absorbed into the string '
            f'instead of sitting beside it',
        )
    return failures


def check_azure_steps(path: Path, document: Any) -> list[str]:
    """Assert every Azure script step carries its own `displayName` key.

    Args:
        path: The file being checked, for reporting.
        document: The parsed pipeline.

    Returns:
        A list of failure messages.
    """
    failures = []
    for stage in (document or {}).get('stages', []):
        for job in stage.get('jobs', []):
            for step in job.get('steps', []):
                if 'script' in step and not step.get('displayName'):
                    failures.append(
                        f'{path.relative_to(REPO)}: a script step in stage '
                        f'{stage.get("stage")!r} has no displayName of its own',
                    )
    return failures


def check_release_topology(fixture: Path) -> list[str]:
    """Assert a fixture publishes if and only if its layout is publishable, and only when green.

    Args:
        fixture: The fixture directory.

    Returns:
        A list of failure messages.
    """
    release = fixture / '.github' / 'workflows' / 'release.yml'
    if not release.is_file():
        return []
    document = yaml.safe_load(release.read_text(encoding='utf-8')) or {}
    jobs = document.get('jobs', {})
    publishes = 'pypi-release' in jobs
    deployed = any(f'layout-{kind}-' in f'{fixture.name}-' for kind in ('ml', 'dataeng', 'service'))
    expected = not deployed and 'publish-pypi-disabled' not in fixture.name

    failures = []
    if publishes != expected:
        state = 'has' if publishes else 'lacks'
        want = 'should' if expected else 'should not'
        failures.append(f'{fixture.name}: {state} a pypi-release job but {want} publish')
    if publishes and 'ci' not in jobs.get('pypi-release', {}).get('needs', ['build']):
        build_needs = jobs.get('build', {}).get('needs')
        if build_needs != 'ci' and 'ci' not in (build_needs or []):
            failures.append(
                f'{fixture.name}: publishing does not depend on the CI job, so a red test '
                f'suite would not stop a release',
            )
    return failures


def scan_file(path: Path) -> tuple[list[str], int] | None:
    """Scan one fixture file for unrendered constructs and structural problems.

    Args:
        path: The file to scan.

    Returns:
        The failures found and 1 if the file parsed as a YAML document, or None if the file could not be
        read as text and was skipped.
    """
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return None

    failures = []
    if found := UNRENDERED.search(text):
        failures.append(f'{path.relative_to(REPO)}: contains an unrendered template construct {found.group(0)!r}')

    if path.suffix not in {'.yml', '.yaml'}:
        return failures, 0
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as error:
        failures.append(f'{path.relative_to(REPO)}: does not parse as YAML: {error}')
        return failures, 0
    if document is None:
        failures.append(f'{path.relative_to(REPO)}: parses as an empty document')
        return failures, 1

    failures += find_swallowed_keys(path, document)
    if path.name == 'azure-pipelines.yml':
        failures += check_azure_steps(path, document)
    return failures, 1


def main() -> None:
    """Validate every generated fixture."""
    if not EXPECTED.is_dir():
        sys.exit(f'No fixtures found at {EXPECTED}')

    failures: list[str] = []
    parsed = 0
    scanned = 0

    for fixture in sorted(p for p in EXPECTED.iterdir() if p.is_dir()):
        failures += check_release_topology(fixture)

    for path in sorted(EXPECTED.rglob('*')):
        if not path.is_file() or path.suffix in SKIP_SUFFIXES:
            continue
        result = scan_file(path)
        if result is None:
            continue
        file_failures, was_parsed = result
        failures += file_failures
        scanned += 1
        parsed += was_parsed

    if failures:
        print(f'{len(failures)} structural problem(s) in the generated fixtures:\n')
        for failure in failures:
            print(f'  - {failure}')
        sys.exit(1)
    print(f'pipelines OK: {parsed} YAML documents parsed, {scanned} files scanned')


if __name__ == '__main__':
    main()
