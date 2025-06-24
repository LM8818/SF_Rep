import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import Session
import logging

from app.models.conversation import Conversation
from app.models.analytics import AnalyticsReport
from app.core.database import get_db
from app.schemas.analytics import AnalyticsReportQuery, AnalyticsReportResponse, AnalyticsReportItem, StatisticsSummaryQuery, StatisticsSummaryResponse
from datetime import date

logger = logging.getLogger(__name__)

class BankingAnalyticsService:
    def __init__(self):
        self.product_mapping = {
            'кредит': 'CREDIT',
            'ипотека': 'MORTGAGE', 
            'карта': 'CARD',
            'вклад': 'DEPOSIT',
            'страхование': 'INSURANCE'
        }

    async def generate_daily_report(self, date: datetime) -> Dict[str, Any]:
        """Генерация ежедневного отчета по разговорам"""
        try:
            conversations = await self._get_conversations_by_date(date)
            
            report = {
                "date": date.isoformat(),
                "total_conversations": len(conversations),
                "themes_distribution": self._analyze_themes_distribution(conversations),
                "emotion_analysis": self._analyze_emotions(conversations),
                "product_mentions": self._analyze_product_mentions(conversations),
                "satisfaction_metrics": self._calculate_satisfaction_metrics(conversations),
                "conversion_opportunities": self._identify_conversion_opportunities(conversations),
                "risk_indicators": self._identify_risk_indicators(conversations)
            }
            
            return report
        except Exception as e:
            logger.error(f"Ошибка при генерации отчета: {e}")
            raise

    def _analyze_themes_distribution(self, conversations: List[Dict]) -> Dict[str, int]:
        """Анализ распределения тем разговоров"""
        themes = {}
        for conv in conversations:
            theme = conv.get('theme', 'неопределено')
            themes[theme] = themes.get(theme, 0) + 1
        return themes

    def _analyze_emotions(self, conversations: List[Dict]) -> Dict[str, Any]:
        """Анализ эмоциональной окраски разговоров"""
        emotions = {'позитивная': 0, 'негативная': 0, 'нейтральная': 0}
        total_satisfaction = 0
        
        for conv in conversations:
            emotion = conv.get('emotion', 'нейтральная')
            emotions[emotion] = emotions.get(emotion, 0) + 1
            total_satisfaction += conv.get('satisfaction_score', 3)
        
        avg_satisfaction = total_satisfaction / len(conversations) if conversations else 0
        
        return {
            "distribution": emotions,
            "average_satisfaction": round(avg_satisfaction, 2),
            "negative_ratio": emotions['негативная'] / len(conversations) if conversations else 0
        }

    def _analyze_product_mentions(self, conversations: List[Dict]) -> Dict[str, Any]:
        """Анализ упоминаний банковских продуктов"""
        product_stats = {}
        
        for conv in conversations:
            products = conv.get('products', [])
            for product in products:
                if product not in product_stats:
                    product_stats[product] = {
                        'mentions': 0,
                        'positive_mentions': 0,
                        'conversion_potential': 0
                    }
                
                product_stats[product]['mentions'] += 1
                
                if conv.get('emotion') == 'позитивная':
                    product_stats[product]['positive_mentions'] += 1
                
                if conv.get('satisfaction_score', 3) >= 4:
                    product_stats[product]['conversion_potential'] += 1
        
        return product_stats

    def _calculate_satisfaction_metrics(self, conversations: List[Dict]) -> Dict[str, float]:
        """Расчет метрик удовлетворенности"""
        if not conversations:
            return {}
        
        scores = [conv.get('satisfaction_score', 3) for conv in conversations]
        
        return {
            "average_score": sum(scores) / len(scores),
            "high_satisfaction_ratio": len([s for s in scores if s >= 4]) / len(scores),
            "low_satisfaction_ratio": len([s for s in scores if s <= 2]) / len(scores),
            "nps_score": self._calculate_nps(scores)
        }

    def _calculate_nps(self, scores: List[int]) -> float:
        """Расчет Net Promoter Score"""
        promoters = len([s for s in scores if s >= 4])
        detractors = len([s for s in scores if s <= 2])
        return ((promoters - detractors) / len(scores)) * 100 if scores else 0

    def _identify_conversion_opportunities(self, conversations: List[Dict]) -> List[Dict]:
        """Выявление возможностей для конверсии"""
        opportunities = []
        
        for conv in conversations:
            if (conv.get('satisfaction_score', 3) >= 4 and 
                conv.get('emotion') == 'позитивная' and
                conv.get('products')):
                
                opportunities.append({
                    "conversation_id": conv.get('id'),
                    "client_id": conv.get('client_id'),
                    "recommended_products": conv.get('products'),
                    "confidence": conv.get('confidence', 0.5),
                    "reason": "Высокая удовлетворенность и интерес к продуктам"
                })
        
        return opportunities

    def _identify_risk_indicators(self, conversations: List[Dict]) -> List[Dict]:
        """Выявление индикаторов риска"""
        risks = []
        
        for conv in conversations:
            risk_score = 0
            risk_factors = []
            
            if conv.get('emotion') == 'негативная':
                risk_score += 3
                risk_factors.append("Негативная эмоция")
            
            if conv.get('satisfaction_score', 3) <= 2:
                risk_score += 2
                risk_factors.append("Низкая удовлетворенность")
            
            if 'жалоба' in conv.get('theme', ''):
                risk_score += 4
                risk_factors.append("Жалоба")
            
            if 'конкурент' in conv.get('theme', ''):
                risk_score += 3
                risk_factors.append("Упоминание конкурентов")
            
            if risk_score >= 5:
                risks.append({
                    "conversation_id": conv.get('id'),
                    "client_id": conv.get('client_id'),
                    "risk_score": risk_score,
                    "risk_factors": risk_factors,
                    "recommended_action": self._get_recommended_action(risk_score)
                })
        
        return risks

    def _get_recommended_action(self, risk_score: int) -> str:
        """Рекомендуемые действия на основе уровня риска"""
        if risk_score >= 8:
            return "Немедленный контакт менеджера"
        elif risk_score >= 6:
            return "Контакт в течение 24 часов"
        else:
            return "Мониторинг ситуации"

    async def _get_conversations_by_date(self, date: datetime) -> List[Dict]:
        """Получение разговоров за определенную дату"""
        # Здесь должна быть логика получения данных из БД
        # Пока возвращаем заглушку
        return []

def get_analytics_report(query: AnalyticsReportQuery) -> AnalyticsReportResponse:
    # TODO: Реализовать бизнес-логику, сейчас возвращается пример
    return AnalyticsReportResponse(
        group_by=query.group_by,
        period={"start": query.start_date or date.today(), "end": query.end_date or date.today()},
        results=[
            AnalyticsReportItem(theme="ипотека", count=1200, avg_emotion="positive", top_products=["Ипотека 2024", "Рефинансирование"]),
            AnalyticsReportItem(theme="карты", count=950, avg_emotion="neutral", top_products=["Дебетовая карта", "Кредитная карта"])
        ]
    )

def get_statistics_summary(query: StatisticsSummaryQuery) -> StatisticsSummaryResponse:
    # TODO: Реализовать бизнес-логику, сейчас возвращается пример
    return StatisticsSummaryResponse(
        period=query.period,
        total_conversations=12000,
        unique_users=350,
        avg_conversation_length=7.2,
        top_channels=["чат", "звонок"]
    )

analytics_service = BankingAnalyticsService()
