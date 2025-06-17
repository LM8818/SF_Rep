import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import os

# Настройка логирования
log_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
)
log_handler = RotatingFileHandler('logs/features.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def extract_text_features(df):
    """
    Генерирует текстовые признаки: длина сообщения, количество слов и др.
    """
    df['message_length'] = df['conversation_text'].astype(str).apply(len)
    df['word_count'] = df['conversation_text'].astype(str).apply(lambda x: len(x.split()))
    return df

def extract_time_features(df):
    """
    Генерирует временные признаки: час обращения, день недели.
    """
    if 'timestamp' in df.columns:
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['weekday'] = pd.to_datetime(df['timestamp']).dt.weekday
    return df

def build_features(df):
    """
    Основная функция для генерации всех признаков.
    """
    df = extract_text_features(df)
    df = extract_time_features(df)
    # Можно добавить другие группы признаков
    if df.isnull().any().any():
        logger.warning('В данных после генерации признаков есть пропуски!')
    logger.info(f'Добавлено {df.shape[1]} признаков.')
    return df

if __name__ == '__main__':
    data_path = 'data/processed/transcripts.csv'
    features_path = 'data/processed/features.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df = build_features(df)
        df.to_csv(features_path, index=False)
        print(df.head())
    else:
        logger.error('Файл с транскриптами не найден.')
