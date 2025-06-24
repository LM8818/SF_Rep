import pytest
import logging
from fastapi.testclient import TestClient
from app.main import app

logger = logging.getLogger("test_api_endpoints")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    logger.info("Проверка корневого эндпоинта — успешно")

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    logger.info("Проверка эндпоинта /health — успешно")

def test_analytics_report():
    response = client.get("/api/v1/analytics/report?group_by=theme&top_n=2")
    assert response.status_code == 200
    data = response.json()
    assert "group_by" in data
    assert "results" in data
    assert isinstance(data["results"], list)

def test_statistics_summary():
    response = client.get("/api/v1/statistics/summary?period=week")
    assert response.status_code == 200
    data = response.json()
    assert "total_conversations" in data
    assert "unique_users" in data

def test_model_retrain():
    payload = {
        "triggered_by": "admin",
        "data_range": {"start": "2024-06-01", "end": "2024-06-30"},
        "model_type": "llm"
    }
    response = client.post("/api/v1/model/retrain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "started"

def test_integration_crm_push_results():
    payload = {
        "conversation_id": "abc123",
        "results": {
            "theme": "ипотека",
            "products": ["Ипотека 2024"],
            "emotion": "positive",
            "satisfaction": 0.92
        },
        "crm_endpoint": "https://crm.sovcombank.ru/api/v1/receive"
    }
    response = client.post("/api/v1/integration/crm/push_results", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_monitoring_alerts_get():
    response = client.get("/api/v1/monitoring/alerts?level=critical")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list)

def test_monitoring_alerts_post():
    payload = {"event": "Test event", "details": {"info": "test"}}
    response = client.post("/api/v1/monitoring/alerts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list) 