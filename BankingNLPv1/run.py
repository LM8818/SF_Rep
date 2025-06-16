#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banking NLP System - Скрипт автоматического запуска с инициализацией данных
"""
import sys
import subprocess
import platform
from pathlib import Path

from src.banking_nlp.core.logging_config import setup_logging

setup_logging(log_level="INFO", log_file="logs/app.log")

import logging
logger = logging.getLogger(__name__)

def check_and_install_dependencies():
    """Проверка и установка зависимостей"""
    required_packages = [
        "fastapi>=0.115.2",
        "uvicorn>=0.32.0", 
        "pydantic>=2.9.2",
        "pandas>=2.0.0",
        "faker>=20.0.0",
        "psutil>=5.9.0"
    ]
    
    ("📦 Проверка зависимостей...")
    
    try:
        for package in required_packages:
            package_name = package.split(">=")[0]
            __import__(package_name.replace("-", "_"))
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("🔧 Установка недостающих зависимостей...")
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install"
        ] + required_packages)
        
        print("✅ Зависимости установлены")
        return True

def main():
    """Основная функция запуска с автоматической инициализацией"""
    print("🏦 Banking NLP System - Автоматический запуск с данными")
    print("=" * 60)
    
    # Проверяем Python версию
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        sys.exit(1)
    
    logger.info("✅ Python {sys.version.split()[0]}")
    
    # Проверяем и устанавливаем зависимости
    check_and_install_dependencies()
    
    logger.info("🚀 Запуск Banking NLP System...")
    logger.info("📊 Данные будут автоматически созданы при первом запуске")
    logger.info("🌐 После запуска система будет доступна на http://localhost:8000")
    logger.info("📋 API данных: http://localhost:8000/api/data/conversations")
    logger.info("-" * 60)
    
    # Запускаем приложение
    try:
        from src.banking_nlp.main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
