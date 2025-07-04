# 🏦 Banking NLP System

Система автоматического анализа банковских разговоров на базе FastAPI с современным веб-интерфейсом.

## 📋 Описание проекта

**Banking NLP System** — это полнофункциональная система для анализа текстов банковских разговоров, построенная на современных технологиях Python. Система обеспечивает автоматическую классификацию тематик, распознавание банковских продуктов и эмоциональный анализ клиентских обращений.

### 🎯 Основные возможности

- **Анализ тематик разговоров** — автоматическая классификация по 10 основным категориям
- **Распознавание банковских продуктов** — выявление упоминаний кредитов, депозитов, карт и других услуг
- **Эмоциональный анализ** — определение позитивной, негативной или нейтральной окраски текста
- **Современный веб-интерфейс** — удобная русскоязычная форма для анализа
- **REST API** — полнофункциональный API для интеграции с другими системами

## 🚀 Быстрый старт

### Автоматическая установка (рекомендуется)

```bash
# Скачайте файл run.py и выполните команду:
python run.py
```

Скрипт автоматически:
- Проверит версию Python
- Создаст виртуальное окружение
- Установит все необходимые зависимости
- Запустит приложение

### Ручная установка

```bash
# 1. Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Запуск приложения
python3 -m src.banking_nlp.main
```

## 🏗️ Структура проекта

```
Дерево каталогов для: BankingNLP
├── Dockerfile
├── Makefile
├── README.md                                 # Документация проекта
├── api
│   └── routers.py                             # API маршруты
├── data
│   ├── processed
│   │   ├── conversation_analytics.csv
│   │   ├── conversations_processed.csv
│   │   ├── data_metadata.json
│   │   └── themes_summary.csv
│   └── raw
│   │   └── conversations_raw_20250611_131947.csv
├── directory_tree.txt
├── docker-compose.yml
├── img
│   ├── API_test_ans.jpg
│   └── API_test_req.jpg
├── info.md
├── logs
│   └── app.log
├── project_structure.txt
├── pyproject.toml
├── requirements.txt                          # Зависимости Python
├── run.py                                    # Скрипт автоматического запуска
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   └── __init__.cpython-312.pyc
│   └── banking_nlp
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │       ├── __init__.cpython-312.pyc
│   │       └── main.cpython-312.pyc
│   │   ├── api
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   └── routes.cpython-312.pyc
│   │       └── routes.py
│   │   ├── core                              
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   ├── config.cpython-312.pyc
│   │       │   └── logging_config.cpython-312.pyc
│   │       ├── config.py                             # Конфигурация системы
│   │       └── logging_config.py
│   │   ├── data
│   │       └── __init__.py
│   │   ├── main.py
│   │   ├── services
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   ├── analysis.cpython-312.pyc
│   │       │   └── health.cpython-312.pyc
│   │       ├── analysis.py
│   │       └── health.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │           ├── __init__.cpython-312.pyc
│   │           ├── data_generator.cpython-312.pyc
│   │           └── data_initializer.cpython-312.pyc
│   │       ├── data_generator.py
│   │       ├── data_initializer.py
│   │       └── preprocessing.py
├── static                   # Статические файлы (CSS, JS)
│   ├── app.js
│   ├── bank_icon.svg
│   └── style.css
├── templates                 # HTML шаблоны
│   └── index.html
├── test.ipynb
└── tests
│   ├── __init__.py
│   ├── e2e
│       └── __init__.py
│   ├── integration
│       ├── __init__.py
│       └── test_api.py
│   └── unit
│       ├── __init__.py
│       └── test_analysis.py            
```

## 🌐 Использование системы

### Веб-интерфейс

После запуска откройте браузер и перейдите на:
- **Главная страница**: http://localhost:8000/
- **API документация**: http://localhost:8000/docs
- **API тестирование: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/06fdb339ca8d45c94c4ad941dfd4131f/74ed22ec-0786-4090-8d45-d3eaed32e994/index.html

### Пример использования

1. **Введите текст разговора** в большое поле на главной странице
2. **Нажмите "Анализировать разговор"**
3. **Получите результат** с тематиками, продуктами и эмоциональной окраской

