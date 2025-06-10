"""
Интеграционные тесты для API Banking NLP System
==============================================

Тесты для проверки работы REST API endpoints
и корректности обработки HTTP запросов.
"""

import pytest
from fastapi.testclient import TestClient
from src.banking_nlp.main import app


class TestAPI:
    """Тесты для API endpoints"""

    @pytest.fixture
    def client(self):
        """Фикстура для тестового клиента"""
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Тест корневого endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data

    def test_health_endpoint(self, client):
        """Тест health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data

    def test_analyze_endpoint(self, client):
        """Тест основного endpoint анализа"""
        request_data = {
            "text": "Хочу взять кредит на покупку машины",
            "language": "ru"
        }

        response = client.post("/api/analyze", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert "themes" in data
        assert "products" in data
        assert "emotions" in data
        assert "confidence" in data

    def test_analyze_empty_text(self, client):
        """Тест анализа пустого текста"""
        request_data = {
            "text": "",
            "language": "ru"
        }

        response = client.post("/api/analyze", json=request_data)

        assert response.status_code == 400

    def test_get_themes(self, client):
        """Тест получения списка тематик"""
        response = client.get("/api/themes")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_products(self, client):
        """Тест получения списка продуктов"""
        response = client.get("/api/products")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_batch_analysis(self, client):
        """Тест пакетного анализа"""
        request_data = [
            {"text": "Хочу кредит", "language": "ru"},
            {"text": "Проблемы с картой", "language": "ru"}
        ]

        response = client.post("/api/analyze/batch", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_statistics_endpoint(self, client):
        """Тест получения статистики"""
        response = client.get("/api/statistics")

        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
