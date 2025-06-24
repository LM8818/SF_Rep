from fastapi import APIRouter, Body, Depends
from app.schemas.model import ModelRetrainRequest, ModelRetrainResponse
from app.services.model_service import retrain_model

router = APIRouter()

@router.post("/model/retrain", response_model=ModelRetrainResponse, summary="Запуск переобучения модели")
def model_retrain(request: ModelRetrainRequest = Body(...)):
    """Запустить переобучение модели по запросу пользователя или системы."""
    return retrain_model(request) 