#!/usr/bin/env bats

setup() {
    export TEST_DIR="$(mktemp -d)"
    export TEMPLATE_DIR="$(pwd)"
    cd "$TEST_DIR"
}

teardown() {
    rm -rf "$TEST_DIR"
}

@test "Test default copier" {
    run copier copy "$TEMPLATE_DIR" test-repo --defaults --vcs-ref=HEAD \
    --data project_description="A test project." \
    --data author_fullname="Georgios Douzas" \
    --data author_email="gdouzas@icloud.com" \
    --data author_username="gdouzas" \
    --data repository_name="test-repo"

    [ "$status" -eq 0 ]
    [ -d "test-repo" ]
    for expected_file in "$(dirname "$BATS_TEST_FILENAME")/repos/default"/*; do
        if [ -f "$expected_file" ]; then
            filename=$(basename "$expected_file")
            [ -f "test-repo/$filename" ]
            diff "$expected_file" "test-repo/$filename"
        fi
    done
}

@test "Test default interactive copier" {
    run timeout 20 expect -c '
        spawn copier copy "$::env(TEMPLATE_DIR)" test-repo --vcs-ref=HEAD
        expect "Your project description" { send "A test project.\r" }
        expect "Your full name" { send "Georgios Douzas\r" }
        expect "Your email" { send "gdouzas@icloud.com\r" }
        expect "Your GitHub username" { send "gdouzas\r" }
        expect "Your repository namespace" { send "\r" }
        expect "Your repository name" { send "test-repo\r" }
        expect "The name of the person" { send "\r" }
        expect "The email of the person" { send "\r" }
        expect "The copyright date" { send "\r" }
        expect "Your project* license" { send "\r" }
        expect "Your Python package distribution name" { send "\r" }
        expect "Your Python package import name" { send "\r" }
        expect "The range of Python versions" { send "\r" }
        expect "Your Git provider" { send "\r" }
        expect "Your Python package manager" { send "\r" }
        expect "Publish your project to PyPI" { send "\r" }
        expect eof
    '
    [ "$status" -eq 0 ]
    [ -d "test-repo" ]
    [ -f "test-repo/README.md" ]
    for expected_file in "$(dirname "$BATS_TEST_FILENAME")/repos/default"/*; do
        if [ -f "$expected_file" ]; then
            filename=$(basename "$expected_file")
            [ -f "test-repo/$filename" ]
            diff "$expected_file" "test-repo/$filename"
        fi
    done
}
