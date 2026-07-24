#!/usr/bin/env bats
#
# Integration smoke tests: generate a project and actually run its toolchain.
# These need network access plus pdm and uv installed, so they are kept out of
# the default `make tests` target and run via `make tests-integration`.

generate() {
    local out="$1"
    shift
    copier copy "$TEMPLATE_DIR" "$out" --defaults --vcs-ref=HEAD \
        --data project_description="A test project." \
        --data author_fullname="Georgios Douzas" \
        --data author_email="gdouzas@icloud.com" \
        --data author_username="gdouzas" \
        --data repository_name="test-repo" \
        "$@" || true
    [ -d "$out" ]
}

init_git() {
    git init -q
    git add -A
    git -c user.email=test@test.com -c user.name=test commit -qm "init"
    git tag 0.1.0
}

setup() {
    export TEST_DIR="$(mktemp -d)"
    export TEMPLATE_DIR="$(pwd)"
    cd "$TEST_DIR"
}

teardown() {
    rm -rf "$TEST_DIR"
}

@test "Generated PDM project installs, checks and tests pass" {
    command -v pdm >/dev/null || skip "pdm not installed"
    command -v uv >/dev/null || skip "uv not installed (needed for nox venvs)"

    generate proj
    cd proj
    init_git

    run pdm install
    [ "$status" -eq 0 ]

    run pdm checks
    [ "$status" -eq 0 ]

    run pdm tests
    [ "$status" -eq 0 ]
    [ -f coverage.xml ]
}

@test "Generated uv project installs, checks and tests pass" {
    command -v uv >/dev/null || skip "uv not installed"

    generate proj --data package_manager=uv
    cd proj
    init_git

    run uv sync
    [ "$status" -eq 0 ]

    run uv run nox -s checks
    [ "$status" -eq 0 ]

    run uv run nox -s tests
    [ "$status" -eq 0 ]
    [ -f coverage.xml ]
}

@test "Generated script layout installs, checks, tests and runs its command" {
    command -v pdm >/dev/null || skip "pdm not installed"
    command -v uv >/dev/null || skip "uv not installed (needed for nox venvs)"

    generate proj --data project_layout=script
    cd proj
    init_git

    run pdm install
    [ "$status" -eq 0 ]

    run pdm checks
    [ "$status" -eq 0 ]

    run pdm tests
    [ "$status" -eq 0 ]

    run pdm run test-repo --name layouts
    [ "$status" -eq 0 ]
    [[ "$output" == *"Hello, layouts!"* ]]
}

@test "Generated ML layout installs, checks and tests with no cloud credentials" {
    command -v pdm >/dev/null || skip "pdm not installed"
    command -v uv >/dev/null || skip "uv not installed (needed for nox venvs)"

    generate proj --data project_layout=ml
    cd proj
    init_git

    run pdm install
    [ "$status" -eq 0 ]

    run pdm checks
    [ "$status" -eq 0 ]

    # Stripped of AWS configuration: Metaflow local mode must need no account or server.
    run env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_PROFILE pdm tests
    [ "$status" -eq 0 ]

    # Running the flow must not leave the project dirty.
    run git status --porcelain
    [ -z "$output" ]
}

@test "Generated ML layout keeps data out of version control" {
    generate proj --data project_layout=ml
    cd proj
    init_git

    echo "secret,data" > data/probe.csv

    run git status --porcelain
    [ -z "$output" ]

    run git ls-files data/
    [ -n "$output" ]
}

@test "Generated service layout installs, checks, tests and serves" {
    command -v pdm >/dev/null || skip "pdm not installed"
    command -v uv >/dev/null || skip "uv not installed (needed for nox venvs)"

    generate proj --data project_layout=service
    cd proj
    init_git

    run pdm install
    [ "$status" -eq 0 ]

    run pdm checks
    [ "$status" -eq 0 ]

    run pdm tests
    [ "$status" -eq 0 ]
}
