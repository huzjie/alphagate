.PHONY: install dev test lint doctor serve build-docker

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check alphagate tests

doctor:
	alphagate doctor

serve:
	alphagate serve --port 8000

build-docker:
	docker build -t alphagate:latest .
