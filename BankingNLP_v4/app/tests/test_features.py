import pytest
import logging
import time
from app.features.build_features import extract_features

logger = logging.getLogger("test_features")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_features.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_features.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

def test_extract_features_basic():
    test_name = "test_extract_features_basic"
    params = {"data": "2 строки"}
    log_test_start(test_name, **params)
    start = time.time()
    data = [
        {"text": "Привет, как дела?"},
        {"text": "Добрый день!"}
    ]
    features = extract_features(data)
    try:
        assert isinstance(features, list)
        assert len(features) == 2
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise

def test_extract_features_empty():
    test_name = "test_extract_features_empty"
    params = {"data": "пустой список"}
    log_test_start(test_name, **params)
    start = time.time()
    data = []
    features = extract_features(data)
    try:
        assert features == []
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise
