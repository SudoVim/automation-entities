.PHONY: all
all: check test docs

.PHONY: check
check: mypy format-check

.PHONY: mypy
mypy:
	@pipenv run mypy automation_entities

.PHONY: format
format:
	@pipenv run isort --profile black .
	@pipenv run black .

.PHONY: format-check
format-check:
	@pipenv run isort --profile black --check-only .
	@pipenv run black --check .

.PHONY: test
test:
	@pipenv run py.test --cov=automation_entities --cov-report=term-missing .

docs/_static:
	mkdir -p docs/_static

.PHONY: docs
docs: docs/_static
	@pipenv run sphinx-build . docs/build -c docs/

.PHONY: clean-docs
clean-docs:
	rm -rf docs/build
