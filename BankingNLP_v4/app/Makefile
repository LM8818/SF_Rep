# Makefile для BankingNLP v2

.PHONY: install test lint format clean train predict

# Установка зависимостей
install:
	pip install -r requirements.txt
	python -m spacy download ru_core_news_sm

# Установка для разработки
install-dev: install
	pip install -r requirements-dev.txt

# Форматирование кода
format:
	black src/ tests/
	isort src/ tests/

# Проверка стиля кода
lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

# Запуск тестов
test:
	pytest tests/ -v

# Тесты с покрытием
test-coverage:
	pytest --cov=src tests/ --cov-report=html

# Обучение модели
train:
	python run.py train --config src/config/config.yaml

# Предсказание (пример)
predict:
	python run.py predict --config src/config/config.yaml --text "Хочу узнать баланс"

# Очистка временных файлов
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Создание дистрибутива
build:
	python setup.py sdist bdist_wheel

# Полная проверка перед коммитом
check: format lint test

# Помощь
help:
	@echo "Доступные команды:"
	@echo "  install      - Установка зависимостей"
	@echo "  install-dev  - Установка для разработки"
	@echo "  format       - Форматирование кода"
	@echo "  lint         - Проверка стиля кода"
	@echo "  test         - Запуск тестов"
	@echo "  train        - Обучение модели"
	@echo "  predict      - Пример предсказания"
	@echo "  clean        - Очистка временных файлов"
	@echo "  check        - Полная проверка"
