# Phase 0 Research: Project Layouts

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-07-24

Phase 0 resolves the unknowns the plan's Technical Context could not settle, and closes the
Principle VI gate the Constitution Check left open.

## R1: How layout varies the template

**Decision**: One shared template spine, branching on a `project_layout` answer through the
two mechanisms already used for `git_provider` and `package_manager` — in-file Jinja
conditionals, and conditional path-name directories such as
`{% if project_layout == 'ml' %}notebooks{% endif %}`.

**Rationale**: `noxfile.py.jinja` is where the quality floor lives. If it is shared, then
FR-006 and FR-007 hold by construction: there is only one definition of what `checks` means,
so a layout cannot quietly weaken it. The repository already proves this mechanism scales to
a four-value answer (`git_provider`) inside the same files.

**Alternatives considered**:

- *Per-layout template subdirectory* (`project-library/`, `project-script/`, `project-ml/`,
  selected via `_subdirectory`). Rejected: forks `noxfile.py.jinja` and
  `pyproject.toml.jinja` three ways. Principle II exists because copies drift, and this
  would guarantee three copies of the exact thing that must not drift. It also breaks FR-012,
  since a fourth layout would mean a fourth full copy.
- *Copier `_exclude` patterns driven by layout*. Rejected as the primary mechanism: it can
  remove files but cannot vary their contents, so `pyproject.toml` and `noxfile.py` would
  still need in-file conditionals. Two mechanisms where one suffices.
- *Post-generation task that deletes inapplicable files*. Rejected: the intermediate state
  exists on disk, `copier update` reasons about the pre-deletion tree, and the deletion
  logic is invisible to the fixtures.

## R2: Guaranteeing the library layout does not change

**Decision**: Add `project_layout` with `default: library`, and make every new conditional
render its current content on the `library` branch. Verify by regenerating all existing
fixtures and asserting a zero-byte diff, before any new layout is added.

**Rationale**: SC-002 demands comparison, not inspection (Principle IV). The existing eight
fixtures in `tests/expected/` already encode today's output exactly; if adding the question
leaves them untouched, FR-002 is proven rather than asserted. This makes the first
implementation task a pure no-op change whose entire success criterion is "nothing moved".

**Alternatives considered**:

- *Review the diff by eye*. Rejected outright — this is exactly the failure mode Principle IV
  was written about after the Azure `displayName` bug.

## R3: What the script/CLI layout contains

**Decision**: Keep `src/` and the packaging spine, add a `cli.py` module and a
`[project.scripts]` console-script entry point. Dependency addition: **one** CLI framework.

**Rationale**: A CLI tool is a library with an entry point; it is publishable, so the entire
release topology (FR-008) applies unchanged. This is the layout that proves the mechanism
cheaply. `click` is the conservative choice — it is already the dependency `properdocs`
itself pulls in, so the generated project's dependency tree gains nothing new at the
transitive level, and `mkdocs-click` exists should CLI documentation be wanted later.

**Principle VI check**: the framework is configured in `pyproject.toml` (`[project.scripts]`),
exercised by the generated test suite, and its command is runnable immediately after
generation. It is integrated, not merely installed.

**Alternatives considered**:

- *`typer`*. A reasonable choice, but it is `click` plus type-driven sugar, and it adds a
  dependency the tree does not already carry. Deferred rather than rejected; the decision is
  cheap to revisit before implementation.
- *`argparse`, no dependency at all*. Rejected: generates a project whose CLI is a worked
  example of boilerplate the user will replace, which fails the spirit of FR-004's "nothing
  vestigial".

## R4: What the ML layout contains, and what it must not

**Decision**: A `notebooks/` directory, a `data/` directory ignored by version control, a
`src/` package for importable code, and **no** ML framework dependency. The layout ships
the *shape*, not a stack: no pinned framework, no experiment tracker, no pipeline runner.

**Rationale**: This is the Principle VI gate. An ML layout is the natural place to bundle a
fashionable stack, and every dependency added is paid for by every ML project the template
ever generates — including the ones that wanted a different framework and must now remove
this one. The layout's value is the scaffolding that is tedious to assemble (directory
conventions, notebook handling in linting and coverage, data ignored, docs shaped for
narrative rather than API reference). The framework choice is the user's, and it is the one
decision an ML practitioner is certain to have an opinion about.

