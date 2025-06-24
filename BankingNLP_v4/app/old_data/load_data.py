import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import pandas as pd
import sqlite3
import yaml
import re

# Загрузка основной конфигурации
with open('src/config/config.yaml', encoding='utf-8') as f:
    main_config = yaml.safe_load(f)

# Загрузка конфигурации логирования и паттернов анонимизации
try:
    with open('config/logging.yaml', 'r', encoding='utf-8') as f:
        logging_config = yaml.safe_load(f)
        
    # Настройка логирования
    logging.config.dictConfig(logging_config)
    
    # Загрузка паттернов анонимизации
    ANONYMIZATION_PATTERNS = logging_config['anonymization_patterns']
    
except FileNotFoundError:
    # Fallback конфигурация если файл не найден
    logging.basicConfig(level=logging.INFO)
    ANONYMIZATION_PATTERNS = {
        'phone': r'(\+7|8)?\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'card': r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',
        'account': r'\b\d{20}\b'
    }

# Компиляция регулярных выражений
PHONE_PATTERN = re.compile(ANONYMIZATION_PATTERNS['phone'])
EMAIL_PATTERN = re.compile(ANONYMIZATION_PATTERNS['email'])
CARD_PATTERN = re.compile(ANONYMIZATION_PATTERNS['card'])
ACCOUNT_PATTERN = re.compile(ANONYMIZATION_PATTERNS['account'])

# Получение логгера
logger = logging.getLogger(__name__)

# Константы
DB_PATH = os.getenv('BANKINGNLP_DB_PATH', 'bankingnlp.db')
CSV_PATH = 'data/processed/transcripts.csv'
REQUIRED_COLUMNS = [
    'conversation_id', 'client_id', 'agent_id', 'timestamp', 'conversation_text',
    'theme', 'product', 'product_keywords', 'emotion', 'client_satisfaction',
    'duration_minutes', 'call_result', 'follow_up_required', 'region', 'channel'
]

def anonymize_text(text: str) -> str:
    """Анонимизирует персональные данные в тексте."""
    text = PHONE_PATTERN.sub('[PHONE]', text)
    text = ACCOUNT_PATTERN.sub('[ACCOUNT]', text)
    text = EMAIL_PATTERN.sub('[EMAIL]', text)
    text = CARD_PATTERN.sub('[CARD]', text)
    return text

def remove_stopwords(text: str, stopwords: set) -> str:
    """Удаляет стоп-слова из текста."""
    return ' '.join([word for word in text.split() if word not in stopwords])

def validate_schema(df, required_columns):
    """Проверяет наличие обязательных столбцов в DataFrame."""
    if df is None:
        return
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f'Отсутствуют обязательные столбцы: {missing}')
        raise ValueError(f'Отсутствуют обязательные столбцы: {missing}')

def clean_and_normalize(df):
    """Очищает и нормализует данные."""
    if 'conversation_text' in df.columns:
        df['conversation_text'] = df['conversation_text'].astype(str).str.lower().str.replace(r'[^\w\s]', '', regex=True)
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
    if df is not None:
        validate_schema(df, REQUIRED_COLUMNS)
    
    if df is None:
        df = get_data_from_csv()
        if df is not None:
            validate_schema(df, REQUIRED_COLUMNS)
    
    if df is None:
        df = generate_and_save_data()
        validate_schema(df, REQUIRED_COLUMNS)
    
    df = clean_and_normalize(df)
    
    # Создаем директорию если не существует
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/transcripts_versioned.csv', index=False)
    logger.info(f'Загружено {len(df)} строк, версия датасета сохранена.')
    return df

if __name__ == '__main__':
    df = load_transcripts()
    print(df.head())
