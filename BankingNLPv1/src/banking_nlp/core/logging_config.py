"""
Конфигурация системы логирования Banking NLP System
==================================================

Обеспечивает централизованное логирование с поддержкой различных уровней,
форматирования и вывода в файлы и консоль.
"""

import os
import sys
import logging
import logging.config
from pathlib import Path
from typing import Dict, Any


def setup_logging(log_level: str = "INFO", log_file: str = "logs/app.log") -> None:
    """
    Настройка системы логирования

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу логов
    """

    # Создаем директорию для логов если не существует
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Конфигурация логирования
    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_file,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            }
        },
        "loggers": {
            "": {  # root logger
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "fastapi": {
                "level": "INFO", 
                "handlers": ["console", "file"],
                "propagate": False
            }
        }
    }

    # Применяем конфигурацию
    logging.config.dictConfig(config)

    # Логируем успешную настройку
    logger = logging.getLogger(__name__)
    logger.info(f"Система логирования настроена. Уровень: {log_level}, Файл: {log_file}")
