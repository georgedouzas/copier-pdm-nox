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

@test "Test no license choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data copyright_license="None"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/no-license" "test-repo"
}

@test "Test Azure DevOps choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data git_provider="Azure DevOps"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/azure-devops" "test-repo"
}

@test "Test GitLab choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data git_provider="GitLab"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/gitlab" "test-repo"
}

@test "Test Bitbucket choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data git_provider="Bitbucket"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/bitbucket" "test-repo"
}

@test "Test script layout choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data project_layout="script"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/script-layout" "test-repo"
}

@test "Test ML layout choice" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo" \
    --data project_layout="ml"

    [ -d test-repo ]
    compare_repos "$(dirname "$BATS_TEST_FILENAME")/expected/ml-layout" "test-repo"
}
