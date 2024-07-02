install:
	@pip install -r requirements.txt

changelog:
	@git-changelog -T --bump=auto -o CHANGELOG.md -c angular -t keepachangelog -s feat,fix,docs,style,refactor,tests,chore

release:
	@git add CHANGELOG.md
	@git commit -m "docs: Update changelog for version $(version)"
	@git tag $(version)
	@git push --force
	@git push --force --tags
