from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any
import logging

from app.services.nlp_service import nlp_service
from app.schemas.nlp import ConversationAnalysisRequest, ConversationAnalysisResponse
from app.core.security import JWTBearer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=ConversationAnalysisResponse)
async def analyze_conversation(
    request: ConversationAnalysisRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(JWTBearer())
):
    """Анализ текста разговора с клиентом"""
    try:
        result = await nlp_service.analyze_conversation(request.text)
        
        # Логирование для аудита
        background_tasks.add_task(
            log_analysis_request,
            user_token=token,
            text_length=len(request.text),
            result=result
        )
        
        return ConversationAnalysisResponse(**result)
    except Exception as e:
        logger.error(f"Ошибка при анализе разговора: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса"
        )

@router.post("/batch-analyze")
async def batch_analyze_conversations(
    requests: List[ConversationAnalysisRequest],
    token: str = Depends(JWTBearer())
):
    """Пакетный анализ разговоров"""
    if len(requests) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Максимум 100 разговоров за раз"
        )
    
    results = []
    for request in requests:
        try:
            result = await nlp_service.analyze_conversation(request.text)
            results.append(result)
        except Exception as e:
            logger.error(f"Ошибка при анализе разговора: {e}")
            results.append({"error": str(e)})
    
    return {"results": results, "processed_count": len(results)}

@router.get("/themes")
async def get_available_themes(token: str = Depends(JWTBearer())):
    """Получение списка доступных тем для классификации"""
    return {"themes": nlp_service.themes}

@router.post("/retrain")
async def retrain_model(
    background_tasks: BackgroundTasks,
    token: str = Depends(JWTBearer())
):
    """Переобучение модели NLP"""
    background_tasks.add_task(nlp_service.train_new_model)
    return {"message": "Переобучение модели запущено в фоновом режиме"}

async def log_analysis_request(user_token: str, text_length: int, result: Dict[str, Any]):
    """Логирование запросов для аудита"""
    logger.info(f"NLP анализ выполнен: длина текста={text_length}, тема={result.get('theme')}")
