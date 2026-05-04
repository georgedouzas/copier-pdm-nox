#!/usr/bin/env bats

compare_repos() {
    local expected_dir="$1"
    local generated_dir="$2"

    [ -d "$generated_dir" ]
    diff -r --exclude=.copier-answers.yml "$expected_dir" "$generated_dir"
}

setup() {
    export TEST_DIR="$(mktemp -d)"
    export TEMPLATE_DIR="$(pwd)"
    cd "$TEST_DIR"
}

teardown() {
    rm -rf "$TEST_DIR"
}

@test "Test default choices" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/default" "test-repo"
}

@test "Test no git provider choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data git_provider="None"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/no-git-provider" "test-repo"
}

@test "Test uv package manager choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data package_manager="uv"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/uv-package-manager" "test-repo"
}

@test "Test no publish PyPI choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data publish_pypi="False"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/no-publish-pypi" "test-repo"
}
