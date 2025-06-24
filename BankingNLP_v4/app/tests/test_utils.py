import pytest
import logging
import time
from app.utils.utils import some_util_function  # замените на актуальный импорт вашей функции

logger = logging.getLogger("test_utils")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_utils.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_utils.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

def test_some_util_function():
    test_name = "test_some_util_function"
    params = {"a": 2, "b": 3}
    log_test_start(test_name, **params)
    start = time.time()
    result = some_util_function(2, 3)
    try:
        assert result == 5  # замените на актуальную проверку
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise
