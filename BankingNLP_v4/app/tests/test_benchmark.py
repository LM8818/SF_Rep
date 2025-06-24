import pytest
import logging
import time
from fastapi.testclient import TestClient
from app.main import app
import os
import pandas as pd
from app.evaluation.evaluate import run_benchmark, BenchmarkResult

logger = logging.getLogger("test_benchmark")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

client = TestClient(app)

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_benchmark.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_benchmark.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

def test_benchmark_performance():
    """Тест эндпоинта бенчмарка производительности."""
    log_test_start("test_benchmark_performance")
    response = client.post("/api/v1/benchmark/performance?records_count=10000")
    assert response.status_code == 200
    logger.info("Проверка API-бенчмарка на 10 000 записей — успешно")
    
    data = response.json()
    assert "total_records" in data
    assert "total_time_seconds" in data
    assert "records_per_second" in data
    assert "memory_usage_mb" in data
    assert "results_file" in data
    assert "results" in data
    
    # Проверяем, что время обработки положительное
    assert data["total_time_seconds"] > 0
    assert data["records_per_second"] > 0
    
    # Проверяем, что CSV-файл создался
    results_file = data["results_file"]
    filepath = f"app/data/processed/{results_file}"
    assert os.path.exists(filepath)
    
    # Проверяем содержимое CSV
    df = pd.read_csv(filepath)
    assert len(df) > 0
    assert "record_id" in df.columns
    assert "theme" in df.columns
    assert "emotion" in df.columns
    logger.info("Проверка содержимого CSV-файла — успешно")
    log_test_end("test_benchmark_performance")

def test_benchmark_performance_invalid_count():
    """Тест с некорректным количеством записей."""
    log_test_start("test_benchmark_performance_invalid_count")
    response = client.post("/api/v1/benchmark/performance?records_count=100")
    assert response.status_code == 422
    logger.info("Проверка API-бенчмарка с некорректным количеством записей — успешно")
    log_test_end("test_benchmark_performance_invalid_count")

def test_benchmark_performance_large_count():
    """Тест с большим количеством записей."""
    log_test_start("test_benchmark_performance_large_count")
    response = client.post("/api/v1/benchmark/performance?records_count=50000")  # Максимум
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_records"] == 50000
    logger.info("Проверка большого количества записей — успешно")
    log_test_end("test_benchmark_performance_large_count")

def test_benchmark_csv_structure():
    """Тест структуры создаваемого CSV-файла."""
    log_test_start("test_benchmark_csv_structure")
    response = client.post("/api/v1/benchmark/performance?records_count=100")
    data = response.json()
    
    filepath = f"app/data/processed/{data['results_file']}"
    df = pd.read_csv(filepath)
    
    # Проверяем обязательные колонки
    required_columns = ["record_id", "theme", "emotion", "products", "processing_time_ms", "confidence"]
    for col in required_columns:
        assert col in df.columns
    
    # Проверяем, что есть метаданные в конце
    assert "META" in df["record_id"].values
    logger.info("Проверка структуры CSV-файла — успешно")
    log_test_end("test_benchmark_csv_structure")

def test_benchmark_performance_metrics():
    """Тест корректности метрик производительности."""
    log_test_start("test_benchmark_performance_metrics")
    response = client.post("/api/v1/benchmark/performance?records_count=1000")
    data = response.json()
    
    # Проверяем расчёт метрик
    total_time = data["total_time_seconds"]
    total_records = data["total_records"]
    avg_time_ms = data["avg_time_per_record_ms"]
    records_per_sec = data["records_per_second"]
    
    # Проверяем, что расчёты корректны
    assert abs(avg_time_ms - (total_time * 1000 / total_records)) < 0.1
    assert abs(records_per_sec - (total_records / total_time)) < 0.1 
    logger.info("Проверка корректности метрик производительности — успешно")
    log_test_end("test_benchmark_performance_metrics")

def test_run_benchmark_success(tmp_path):
    # Arrange
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "output.csv"
    with open(input_csv, "w") as f:
        f.write("text\nhello\nworld\n")
    llm = DummyLLM(response="answer")
    # Act
    result = run_benchmark(str(input_csv), str(output_csv), llm, timeout=2)
    # Assert
    assert isinstance(result, BenchmarkResult)
    assert result.success_count == 2
    assert result.fail_count == 0
    logger.info("Проверка успешного запуска бенчмарка — успешно")

def test_run_benchmark_timeout(tmp_path):
    class SlowLLM:
        def generate(self, prompt, **kwargs):
            import time
            time.sleep(2)
            return "slow"
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "output.csv"
    with open(input_csv, "w") as f:
        f.write("text\nhello\n")
    llm = SlowLLM()
    result = run_benchmark(str(input_csv), str(output_csv), llm, timeout=0.1)
    assert result.fail_count == 1
    logger.info("Проверка обработки таймаута в бенчмарке — успешно")

def test_run_benchmark_error(tmp_path):
    class ErrorLLM:
        def generate(self, prompt, **kwargs):
            raise Exception("Ошибка LLM")
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "output.csv"
    with open(input_csv, "w") as f:
        f.write("text\nhello\n")
    llm = ErrorLLM()
    result = run_benchmark(str(input_csv), str(output_csv), llm, timeout=1)
    assert result.fail_count == 1
    logger.info("Проверка обработки ошибки LLM в бенчмарке — успешно")

class DummyLLM:
    def __init__(self, response="ok"):
        self.response = response
    def generate(self, prompt, **kwargs):
        return self.response 