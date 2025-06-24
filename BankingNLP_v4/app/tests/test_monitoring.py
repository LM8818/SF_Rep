import pytest
import logging
from app.services.monitoring_service import check_alerts  # замените на актуальный импорт

logger = logging.getLogger("test_monitoring")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_check_alerts_normal():
    alerts = check_alerts()
    assert isinstance(alerts, list)
    logger.info("Проверка получения алертов мониторинга — успешно") 