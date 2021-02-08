export PYTHONPATH = $(shell pwd)

test:
	pipenv run pytest tests

mypy:
	pipenv run mypy crawler

pylint:
	pipenv run pylint crawler

codestyle:
	pipenv run pycodestyle crawler

lint: codestyle pylint mypy
