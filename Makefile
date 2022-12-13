
build:
	@go build -o bin/app

run: build
	@bin/app

increment_version:
	@python3.10 scripts/version.py incr
	@git push --tags

tag: increment_version
	@python3.10 scripts/version.py tag

update: increment_version
	@git add -A
	@python3.10 scripts/version.py get && git commit -m "$VERSION"
	@python3.10 scripts/version.py tag
	@git push --tags