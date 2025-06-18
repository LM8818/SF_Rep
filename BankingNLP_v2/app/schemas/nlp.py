"""
nlp.py
Pydantic-схемы запросов и ответов для NLP-эндпоинтов.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ────────────────────────────
# SCHEMA:  запрос на анализ одного разговора
# ────────────────────────────
class ConversationAnalysisRequest(BaseModel):
    text: str = Field(..., example="Добрый день! Хочу узнать про ипотеку…")
    client_id: Optional[str] = Field(None, example="123456")
    channel: Optional[str] = Field("чат", example="звонок")


# ────────────────────────────
# SCHEMA:  ответ анализа одного разговора
# ────────────────────────────
class ConversationAnalysisResponse(BaseModel):
    theme: str = Field(..., example="ипотека")
    confidence: float = Field(..., ge=0, le=1, example=0.92)
    emotion: str = Field(..., example="позитивная")
    products: List[str] = Field(default_factory=list, example=["ипотека"])
    satisfaction_score: int = Field(..., ge=1, le=5, example=4)
    processed_at: str = Field(..., example="2025-06-18T10:55:03Z")
    text_length: int = Field(..., example=87)
    word_count: int = Field(..., example=15)


# ────────────────────────────
# SCHEMA:  пакетный запрос (до 100 разговоров)
# ────────────────────────────
class BatchConversationRequest(BaseModel):
    conversations: List[ConversationAnalysisRequest] = Field(..., max_items=100)
