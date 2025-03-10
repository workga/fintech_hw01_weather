.DEFAULT_GOAL := help
PYTHONPATH = PYTHONPATH=./
TEST = $(PYTHONPATH) pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg) -k "$(k)"
CODE = weather tests

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) --cov

.PHONY: test-fast
test-fast: ## Runs pytest with exitfirst
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed: ## Runs pytest from last-failed
	$(TEST) --last-failed

.PHONY: test-cov
test-cov: ## Runs pytest with coverage report
	$(TEST) --cov --cov-report html

.PHONY: lint
lint: ## Lint code
	flake8 --jobs 4 --statistics --show-source $(CODE)
	pylint --rcfile=setup.cfg $(CODE)
# mypy $(CODE) ругается на неуказанные типы в объявлениях функций, пока не решил это
	black --line-length 80 --target-version py39 --skip-string-normalization --check $(CODE)
	pytest --dead-fixtures --dup-fixtures
	safety check --full-report

.PHONY: format
format: ## Formats all files
	autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	isort $(CODE)
	black --line-length 80 --target-version py39 --skip-string-normalization $(CODE)
	unify --in-place --recursive $(CODE)

.PHONY: check
check: format lint test ## Format and lint code then run tests
