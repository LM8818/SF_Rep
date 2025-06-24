from fastapi import APIRouter, Query, Body, Depends
from typing import Optional
from app.schemas.monitoring import AlertGetQuery, AlertResponse, AlertCreateRequest
from app.services.monitoring_service import get_alerts, create_alert

router = APIRouter()

@router.get("/monitoring/alerts", response_model=AlertResponse, summary="Получение алертов")
def get_monitoring_alerts(
    level: Optional[str] = Query(None, regex="^(info|warning|critical)$"),
    since: Optional[str] = Query(None)
):
    """Получить список алертов по уровню и дате."""
    query = AlertGetQuery(level=level, since=since)
    return get_alerts(query)

@router.post("/monitoring/alerts", response_model=AlertResponse, summary="Создание алерта")
def create_monitoring_alert(request: AlertCreateRequest = Body(...)):
    """Создать новый алерт по событию в системе."""
    return create_alert(request) 