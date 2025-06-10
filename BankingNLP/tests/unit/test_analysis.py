"""
Тесты для сервиса анализа Banking NLP System
==========================================

Юнит-тесты для проверки корректности работы анализа тематик,
продуктов и эмоциональной окраски текста.
"""

import pytest
import asyncio
from src.banking_nlp.services.analysis import AnalysisService, AnalysisRequest, AnalysisResult


class TestAnalysisService:
    """Тесты для AnalysisService"""

    @pytest.fixture
    def analysis_service(self):
        """Фикстура для создания экземпляра сервиса"""
        return AnalysisService()

    @pytest.fixture
    def sample_request(self):
        """Фикстура с примером запроса"""
        return AnalysisRequest(
            text="Хочу взять потребительский кредит на покупку автомобиля. Какие условия?",
            language="ru"
        )

    def test_analysis_service_initialization(self, analysis_service):
        """Тест инициализации сервиса"""
        assert analysis_service is not None
        assert len(analysis_service.themes_dict) > 0
        assert len(analysis_service.products_dict) > 0
        assert len(analysis_service.emotion_keywords) > 0

    @pytest.mark.asyncio
    async def test_basic_analysis(self, analysis_service, sample_request):
        """Тест базового анализа"""
        result = await analysis_service.analyze(sample_request)

        assert isinstance(result, AnalysisResult)
        assert result.error is None
        assert result.confidence > 0
        assert result.processing_time is not None
        assert result.timestamp is not None

    @pytest.mark.asyncio
    async def test_theme_detection(self, analysis_service):
        """Тест определения тематик"""
        request = AnalysisRequest(text="У меня проблемы с кредитной картой")
        result = await analysis_service.analyze(request)

        assert "кредиты" in result.themes or "карты" in result.themes

    @pytest.mark.asyncio
    async def test_product_detection(self, analysis_service):
        """Тест определения продуктов"""
        request = AnalysisRequest(text="Хочу оформить ипотеку на квартиру")
        result = await analysis_service.analyze(request)

        assert len(result.products) > 0

    @pytest.mark.asyncio
    async def test_emotion_analysis(self, analysis_service):
        """Тест эмоционального анализа"""
        request = AnalysisRequest(text="Отличное обслуживание! Очень доволен банком!")
        result = await analysis_service.analyze(request)

        assert "positive" in result.emotions
        assert result.emotions["positive"] > result.emotions.get("negative", 0)

    @pytest.mark.asyncio
    async def test_empty_text(self, analysis_service):
        """Тест обработки пустого текста"""
        request = AnalysisRequest(text="")
        result = await analysis_service.analyze(request)

        # Должна быть ошибка валидации от Pydantic
        assert result.error is not None

    def test_get_available_themes(self, analysis_service):
        """Тест получения списка тематик"""
        themes = analysis_service.get_available_themes()

        assert isinstance(themes, list)
        assert len(themes) > 0
        assert "кредиты" in themes

    def test_get_available_products(self, analysis_service):
        """Тест получения списка продуктов"""
        products = analysis_service.get_available_products()

        assert isinstance(products, list)
        assert len(products) > 0
