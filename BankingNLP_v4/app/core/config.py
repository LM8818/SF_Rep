"""
config.py
Централизованный объект настроек на базе Pydantic.

Использование:
    from app.core.config import settings
    print(settings.PROJECT_NAME)
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

# Принудительно устанавливаем переменную окружения для отладки
if os.getenv('API_AUTH_ENABLED') == 'false':
    os.environ['API_AUTH_ENABLED'] = 'false'
    print(f"DEBUG: Set API_AUTH_ENABLED to false")


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

    # ────────────────────────────
    # РУБИЛЬНИК АВТОРИЗАЦИИ
    # ────────────────────────────
    api_auth_enabled: bool = Field(True, env="API_AUTH_ENABLED")
    
    @field_validator('api_auth_enabled', mode='before')
    @classmethod
    def validate_api_auth_enabled(cls, v):
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)

    class Config:
        env_file = ".env"           # позволяем задавать переменные в .env
        case_sensitive = True       # имена ключей чувствительны к регистру


class LLMSettings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_timeout: int = 60  # секунд

    class Config:
        env_prefix = "LLM_"


# Экземпляр, который импортируется по всему проекту
settings = Settings()
llm_settings = LLMSettings()
