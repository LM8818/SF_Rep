FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY core/ ./core/
COPY utils/ ./utils/
COPY configs/ ./configs/
COPY pipelines/ ./pipelines/

# Создание директорий для данных и логов
RUN mkdir -p data/raw data/processed data/synthetic logs

# Переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Проверка работоспособности
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import core.data_processing.preprocessors; print('OK')" || exit 1

# Запуск приложения
CMD ["python", "-m", "pipelines.inference"]
