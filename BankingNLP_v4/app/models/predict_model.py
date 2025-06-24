import os
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import joblib
import time
import logging.config
import yaml
import traceback

# Пути относительно корня проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'logreg_model.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'features.csv')
PREDICTIONS_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'predictions.csv')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOGS_DIR, 'model_predict.log')

# Настройка логирования

def setup_logging():
    """Загрузка централизованной конфигурации логирования из logging.yaml"""
    config_path = os.path.join(BASE_DIR, 'core', 'config', 'logging.yaml')
    if os.path.exists(config_path):
        with open(config_path, encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        print("logging.yaml не найден – используется базовая конфигурация.")

setup_logging()
logger = logging.getLogger(__name__)
if not logger.handlers:
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3, encoding='utf-8')
    log_formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


def predict_model():
    """
    Выполняет предсказание классов для новых данных с помощью обученной модели.

    Returns:
        None

    Raises:
        Logs errors and exceptions.
    """
    try:
        start_time = time.time()
        if not os.path.exists(MODEL_PATH):
            logger.error(f'Файл обученной модели не найден: {MODEL_PATH}. Предсказание невозможно.')
            return

        if not os.path.exists(FEATURES_PATH):
            logger.error(f'Файл с признаками не найден: {FEATURES_PATH}. Предсказание невозможно.')
            return

        df = pd.read_csv(FEATURES_PATH)
        if df.empty:
            logger.error('Файл признаков пустой. Предсказание невозможно.')
            return
        X = df.drop(columns=['theme'], errors='ignore')
        X = X.select_dtypes(include=['number'])

        model = joblib.load(MODEL_PATH)
        predictions = model.predict(X)
        df['predicted_theme'] = predictions

        df.to_csv(PREDICTIONS_PATH, index=False)
        logger.info(f'Предсказания успешно выполнены и сохранены. Время инференса: {time.time() - start_time:.2f} сек, {len(df)} строк обработано.')
        print(f'Предсказания сохранены в {PREDICTIONS_PATH}')
    except Exception as e:
        logger.error(f'Ошибка при предсказании: {e}\n{traceback.format_exc()}')

if __name__ == '__main__':
    predict_model()
