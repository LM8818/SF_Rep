# Banking NLP System - Makefile
.PHONY: help install test clean run docker-build docker-run format lint

# Цвета для вывода
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# По умолчанию показываем help
help:
	@echo "$(GREEN)Banking NLP System - Доступные команды:$(RESET)"
	@echo "  $(YELLOW)install$(RESET)      - Установка зависимостей"
	@echo "  $(YELLOW)run$(RESET)          - Запуск приложения"
	@echo "  $(YELLOW)test$(RESET)         - Запуск тестов"
	@echo "  $(YELLOW)format$(RESET)       - Форматирование кода"
	@echo "  $(YELLOW)lint$(RESET)         - Проверка качества кода"
	@echo "  $(YELLOW)docker-build$(RESET) - Сборка Docker образа"
	@echo "  $(YELLOW)docker-run$(RESET)   - Запуск в Docker"
	@echo "  $(YELLOW)clean$(RESET)        - Очистка временных файлов"

# Установка зависимостей
install:
	@echo "$(GREEN)Установка зависимостей...$(RESET)"
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

# Запуск приложения
run:
	@echo "$(GREEN)Запуск Banking NLP System...$(RESET)"
	python -m src.banking_nlp.main

# Запуск тестов
test:
	@echo "$(GREEN)Запуск тестов...$(RESET)"
	pytest tests/ -v

# Запуск тестов с покрытием
test-coverage:
	@echo "$(GREEN)Запуск тестов с покрытием...$(RESET)"
	pytest --cov=src/banking_nlp --cov-report=html tests/

# Форматирование кода
format:
	@echo "$(GREEN)Форматирование кода...$(RESET)"
	black src/ tests/
	isort src/ tests/

# Проверка качества кода
lint:
	@echo "$(GREEN)Проверка качества кода...$(RESET)"
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/

# Сборка Docker образа
docker-build:
	@echo "$(GREEN)Сборка Docker образа...$(RESET)"
	docker build -t banking-nlp:latest .

# Запуск в Docker
docker-run:
	@echo "$(GREEN)Запуск в Docker...$(RESET)"
	docker-compose up -d

# Остановка Docker
docker-stop:
	@echo "$(GREEN)Остановка Docker...$(RESET)"
	docker-compose down

# Очистка временных файлов
clean:
	@echo "$(GREEN)Очистка временных файлов...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Создание production сборки
build-prod:
	@echo "$(GREEN)Создание production сборки...$(RESET)"
	python -m build

# Проверка безопасности
security-check:
	@echo "$(GREEN)Проверка безопасности...$(RESET)"
	safety check
	bandit -r src/
