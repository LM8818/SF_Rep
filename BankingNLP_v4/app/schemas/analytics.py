from typing import Optional, List, Dict, Any
from datetime import date
from pydantic import BaseModel

class AnalyticsReportQuery(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    group_by: Optional[str] = "theme"
    top_n: Optional[int] = 10

class AnalyticsReportItem(BaseModel):
    theme: Optional[str]
    product: Optional[str]
    emotion: Optional[str]
    count: int
    avg_emotion: Optional[str]
    top_products: Optional[List[str]]

class AnalyticsReportResponse(BaseModel):
    group_by: str
    period: Dict[str, date]
    results: List[AnalyticsReportItem]

class StatisticsSummaryQuery(BaseModel):
    period: Optional[str] = "week"
    user_id: Optional[str]

class StatisticsSummaryResponse(BaseModel):
    period: str
    total_conversations: int
    unique_users: int
    avg_conversation_length: float
    top_channels: List[str] 