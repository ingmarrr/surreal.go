
build:
	@go build -o bin/app

run: build
	@bin/app

tag: increment_version
	@python3.10 scripts/version.py tag

increment_version:
	@python3.10 scripts/version.py incr

update:
	@git add -A
	@python3.10 scripts/version.py get && git commit -m $VERSION