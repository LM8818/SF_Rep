import os
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import sqlite3

import logging.config
import yaml

def setup_logging():
    with open('logging.yaml') as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)

# Настройка логирования с ротацией и поддержкой JSON-формата
log_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
)
log_handler = RotatingFileHandler('logs/data_load.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
log_handler.setFormatter(log_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

DB_PATH = os.getenv('BANKINGNLP_DB_PATH', 'bankingnlp.db')
CSV_PATH = 'data/processed/transcripts.csv'
REQUIRED_COLUMNS = [
    'conversation_id', 'client_id', 'agent_id', 'timestamp', 'conversation_text',
    'theme', 'product', 'product_keywords', 'emotion', 'client_satisfaction',
    'duration_minutes', 'call_result', 'follow_up_required', 'region', 'channel'
]

def validate_schema(df, required_columns):
    """Проверяет наличие обязательных столбцов в DataFrame."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f'Отсутствуют обязательные столбцы: {missing}')
        raise ValueError(f'Отсутствуют обязательные столбцы: {missing}') 

def clean_and_normalize(df):
    """Очищает и нормализует данные: удаляет пропуски, приводит текст к нижнему регистру."""
    if 'conversation_text' in df.columns:
        df['conversation_text'] = df['conversation_text'].astype(str).str.lower().str.replace(r'[^\w\s]', '', regex=True)
    # Добавьте другие шаги нормализации по необходимости
    df = df.dropna(subset=['conversation_id', 'conversation_text'])
    return df

def get_data_from_db():
    """Пытается загрузить данные из БД."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('SELECT * FROM transcripts', conn)
        conn.close()
        logger.info('Данные успешно загружены из базы данных.')
        return df
    except Exception as e:
        logger.warning(f'Не удалось получить данные из БД: {e}')
        return None

def get_data_from_csv():
    """Пытается загрузить данные из CSV."""
    try:
        df = pd.read_csv(CSV_PATH)
        logger.info('Данные успешно загружены из CSV файла.')
        return df
    except Exception as e:
        logger.warning(f'Не удалось получить данные из CSV: {e}')
        return None

def generate_and_save_data():
    """Генерирует тестовые данные в формате эталонного датасета."""
    data = {
        'conversation_id': [1, 2, 3],
        'client_id': [1001, 1002, 1003],
        'agent_id': [501, 502, 503],
        'timestamp': ['2025-06-10 10:00', '2025-06-10 11:00', '2025-06-10 12:00'],
        'conversation_text': [
            'добрый день, хочу узнать остаток по счету',
            'здравствуйте, интересует оформление ипотеки',
            'подскажите, почему не прошел платеж'
        ],
        'theme': ['информация', 'ипотека', 'жалоба'],
        'product': ['счет', 'ипотека', 'платеж'],
        'product_keywords': ['остаток', 'оформление', 'ошибка'],
        'emotion': ['нейтральная', 'позитивная', 'негативная'],
        'client_satisfaction': [4, 5, 2],
        'duration_minutes': [3, 10, 5],
        'call_result': ['решено', 'требуется время', 'решено'],
        'follow_up_required': [False, True, False],
        'region': ['Москва', 'Санкт-Петербург', 'Казань'],
        'channel': ['чат', 'чат', 'чат']
    }
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    logger.info('Сгенерированы и сохранены тестовые данные в CSV.')
    return df

def load_transcripts():
    """
    Загружает транскрипты по алгоритму: БД → CSV → генерация тестовых данных.
    Проверяет схему и нормализует данные.
    """
    df = get_data_from_db()
    validate_schema(df, REQUIRED_COLUMNS)
    if df is None:
        df = get_data_from_csv()
    if df is None:
        df = generate_and_save_data()
    validate_schema(df, REQUIRED_COLUMNS)
    df = clean_and_normalize(df)
    df.to_csv('data/processed/transcripts_versioned.csv', index=False)
    logger.info(f'Загружено {len(df)} строк, версия датасета сохранена.')
    return df

if __name__ == '__main__':
    df = load_transcripts()
    print(df.head())
