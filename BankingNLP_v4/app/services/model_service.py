from app.schemas.model import ModelRetrainRequest, ModelRetrainResponse

def retrain_model(request: ModelRetrainRequest) -> ModelRetrainResponse:
    # TODO: Реализовать запуск переобучения модели
    return ModelRetrainResponse(
        status="started",
        message=f"Retraining started for model: {request.model_type}, data: {request.data_range}"
    ) 