from fastapi import APIRouter, Query, Depends
from typing import Optional, List
from datetime import date
from app.schemas.analytics import AnalyticsReportResponse, AnalyticsReportQuery, StatisticsSummaryResponse, StatisticsSummaryQuery
from app.services.analytics_service import get_analytics_report, get_statistics_summary

router = APIRouter()

@router.get("/analytics/report", response_model=AnalyticsReportResponse, summary="Выгрузка аналитических отчётов")
def analytics_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    group_by: Optional[str] = Query("theme", regex="^(theme|product|emotion|channel|day|week|month)$"),
    top_n: Optional[int] = Query(10, ge=1, le=100)
):
    """Получить аналитический отчёт по выбранной группировке и периоду."""
    query = AnalyticsReportQuery(
        start_date=start_date,
        end_date=end_date,
        group_by=group_by,
        top_n=top_n
    )
    return get_analytics_report(query)

@router.get("/statistics/summary", response_model=StatisticsSummaryResponse, summary="Сводная статистика по пользователям/разговорам")
def statistics_summary(
    period: Optional[str] = Query("week", regex="^(day|week|month)$"),
    user_id: Optional[str] = Query(None)
):
    """Получить сводную статистику по выбранному периоду и пользователю."""
    query = StatisticsSummaryQuery(period=period, user_id=user_id)
    return get_statistics_summary(query) 