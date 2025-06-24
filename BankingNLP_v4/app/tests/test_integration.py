import pytest
import logging
from app.services.integration_service import integrate_with_crm  # замените на актуальный импорт

logger = logging.getLogger("test_integration")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_integrate_with_crm_success():
    result = integrate_with_crm({"client_id": 1, "data": "test"})
    assert result["status"] == "ok"
    logger.info("Проверка успешной интеграции с CRM — успешно")

def test_integrate_with_crm_fail():
    result = integrate_with_crm({"client_id": None, "data": "test"})
    assert result["status"] == "error"
    logger.info("Проверка обработки ошибки интеграции с CRM — успешно") 