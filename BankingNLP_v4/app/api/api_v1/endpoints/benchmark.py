from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResponse
from app.services.benchmark_service import run_performance_benchmark

router = APIRouter()

@router.post("/benchmark/performance", response_model=BenchmarkResponse, summary="Тестирование скорости обработки")
def benchmark_performance(
    records_count: Optional[int] = Query(10000, ge=1000, le=50000, description="Количество записей для обработки")
):
    """Запустить бенчмарк производительности на указанном количестве записей из CSV."""
    request = BenchmarkRequest(records_count=records_count)
    return run_performance_benchmark(request) 