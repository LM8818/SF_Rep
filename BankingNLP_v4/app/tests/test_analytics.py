import pytest
import logging
from app.services.analytics_service import analyze_conversation  # замените на актуальный импорт

logger = logging.getLogger("test_analytics")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_analyze_conversation_basic():
    result = analyze_conversation("Привет, как дела?")
    assert "topics" in result
    logger.info("Проверка базового анализа разговора — успешно")

def test_analyze_conversation_empty():
    result = analyze_conversation("")
    assert result["topics"] == []
    logger.info("Проверка анализа пустого разговора — успешно") 