.phony: install
install:
	@pipenv install --dev

.PHONY: check
check: pyright format-check test docs

.PHONY: pyright
pyright:
	@pipenv run basedpyright --warnings

.PHONY: format
format:
	@pipenv run isort --profile black .
	@pipenv run black .

.PHONY: ci
ci: format pyright

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
