"""
config.py
Централизованный объект настроек на базе Pydantic.

Использование:
    from app.core.config import settings
    print(settings.PROJECT_NAME)
"""

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # ────────────────────────────
    # ОБЩИЕ ПАРАМЕТРЫ
    # ────────────────────────────
    PROJECT_NAME: str = Field("Banking NLP API", env="PROJECT_NAME")
    API_V1_STR: str = "/api/v1"
    
    # Добавляем базовый URL для гибкости
    BASE_URL: str = Field("", env="BASE_URL")  # для проксирования    

    # ────────────────────────────
    # БЕЗОПАСНОСТЬ
    # ────────────────────────────
    SECRET_KEY: str = Field("please-set-real-secret", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ────────────────────────────
    # БАЗА ДАННЫХ
    # ────────────────────────────
    DATABASE_URL: str = Field(
        "sqlite:///bankingnlp.db",
        env="DATABASE_URL",
        description="Строка подключения SQLAlchemy"
    )

    # ────────────────────────────
    # СИСТЕМНЫЕ ПАРАМЕТРЫ
    # ────────────────────────────
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"           # позволяем задавать переменные в .env
        case_sensitive = True       # имена ключей чувствительны к регистру


# Экземпляр, который импортируется по всему проекту
settings = Settings()
