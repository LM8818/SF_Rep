import os
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import joblib
import time

# Настройка логирования
log_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
)
log_handler = RotatingFileHandler('logs/model_predict.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

MODEL_PATH = 'models/logreg_model.joblib'
FEATURES_PATH = 'data/processed/features.csv'
PREDICTIONS_PATH = 'data/processed/predictions.csv'

def predict():
    """
    Выполняет предсказание классов для новых данных с помощью обученной модели.
    Алгоритм:
    1. Проверяет наличие обученной модели и файла с признаками.
    2. Загружает признаки и модель.
    3. Выполняет предсказание классов.
    4. Сохраняет результаты в отдельный CSV-файл.
    5. Логирует время инференса и ошибки.
    """
    try:
        start_time = time.time()
        if not os.path.exists(MODEL_PATH):
            logger.error('Файл обученной модели не найден. Предсказание невозможно.')
            return

        if not os.path.exists(FEATURES_PATH):
            logger.error('Файл с признаками не найден. Предсказание невозможно.')
            return

        df = pd.read_csv(FEATURES_PATH)
        X = df.drop(columns=['theme'], errors='ignore')
        X = X.select_dtypes(include=['number'])

        model = joblib.load(MODEL_PATH)
        predictions = model.predict(X)
        df['predicted_theme'] = predictions

        df.to_csv(PREDICTIONS_PATH, index=False)
        logger.info(f'Предсказания успешно выполнены и сохранены. Время инференса: {time.time() - start_time:.2f} сек, {len(df)} строк обработано.')
        print(f'Предсказания сохранены в {PREDICTIONS_PATH}')
    except Exception as e:
        logger.error(f'Ошибка при предсказании: {e}')

if __name__ == '__main__':
    predict()
