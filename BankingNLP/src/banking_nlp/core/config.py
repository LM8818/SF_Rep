"""
Система конфигурации Banking NLP System
=======================================

Обеспечивает централизованное управление настройками с валидацией через Pydantic
и поддержкой различных окружений (development, staging, production).
"""

import os
from enum import Enum
from typing import Optional, List, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Доступные окружения для развертывания"""
    DEVELOPMENT = "development"
    STAGING = "staging" 
    PRODUCTION = "production"


class DatabaseConfig(BaseModel):
    """Конфигурация базы данных"""
    host: str = Field(default="localhost", description="Хост базы данных")
    port: int = Field(default=5432, description="Порт базы данных")
    username: str = Field(default="postgres", description="Имя пользователя")
    password: str = Field(default="password", description="Пароль")
    database: str = Field(default="banking_nlp", description="Название базы данных")

    @property
    def url(self) -> str:
        """Строка подключения к базе данных"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class SecurityConfig(BaseModel):
    """Конфигурация безопасности"""
    secret_key: str = Field(default="your-secret-key-here", description="Секретный ключ для JWT")
    algorithm: str = Field(default="HS256", description="Алгоритм шифрования")
    token_expire_minutes: int = Field(default=30, description="Время жизни токена в минутах")
    encryption_key_path: Optional[str] = Field(default=None, description="Путь к ключу шифрования")


class MLConfig(BaseModel):
    """Конфигурация ML моделей"""
    model_name: str = Field(default="DeepPavlov/rubert-base-cased", description="Название модели BERT")
    max_length: int = Field(default=512, description="Максимальная длина токенов")
    batch_size: int = Field(default=16, description="Размер батча для обучения")
    confidence_threshold: float = Field(default=0.85, description="Порог уверенности модели")


class AppConfig(BaseSettings):
    """Основная конфигурация приложения"""

    # Основные настройки
    app_name: str = Field(default="Banking NLP System", description="Название приложения")
    version: str = Field(default="1.0.0", description="Версия приложения")
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Окружение")
    debug: bool = Field(default=True, description="Режим отладки")

    # Сетевые настройки
    host: str = Field(default="0.0.0.0", description="Хост для запуска")
    port: int = Field(default=8000, description="Порт для запуска")

    # Конфигурации подсистем
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    ml: MLConfig = Field(default_factory=MLConfig)

    # Настройки логирования
    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_file: str = Field(default="logs/app.log", description="Файл для логов")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


# Глобальная переменная для конфигурации
_settings: Optional[AppConfig] = None


def get_settings() -> AppConfig:
    """
    Получение экземпляра конфигурации (Singleton pattern)

    Returns:
        AppConfig: Конфигурация приложения
    """
    global _settings
    if _settings is None:
        _settings = AppConfig()
    return _settings


def reload_settings() -> AppConfig:
    """
    Принудительная перезагрузка конфигурации

    Returns:
        AppConfig: Новая конфигурация приложения
    """
    global _settings
    _settings = AppConfig()
    return _settings
