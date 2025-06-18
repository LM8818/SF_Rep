"""
Модуль для работы с конфигурацией системы
"""

import logging
import logging.config
from pathlib import Path
from typing import Dict, Any
import yaml
from pydantic import BaseModel, validator


class DataConfig(BaseModel):
    """Конфигурация для работы с данными"""
    raw_path: str = "data/raw"
    processed_path: str = "data/processed"
    db_path: str = "bankingnlp.db"
    
    @validator('raw_path', 'processed_path')
    def validate_paths(cls, v):
        Path(v).mkdir(parents=True, exist_ok=True)
        return v


class ModelConfig(BaseModel):
    """Конфигурация модели машинного обучения"""
    model_type: str = "random_forest"
    test_size: float = 0.2
    random_state: int = 42
    n_estimators: int = 100
    max_depth: int = 10
    
    @validator('test_size')
    def validate_test_size(cls, v):
        if not 0 < v < 1:
            raise ValueError('test_size должен быть между 0 и 1')
        return v


class PreprocessingConfig(BaseModel):
    """Конфигурация предобработки текста"""
    min_text_length: int = 5
    max_text_length: int = 1000
    remove_stopwords: bool = True
    lemmatize: bool = True
    anonymize: bool = True


class Config(BaseModel):
    """Главная конфигурация системы"""
    DataConfig = DataConfig()
    model: ModelConfig = ModelConfig()
    preprocessing: PreprocessingConfig = PreprocessingConfig()


def load_config(config_path: str) -> Config:
    """
    Загружает конфигурацию из YAML файла
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        Объект конфигурации
        
    Raises:
        FileNotFoundError: Если файл конфигурации не найден
        yaml.YAMLError: Если файл содержит некорректный YAML
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        
        return Config(**config_dict)
        
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Ошибка парсинга YAML файла: {e}")


def setup_logging(level: int = logging.INFO):
    """
    Настройка системы логирования
    
    Args:
        level: Уровень логирования
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': logging.DEBUG,
                'formatter': 'detailed',
                'filename': 'logs/banking_nlp.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf-8'
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': level,
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)
