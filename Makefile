.PHONY: help install install-dev test lint format clean run demo

help:  ## Show this help message
	@echo "TweetDuel Development Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

test:  ## Run tests
	python -m pytest tests/ -v

test-cov:  ## Run tests with coverage
	python -m pytest tests/ -v --cov=utils --cov-report=html

lint:  ## Run linting
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:  ## Format code with black and isort
	black .
	isort .

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage

run:  ## Run TweetDuel
	python tweetduel.py

demo:  ## Run TweetDuel with demo URL
	python tweetduel.py --url "https://x.com/elonmusk/status/1234567890" --mode instant --persona socrates

build:  ## Build package
	python setup.py sdist bdist_wheel

install-local:  ## Install package locally
	pip install -e .

check-setup:  ## Check setup.py
	python setup.py check

docs:  ## Build documentation
	cd docs && make html

setup-dirs:  ## Create necessary directories
	mkdir -p duels armory cache

check-ollama:  ## Check if Ollama is running
	@echo "Checking Ollama status..."
	@if curl -s http://localhost:11434/api/tags > /dev/null; then \
		echo "✅ Ollama is running"; \
	else \
		echo "❌ Ollama is not running"; \
		echo "Please start Ollama: ollama serve"; \
	fi

all: clean install-dev lint test  ## Run all checks
