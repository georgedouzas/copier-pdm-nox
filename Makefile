.PHONY: install docs tests changelog release

install:
	@pip install -r requirements.txt

docs:
	@mkdocs serve

tests:
	@bats tests

changelog:
	@git-changelog -T --bump=auto -o CHANGELOG.md -c angular -t keepachangelog -s feat,fix,docs,style,refactor,tests,chore

release: changelog
	$(eval version := $(shell grep -m1 -oE '^## \[[^]]+\]' CHANGELOG.md | sed 's/^## \[//;s/\]$$//'))
	@git add CHANGELOG.md
	-@pre-commit run --files CHANGELOG.md
	@git add CHANGELOG.md
	@git commit -m "docs: Update changelog for version $(version)"
	@git tag $(version)
	@git push --force
	@git push --force --tags
