from fastapi import APIRouter, Body, Depends
from app.schemas.integration import CRMPushResultsRequest, CRMPushResultsResponse
from app.services.integration_service import push_results_to_crm

router = APIRouter()

@router.post("/integration/crm/push_results", response_model=CRMPushResultsResponse, summary="Отправка результатов анализа в CRM")
def crm_push_results(request: CRMPushResultsRequest = Body(...)):
    """Отправить результаты анализа разговора во внешний CRM-сервис."""
    return push_results_to_crm(request) 