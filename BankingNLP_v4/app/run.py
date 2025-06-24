#!/usr/bin/env python3
"""
BankingNLP v2 - Главный файл запуска
Система анализа банковских диалогов с использованием NLP

Автор: LM8818
Версия: 2.0.0
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from src.utils.config import load_config, setup_logging
from src.data.load_data import load_transcripts
from src.features.build_features import build_features
from src.models.train_model import train_model
from src.models.predict_model import predict_model

logger = logging.getLogger(__name__)


def setup_environment():
    """
    Настройка рабочего окружения
    Создает необходимые директории и проверяет зависимости
    """
    directories = ['logs', 'data/raw', 'data/processed', 'models', 'reports']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Создана директория: {directory}")


def run_training_pipeline(config_path: str, data_path: Optional[str] = None):
    """
    Запуск полного пайплайна обучения модели
    
    Args:
        config_path: Путь к файлу конфигурации
        data_path: Путь к данным для обучения (опционально)
    """
    logger.info("Запуск пайплайна обучения модели")
    
    try:
        # Загрузка конфигурации
        config = load_config(config_path)
        
        # Загрузка данных
        logger.info("Загрузка данных...")
        data = load_transcripts(config, data_path)
        
        # Построение признаков
        logger.info("Извлечение признаков...")
        features = build_features(data, config)
        
        # Обучение модели
        logger.info("Обучение модели...")
        model_metrics = train_model(features, config)
        
        logger.info(f"Обучение завершено. Точность: {model_metrics.get('accuracy', 'N/A')}")
        
    except Exception as e:
        logger.error(f"Ошибка в пайплайне обучения: {e}")
        raise


def run_prediction_pipeline(config_path: str, input_text: str):
    """
    Запуск пайплайна предсказания для одного текста
    
    Args:
        config_path: Путь к файлу конфигурации
        input_text: Текст для анализа
    """
    logger.info("Запуск пайплайна предсказания")
    
    try:
        config = load_config(config_path)
        result = predict_model(input_text, config)
        
        print(f"Результат анализа:")
        print(f"Тема: {result.get('theme', 'Не определена')}")
        print(f"Эмоция: {result.get('emotion', 'Не определена')}")
        print(f"Уверенность: {result.get('confidence', 0):.3f}")
        
    except Exception as e:
        logger.error(f"Ошибка в пайплайне предсказания: {e}")
        raise


def main():
    """Главная функция программы"""
    parser = argparse.ArgumentParser(
        description="BankingNLP v2 - Анализ банковских диалогов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python run.py train --config config/default.yaml
  python run.py predict --config config/default.yaml --text "Хочу узнать баланс карты"
  python run.py train --config config/default.yaml --data data/custom_data.csv
        """
    )
    
    parser.add_argument(
        'command',
        choices=['train', 'predict'],
        help='Команда для выполнения'
    )
    
    parser.add_argument(
        '--config',
        default='src/config/config.yaml',
        help='Путь к файлу конфигурации (по умолчанию: src/config/config.yaml)'
    )
    
    parser.add_argument(
        '--data',
        help='Путь к данным для обучения (только для команды train)'
    )
    
    parser.add_argument(
        '--text',
        help='Текст для анализа (только для команды predict)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Подробный вывод'
    )
    
    args = parser.parse_args()
    
    # Настройка логирования
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    # Настройка окружения
    setup_environment()
    
    try:
        if args.command == 'train':
            run_training_pipeline(args.config, args.data)
        elif args.command == 'predict':
            if not args.text:
                parser.error("Для команды predict требуется параметр --text")
            run_prediction_pipeline(args.config, args.text)
            
    except KeyboardInterrupt:
        logger.info("Выполнение прервано пользователем")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
