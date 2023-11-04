.PHONY: check
check: mypy format-check

.PHONY: mypy
mypy:
	@mypy automation_entities

.PHONY: format
format:
	@git ls-files | grep "\.py$ " | xargs black

.PHONY: format-check
format-check:
	@git ls-files | grep "\.py$ " | xargs black --check

.PHONY: test
test:
	@py.test --cov=automation_entities --cov-report=term-missing .

docs/_static:
	mkdir -p docs/_static

.PHONY: docs
docs: docs/_static
	@sphinx-build . docs/build -c docs/

.PHONY: clean-docs
clean-docs:
	rm -rf docs/build
