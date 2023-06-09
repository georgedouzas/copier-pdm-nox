install:
	@pip install -r requirements.txt

changelog:
	@git-changelog -Tbo CHANGELOG.md -c angular -t keepachangelog -s feat,fix,docs,style,refactor,tests,chore

release:
	@git add CHANGELOG.md
	@git commit -m "docs: Update changelog for version $(version)"
	@git tag -d $(version) || true
	@git tag $(version) || true
	@git push --force
	@git push --force --tags
