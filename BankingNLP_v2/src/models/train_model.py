import os
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import yaml

import logging.config
import yaml

def setup_logging():
    with open('logging.yaml') as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)

# Настройка логирования
log_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
)
log_handler = RotatingFileHandler('logs/model_train.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

MODEL_PATH = 'models/logreg_model.joblib'
FEATURES_PATH = 'data/processed/features.csv'

def load_config():
    """Загружает параметры из конфиг-файла (если есть)."""
    config_path = 'src/config/config.yaml'
    if os.path.exists(config_path):
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}

def train_model():
    """
    Обучает модель классификации тем обращения на основе подготовленных признаков.
    Алгоритм:
    1. Проверяет наличие файла с признаками.
    2. Загружает данные и выделяет целевую переменную ('theme').
    3. Оставляет только числовые признаки для обучения.
    4. Делит данные на обучающую и тестовую выборки.
    5. Обучает модель логистической регрессии.
    6. Сохраняет обученную модель с версией.
    7. Ведёт логирование этапов и ошибок.
    """
    try:
        if not os.path.exists(FEATURES_PATH):
            logger.error('Файл с признаками не найден. Обучение невозможно.')
            return

        df = pd.read_csv(FEATURES_PATH)
        if 'theme' not in df.columns:
            logger.error('В данных отсутствует колонка "theme".')
            return

        X = df.drop(columns=['theme'])
        y = df['theme']

        X = X.select_dtypes(include=['number'])
        if X.isnull().any().any():
            logger.error('В признаках есть пропуски, обучение невозможно.')
            raise ValueError('В признаках есть пропуски.')

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        config = load_config()
        max_iter = config.get('model', {}).get('max_iter', 500)
        model = LogisticRegression(max_iter=max_iter)
        model.fit(X_train, y_train)

        # Сохраняем модель с версией
        model_filename = f"models/logreg_model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.joblib"
        joblib.dump(model, model_filename)
        logger.info(f'Модель успешно обучена и сохранена: {model_filename}')
        print(f'Обучение завершено. Модель сохранена в {model_filename}')
    except Exception as e:
        logger.error(f'Ошибка при обучении модели: {e}')

if __name__ == '__main__':
    train_model()
