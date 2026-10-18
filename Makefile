all: pyright format-check test docs

.phony: install
install:
	@uv sync --dev

.PHONY: check
check: pyright format-check test docs

.PHONY: pyright
pyright:
	@uv run basedpyright --warnings

.PHONY: format
format:
	@uv run isort --profile black .
	@uv run black .

.PHONY: ci
ci: format pyright

.PHONY: format-check
format-check:
	@uv run isort --profile black --check-only .
	@uv run black --check .

.PHONY: test
test:
	@uv run py.test --cov=automation_entities --cov-report=term-missing .

docs/_static:
	mkdir -p docs/_static

.PHONY: docs
docs: docs/_static
	@uv run sphinx-build . docs/build -c docs/

.PHONY: clean-docs
clean-docs:
	rm -rf docs/build
