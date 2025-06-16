# Banking NLP Toolkit - Development Makefile

.PHONY: help install install-dev test lint format clean build docs

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package for production
	pip install -e .

install-dev:  ## Install package for development
	pip install -e ".[dev]"
	pre-commit install
	python -m spacy download ru_core_news_md

test:  ## Run tests
	pytest tests/ -v --cov=banking_nlp --cov-report=html --cov-report=term

test-unit:  ## Run unit tests only
	pytest tests/unit/ -v

test-integration:  ## Run integration tests only
	pytest tests/integration/ -v

lint:  ## Run linting checks
	flake8 banking_nlp/ tests/
	mypy banking_nlp/ --ignore-missing-imports
	bandit -r banking_nlp/

format:  ## Format code
	black banking_nlp/ tests/
	isort banking_nlp/ tests/

format-check:  ## Check code formatting
	black --check banking_nlp/ tests/
	isort --check-only banking_nlp/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

docs:  ## Build documentation
	cd docs && make html

docs-serve:  ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

run-example:  ## Run example usage
	banking-nlp process --input examples/sample.txt --config configs/default.yaml

train-example:  ## Train example model
	banking-nlp train --config configs/training.yaml --data examples/training_data.json

setup-project:  ## Initial project setup
	make install-dev
	make format
	make test
	@echo "Project setup complete!"
