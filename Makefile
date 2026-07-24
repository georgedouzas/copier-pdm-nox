.PHONY: install docs tests tests-integration changelog release

install:
	@pip install -r requirements.txt

docs:
	@properdocs serve

tests:
	@bats tests/test_copier.bats

tests-integration:
	@bats tests/test_integration.bats

changelog:
	@git-changelog -T --bump=auto -o CHANGELOG.md -c angular -t keepachangelog -s feat,fix,docs,style,refactor,tests,chore

release: changelog
	$(eval version := $(shell grep -m1 -oE '^## \[[^]]+\]' CHANGELOG.md | sed 's/^## \[//;s/\]$$//'))
	@git add CHANGELOG.md
	-@pre-commit run --files CHANGELOG.md
	@git add CHANGELOG.md
	@git commit -m "docs: Update changelog for version $(version)"
	@git tag $(version)
	@git push
	@git push --tags
