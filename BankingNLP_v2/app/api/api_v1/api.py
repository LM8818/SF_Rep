"""
api.py
Единый роутер для API-верcии v1.

Подключается в app/main.py:
    from app.api.api_v1.api import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
"""

from fastapi import APIRouter

# Импорт отдельных групп эндпоинтов
from app.api.api_v1.endpoints import nlp  # noqa: F401

# «главный» роутер версии v1
api_router = APIRouter()

# Регистрируем вложенные роутеры
api_router.include_router(
    nlp.router,          # сам роутер
    prefix="/nlp",       # общий префикс → /api/v1/nlp/…
    tags=["nlp"],        # тег в Swagger-документации
)
