.PHONY: act-test act-push act-pr act-list test test-cov test-cov-html

# List all workflows
act-list:
	act -l

# Run tests locally (simulating push event)
act-push:
	act push --env-file .github/workflows/.env.act

# Run tests locally (simulating pull request)
act-pr:
	act pull_request --env-file .github/workflows/.env.act

# Run specific job
act-test:
	act -j test-coverage --env-file .github/workflows/.env.act

# Run with verbose output
act-debug:
	act push --env-file .github/workflows/.env.act -v

# Run tests
test:
	uv run pytest

# Run tests with coverage report
test-cov:
	uv run pytest --cov=src --cov-report=term-missing --cov-report=xml

# Run tests with HTML coverage report
test-cov-html:
	uv run pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"