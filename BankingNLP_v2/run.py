import logging
import logging.config
import yaml
import sys

# Импортируем модули пайплайна
from src.data.load_data import load_transcripts
from src.features.build_features import build_features
from src.models.train_model import train_model
from src.models.predict_model import predict
from src.evaluation.evaluate import evaluate

def setup_logging():
    """Настраивает логирование из файла logging.yaml, если он есть."""
    try:
        with open('logging.yaml') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().warning("Не удалось загрузить logging.yaml, используется базовая настройка логирования.")

def main(step='all'):
    """
    Запускает пайплайн BankingNLP.
    step: 'all' или одна из стадий: data, features, train, predict, eval
    """
    logger = logging.getLogger("run")
    try:
        if step in ('all', 'data'):
            logger.info("=== Загрузка и подготовка данных ===")
            df = load_transcripts()
        if step in ('all', 'features'):
            logger.info("=== Генерация признаков ===")
            import pandas as pd
            df = pd.read_csv('data/processed/transcripts.csv')
            df = build_features(df)
            df.to_csv('data/processed/features.csv', index=False)
        if step in ('all', 'train'):
            logger.info("=== Обучение модели ===")
            train_model()
        if step in ('all', 'predict'):
            logger.info("=== Предсказание ===")
            predict()
        if step in ('all', 'eval'):
            logger.info("=== Оценка качества ===")
            evaluate()
        logger.info("Пайплайн успешно завершён.")
    except Exception as e:
        logger.exception(f"Ошибка в пайплайне: {e}")

if __name__ == "__main__":
    setup_logging()
    # Поддержка CLI-аргументов: python run.py [all|data|features|train|predict|eval]
    step = sys.argv[1] if len(sys.argv) > 1 else 'all'
    main(step)
