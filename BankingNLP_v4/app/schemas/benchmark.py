from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class BenchmarkRequest(BaseModel):
    records_count: int = 10000

class BenchmarkResult(BaseModel):
    record_id: str
    theme: str
    emotion: str
    products: List[str]
    processing_time_ms: float
    confidence: float

class BenchmarkResponse(BaseModel):
    total_records: int
    total_time_seconds: float
    avg_time_per_record_ms: float
    records_per_second: float
    memory_usage_mb: float
    results_file: str
    timestamp: datetime
    results: List[BenchmarkResult] 