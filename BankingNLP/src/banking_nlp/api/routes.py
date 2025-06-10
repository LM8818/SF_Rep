"""
API маршруты Banking NLP System
=============================

Определяет REST API endpoints для анализа банковских разговоров,
включая классификацию тематик, анализ продуктов и эмоций.
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

from ..services.analysis import AnalysisService, AnalysisRequest, AnalysisResult
from ..services.health import HealthService

logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter()

# Инициализация сервисов
analysis_service = AnalysisService()
health_service = HealthService()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_conversation(request: AnalysisRequest):
    """
    Анализ банковского разговора
    """
    try:
        logger.info(f"Получен запрос на анализ текста длиной {len(request.text)} символов")

        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Текст для анализа не может быть пустым"
            )

        result = await analysis_service.analyze(request)

        logger.info(f"Анализ завершен. Найдено тематик: {len(result.themes)}, продуктов: {len(result.products)}")
        return result

    except ValueError as e:
        logger.warning(f"Ошибка валидации данных: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Ошибка анализа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка анализа: {str(e)}"
        )


@router.post("/analyze/batch", response_model=List[AnalysisResult])
async def analyze_conversations_batch(requests: List[AnalysisRequest]):
    """
    Пакетный анализ нескольких разговоров
    """
    try:
        logger.info(f"Получен пакетный запрос на анализ {len(requests)} разговоров")

        if len(requests) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Максимальное количество разговоров в пакете: 100"
            )

        results = []
        for i, request in enumerate(requests):
            try:
                result = await analysis_service.analyze(request)
                results.append(result)
            except Exception as e:
                logger.error(f"Ошибка анализа разговора {i}: {e}")
                error_result = AnalysisResult(
                    themes=[],
                    products=[],
                    emotions={},
                    confidence=0.0,
                    error=str(e)
                )
                results.append(error_result)

        logger.info(f"Пакетный анализ завершен. Обработано: {len(results)} разговоров")
        return results

    except Exception as e:
        logger.error(f"Ошибка пакетного анализа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка пакетного анализа: {str(e)}"
        )


@router.get("/themes", response_model=List[str])
async def get_available_themes():
    """
    Получение списка доступных тематик для классификации
    """
    try:
        themes = analysis_service.get_available_themes()
        return themes
    except Exception as e:
        logger.error(f"Ошибка получения списка тематик: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения списка тематик"
        )


@router.get("/products", response_model=List[str])
async def get_available_products():
    """
    Получение списка банковских продуктов
    """
    try:
        products = analysis_service.get_available_products()
        return products
    except Exception as e:
        logger.error(f"Ошибка получения списка продуктов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения списка продуктов"
        )


@router.get("/statistics")
async def get_system_statistics():
    """
    Получение статистики работы системы
    """
    try:
        stats = await health_service.get_system_statistics()
        return stats
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения статистики системы"
        )


@router.get("/health")
async def health_check():
    """
    Проверка здоровья API
    """
    try:
        health_status = await health_service.check_health()
        return health_status
    except Exception as e:
        logger.error(f"Ошибка проверки здоровья: {e}")
        return {"status": "unhealthy", "error": str(e)}