Concretely, adding a framework would violate the principle's third condition: it cannot be
"exercised by CI" in any meaningful way, because the template has no model to train.

**Principle VI check**: **passes by adding nothing.** The layout's only new machinery is
configuration — notebook-aware lint and coverage settings — which is exercised by the
generated project's own `checks` session.

**Alternatives considered**:

- *Ship scikit-learn, pandas and numpy as defaults*. Rejected per the above. Note the docs
  dependency group already carries `pandas` for the gallery, so the marginal convenience is
  smaller than it appears.
- *Ship an experiment tracker (MLflow or similar)*. Rejected: it implies infrastructure the
  template cannot provision, and an unconfigured tracker is worse than none.
- *Offer a nested "ML framework" question*. Rejected for the first release: it multiplies
  the matrix again for a choice the user can make in one line of `pyproject.toml`.

## R5: Publishing for a layout that publishes nothing

**Decision**: Make `publish_pypi` conditional — `when: "{{ project_layout != 'ml' }}"` with
a computed default of `false` for `ml`. The release *session* remains present for every
layout, because changelog and tagging are still meaningful; only the publish step is absent.

**Rationale**: FR-009 requires omission rather than a broken artifact, and FR-016 makes ML
the case that proves it. This also resolves the spec's first edge case — the contradiction
cannot arise, because the question is not asked when it does not apply. The distinction that
matters is between *releasing* (versioning, changelog, tagging — universal) and *publishing*
(uploading a distribution — layout-dependent).

**Alternatives considered**:

- *Ask `publish_pypi` anyway and ignore a `true` answer*. Rejected: silently discarding a
  user's answer is precisely the "resolve predictably and report" failure FR-013 forbids.
- *Hard-error on the contradictory combination*. Rejected as hostile for a case the question
  flow can simply avoid.

## R6: Documentation shape per layout

**Decision**: The API-reference generator (`docs/generate_api.py.jinja`, driven by
`mkdocstrings`) is library-and-script only. The ML layout gets a narrative documentation
nav instead, and `properdocs.yml.jinja`'s `watch` list follows the layout's source paths.

**Rationale**: `generate_api.py` imports the package to document it. For a layout whose
centre of gravity is notebooks, an API reference over a thin `src/` package is the
"present-but-broken" artifact the spec's fourth edge case names. This is also the
`--only-dev` bug from the uv docs session in a different costume: documentation tooling that
assumes an importable package fails loudly when the layout does not guarantee one.

**Alternatives considered**:

- *Keep the API reference for all layouts*. Rejected: generates a near-empty page, and
  couples the ML layout to having an importable package at all times.

## R7: Fixture coverage strategy

**Decision**: Add exactly two fixtures — `script-layout` and `ml-layout`, both at otherwise
default answers. Extend `tests/test_integration.bats` to generate and run all three layouts.
Do not expand the provider or package-manager fixtures per layout.

**Rationale**: The constitution's Principle III coverage rule requires every dimension value
to appear at least once, not every combination to be enumerated. Three layouts × four
providers × two package managers is 24 fixtures; that suite would stop being run before
every commit, which would cost more than it catches. Layout affects the source tree, the
dependency set and the docs shape — dimensions largely orthogonal to which CI provider is
configured — so the cross terms are low-risk.

**Residual risk, accepted and recorded**: a defect that appears only in, say, ml + Bitbucket
would not be caught. The integration suite's per-layout runs mitigate the most likely
version of this, which is a layout breaking the shared nox spine.

**Alternatives considered**:

- *Full cross product*. Rejected: 24 fixtures, unrunnable before every commit.
- *One fixture per layout per package manager* (6). Deferred: a reasonable middle ground if
  the ML layout turns out to interact with dependency-group syntax, which differs between
  PDM and uv. Revisit if implementation surfaces it.

## Open questions carried into implementation

None blocking. Two decisions are cheap to revisit and flagged in place: the CLI framework
choice (R3) and whether ML needs a per-package-manager fixture (R7).
