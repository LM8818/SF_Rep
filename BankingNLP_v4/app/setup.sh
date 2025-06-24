#!/bin/bash

echo "Настройка окружения BankingNLP_v2..."

# Проверяем наличие Python 3.12
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 не найден. Устанавливаем через Homebrew..."
    brew install python@3.12
fi

# Создаем виртуальную среду
echo "Создание виртуальной среды..."
python3.12 -m venv .venv

# Активируем виртуальную среду
echo "Активация виртуальной среды..."
source .venv/bin/activate

# Обновляем pip
echo "Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "Установка зависимостей..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install pandas numpy scikit-learn pyyaml spacy
fi

# Создаем необходимые директории
echo "Создание директорий..."
mkdir -p logs
mkdir -p data/processed
mkdir -p data/raw
mkdir -p models

echo "Настройка завершена! Для запуска используйте:"
echo "source .venv/bin/activate"
echo "python run.py"
