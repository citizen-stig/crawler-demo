export PYTHONPATH = $(shell pwd)

test:
	pipenv run pytest tests

mypy:
	pipenv run mypy
