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
