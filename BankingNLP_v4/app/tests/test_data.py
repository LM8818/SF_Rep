import pytest
import logging
import time
from app.old_data.load_data import load_raw_data

logger = logging.getLogger("test_data")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_data.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_data.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

def test_load_raw_data_success(tmp_path):
    test_name = "test_load_raw_data_success"
    params = {"file": "test.csv"}
    log_test_start(test_name, **params)
    start = time.time()
    test_file = tmp_path / "test.csv"
    with open(test_file, "w") as f:
        f.write("text\nПример\n")
    data = load_raw_data(str(test_file))
    try:
        assert isinstance(data, list)
        assert data[0]["text"] == "Пример"
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise

def test_load_raw_data_empty(tmp_path):
    test_name = "test_load_raw_data_empty"
    params = {"file": "empty.csv"}
    log_test_start(test_name, **params)
    start = time.time()
    test_file = tmp_path / "empty.csv"
    with open(test_file, "w") as f:
        f.write("text\n")
    data = load_raw_data(str(test_file))
    try:
        assert data == []
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise

def test_load_raw_data_file_not_found():
    test_name = "test_load_raw_data_file_not_found"
    params = {"file": "not_exists.csv"}
    log_test_start(test_name, **params)
    start = time.time()
    try:
        with pytest.raises(FileNotFoundError):
            load_raw_data("not_exists.csv")
        log_test_end(test_name, time.time()-start, result="ожидаемая ошибка")
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise
