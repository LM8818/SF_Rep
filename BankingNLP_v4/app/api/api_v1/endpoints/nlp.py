"""
app/api/api_v1/endpoints/nlp.py

Роуты и бизнес-логика для NLP-эндпоинтов.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional
import logging

from app.schemas.nlp import (
    ConversationAnalysisRequest,
    ConversationAnalysisResponse,
    BatchConversationRequest,
)
from app.core.security import JWTBearer
from app.services.nlp_service import nlp_service
from app.core.config import Settings

# Создаем новый объект настроек для получения актуального значения
settings = Settings()

# Создаем два роутера - с авторизацией и без
router_auth = APIRouter()
router_no_auth = APIRouter()
logger = logging.getLogger(__name__)


# Функции для роутера с авторизацией
@router_auth.post(
    "/analyze",
    response_model=ConversationAnalysisResponse,
    summary="Анализ одного разговора",
    description="Выполняет анализ текста разговора и возвращает тему, эмоцию, продукты и оценку удовлетворенности.",
)
async def analyze_conversation_auth(
    request: ConversationAnalysisRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(JWTBearer()),
):
    """
    Анализирует текст разговора с клиентом (с авторизацией).
    """
    try:
        result = await nlp_service.analyze_conversation(request.text)

        # Логирование для аудита в фоне
        background_tasks.add_task(
            log_analysis_request,
            user_token=token,
            text_length=len(request.text),
            result=result,
        )

        return ConversationAnalysisResponse(**result)
    except Exception as e:
        logger.error(f"Ошибка при анализе разговора: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса",
        )


@router_auth.post(
    "/batch-analyze",
    summary="Пакетный анализ разговоров",
    description="Выполняет анализ списка разговоров (до 100 штук).",
)
async def batch_analyze_conversations_auth(
    requests: BatchConversationRequest,
    token: str = Depends(JWTBearer()),
):
    """
    Пакетный анализ нескольких разговоров (с авторизацией).
    """
    if len(requests.conversations) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Максимум 100 разговоров за раз",
        )

    results = []
    for conv in requests.conversations:
        try:
            result = await nlp_service.analyze_conversation(conv.text)
            results.append(result)
        except Exception as e:
            logger.error(f"Ошибка при анализе разговора: {e}")
            results.append({"error": str(e)})

    return {"results": results, "processed_count": len(results)}


@router_auth.get(
    "/themes",
    summary="Список доступных тем",
    description="Возвращает список тем, которые может распознавать модель.",
)
async def get_available_themes_auth(token: str = Depends(JWTBearer())):
    """
    Получение списка доступных тем для классификации (с авторизацией).
    """
    return {"themes": nlp_service.themes}


@router_auth.post(
    "/retrain",
    summary="Переобучение модели",
    description="Запускает переобучение модели NLP в фоновом режиме.",
)
async def retrain_model_auth(
    background_tasks: BackgroundTasks,
    token: str = Depends(JWTBearer()),
):
    """
    Запуск переобучения модели (с авторизацией).
    """
    background_tasks.add_task(nlp_service.train_new_model)
    return {"message": "Переобучение модели запущено в фоновом режиме"}


# Функции для роутера без авторизации
@router_no_auth.post(
    "/analyze",
    response_model=ConversationAnalysisResponse,
    summary="Анализ одного разговора",
    description="Выполняет анализ текста разговора и возвращает тему, эмоцию, продукты и оценку удовлетворенности.",
)
async def analyze_conversation_no_auth(
    request: ConversationAnalysisRequest,
    background_tasks: BackgroundTasks,
):
    """
    Анализирует текст разговора с клиентом (без авторизации).
    """
    try:
        result = await nlp_service.analyze_conversation(request.text)
        return ConversationAnalysisResponse(**result)
    except Exception as e:
        logger.error(f"Ошибка при анализе разговора: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса",
        )


@router_no_auth.post(
    "/batch-analyze",
    summary="Пакетный анализ разговоров",
    description="Выполняет анализ списка разговоров (до 100 штук).",
)
async def batch_analyze_conversations_no_auth(
    requests: BatchConversationRequest,
):
    """
    Пакетный анализ нескольких разговоров (без авторизации).
    """
    if len(requests.conversations) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Максимум 100 разговоров за раз",
        )

    results = []
    for conv in requests.conversations:
        try:
            result = await nlp_service.analyze_conversation(conv.text)
            results.append(result)
        except Exception as e:
            logger.error(f"Ошибка при анализе разговора: {e}")
            results.append({"error": str(e)})

    return {"results": results, "processed_count": len(results)}


@router_no_auth.get(
    "/themes",
    summary="Список доступных тем",
    description="Возвращает список тем, которые может распознавать модель.",
)
async def get_available_themes_no_auth():
    """
    Получение списка доступных тем для классификации (без авторизации).
    """
    return {"themes": nlp_service.themes}


@router_no_auth.post(
    "/retrain",
    summary="Переобучение модели",
    description="Запускает переобучение модели NLP в фоновом режиме.",
)
async def retrain_model_no_auth(
    background_tasks: BackgroundTasks,
):
    """
    Запуск переобучения модели (без авторизации).
    """
    background_tasks.add_task(nlp_service.train_new_model)
    return {"message": "Переобучение модели запущено в фоновом режиме"}


# Выбираем нужный роутер в зависимости от настроек
print(f"DEBUG: api_auth_enabled = {settings.api_auth_enabled}")
# Временно отключаем авторизацию для тестирования
router = router_no_auth


async def log_analysis_request(user_token: str, text_length: int, result: Dict[str, Any]):
    """
    Логирование запросов для аудита.
    """
    logger.info(
        f"NLP анализ выполнен: длина текста={text_length}, тема={result.get('theme')}"
    )