![](/img/API_test_req.jpg)
![](/img/API_test_ans.jpg)

### Примеры текстов для тестирования

```
"Хочу взять кредит на автомобиль"
"Проблемы с мобильным банком, не могу войти"
"Интересует ипотека на квартиру"
"Не работает карта, списали лишние деньги"
```

## 📊 API Endpoints

### POST /api/analyze

Анализ текста банковского разговора.

**Запрос:**
```json
{
  "text": "Хочу взять кредит на машину",
  "language": "ru"
}
```

**Ответ:**
```json
{
  "themes": ["credit"],
  "products": ["auto_loan"],
  "emotions": {
    "positive": 0.7,
    "negative": 0.1,
    "neutral": 0.2
  },
  "confidence": 0.85
}
```

### GET /api/health

Проверка работоспособности системы.

**Ответ:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-09T02:00:00Z",
  "version": "1.0.0"
}
```

## ⚙️ Конфигурация

### Банковские продукты

Редактируйте файл `config/banking_products.json` для добавления новых продуктов:

```json
{
  "products": [
    {
      "id": "credit",
      "name": "Потребительский кредит",
      "keywords": ["кредит", "займ", "ссуда"],
      "category": "lending"
    }
  ]
}
```

### Тематики разговоров

Настройте файл `config/conversation_themes.json` для новых тематик:

```json
{
  "themes": [
    {
      "id": "credit_request",
      "name": "Заявка на кредит",
      "keywords": ["хочу кредит", "нужен займ"],
      "emotion": "neutral"
    }
  ]
}
```

## 🛠️ Технологический стек

- **Python 3.11+** — основной язык программирования
- **FastAPI** — современный веб-фреймворк для API
- **Uvicorn** — ASGI сервер для production
- **Pydantic** — валидация данных и настроек
- **Jinja2** — шаблонизатор для HTML
- **Bootstrap** — CSS фреймворк для интерфейса

## 🔧 Системные требования

- **Python**: версия 3.8 или выше
- **Операционная система**: Windows, macOS, Linux
- **Память**: минимум 512 MB RAM
- **Дисковое пространство**: 100 MB свободного места

## 📝 Логирование

Система ведет подробные логи в файле `logs/app.log`:

```
INFO - Banking NLP System запущена на порту 8000
INFO - Анализ текста: "Хочу кредит" → themes: ["credit"]
ERROR - Ошибка обработки запроса: текст слишком короткий
```

## 🚨 Решение проблем

### Ошибка импорта модулей

```bash
# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения

python3 run.py
```

### Проблемы с кодировкой

```bash
# Проверьте кодировку файла
file -I README.md

# Конвертируйте в UTF-8 если необходимо
iconv -f WINDOWS-1251 -t UTF-8 input.txt > output.txt
```

### Порт уже занят

```bash
# Найдите процесс на порту 8000
lsof -i :8000

# Убейте процесс (замените PID на реальный)
kill -9 PID
```

## 🔄 Обновление системы

```bash
# Остановите приложение (Ctrl+C)
# Обновите код из репозитория
git pull origin main

# Обновите зависимости
pip install -r requirements.txt --upgrade

# Перезапустите приложение
python run.py
```

## 📈 Планы развития

- [ ] **Интеграция с ML моделями** — RuBERT для повышения точности
- [ ] **Расширенная аналитика** — dashboard с метриками и отчетами
- [ ] **Интеграция с CRM** — подключение к банковским системам
- [ ] **Мобильное приложение** — версия для планшетов и смартфонов
- [ ] **Многоязычность** — поддержка английского и других языков

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте раздел "Решение проблем" в этой документации
2. Убедитесь, что все зависимости установлены корректно
3. Проверьте логи в файле `logs/app.log`
4. Проверьте, что Python версии 3.8+ и все файлы в кодировке UTF-8

## 📄 Лицензия

MIT License - используйте свободно в коммерческих и некоммерческих проектах.

---

**Banking NLP System** — современное решение для автоматизации анализа банковских разговоров с удобным веб-интерфейсом и мощным API.