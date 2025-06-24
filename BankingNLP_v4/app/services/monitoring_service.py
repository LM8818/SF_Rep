import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
from collections import defaultdict, deque
import hashlib
from app.schemas.monitoring import AlertGetQuery, AlertResponse, AlertCreateRequest, AlertItem

logger = logging.getLogger(__name__)

class SecurityMonitoringService:
    def __init__(self):
        self.request_history = defaultdict(deque)
        self.failed_attempts = defaultdict(int)
        self.suspicious_activities = []
        self.rate_limits = {
            'analyze': 100,  # запросов в час
            'batch_analyze': 10,
            'retrain': 1
        }

    async def log_request(self, user_id: str, endpoint: str, request_data: Dict[str, Any]):
        """Логирование запросов для аудита"""
        timestamp = datetime.utcnow()
        
        # Анонимизация чувствительных данных
        sanitized_data = self._sanitize_request_data(request_data)
        
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "user_id": self._hash_user_id(user_id),
            "endpoint": endpoint,
            "data_hash": self._hash_data(sanitized_data),
            "ip_address": request_data.get('client_ip', 'unknown'),
            "user_agent": request_data.get('user_agent', 'unknown')
        }
        
        # Сохранение в защищенный лог
        logger.info(f"AUDIT: {json.dumps(log_entry)}")
        
        # Проверка на подозрительную активность
        await self._check_suspicious_activity(user_id, endpoint, timestamp)

    async def check_rate_limit(self, user_id: str, endpoint: str) -> bool:
        """Проверка лимитов запросов"""
        current_time = datetime.utcnow()
        hour_ago = current_time - timedelta(hours=1)
        
        # Очистка старых записей
        user_requests = self.request_history[user_id]
        while user_requests and user_requests[0] < hour_ago:
            user_requests.popleft()
        
        # Подсчет запросов к конкретному endpoint
        endpoint_requests = sum(1 for req_time, req_endpoint in user_requests 
                               if req_endpoint == endpoint)
        
        limit = self.rate_limits.get(endpoint, 50)
        
        if endpoint_requests >= limit:
            logger.warning(f"Rate limit exceeded for user {self._hash_user_id(user_id)} on {endpoint}")
            return False
        
        # Добавление текущего запроса
        user_requests.append((current_time, endpoint))
        return True

    async def _check_suspicious_activity(self, user_id: str, endpoint: str, timestamp: datetime):
        """Проверка подозрительной активности"""
        # Проверка на аномальную частоту запросов
        recent_requests = [req_time for req_time, _ in self.request_history[user_id] 
                          if timestamp - req_time < timedelta(minutes=5)]
        
        if len(recent_requests) > 50:
            await self._log_suspicious_activity(
                user_id, "Аномально высокая частота запросов", 
                {"requests_in_5min": len(recent_requests)}
            )
        
        # Проверка на попытки доступа к чувствительным endpoint'ам
        sensitive_endpoints = ['retrain', 'admin', 'config']
        if any(sensitive in endpoint for sensitive in sensitive_endpoints):
            await self._log_suspicious_activity(
                user_id, "Попытка доступа к чувствительному endpoint", 
                {"endpoint": endpoint}
            )

    async def _log_suspicious_activity(self, user_id: str, activity_type: str, details: Dict[str, Any]):
        """Логирование подозрительной активности"""
        activity = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": self._hash_user_id(user_id),
            "activity_type": activity_type,
            "details": details,
            "severity": self._calculate_severity(activity_type)
        }
        
        self.suspicious_activities.append(activity)
        logger.warning(f"SECURITY_ALERT: {json.dumps(activity)}")
        
        # Отправка алерта администраторам при высокой степени угрозы
        if activity["severity"] >= 8:
            await self._send_security_alert(activity)

    def _sanitize_request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анонимизация чувствительных данных"""
        sanitized = data.copy()
        
        # Удаление или маскирование чувствительных полей
        sensitive_fields = ['password', 'token', 'email', 'phone', 'account']
        
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = "***MASKED***"
        
        # Ограничение длины текстовых полей для логирования
        if 'text' in sanitized and len(sanitized['text']) > 100:
            sanitized['text'] = sanitized['text'][:100] + "..."
        
        return sanitized

    def _hash_user_id(self, user_id: str) -> str:
        """Хеширование ID пользователя для анонимности"""
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]

    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Хеширование данных запроса"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]

    def _calculate_severity(self, activity_type: str) -> int:
        """Расчет степени серьезности угрозы"""
        severity_map = {
            "Аномально высокая частота запросов": 6,
            "Попытка доступа к чувствительному endpoint": 8,
            "Множественные неудачные попытки авторизации": 7,
            "Подозрительный паттерн запросов": 5
        }
        return severity_map.get(activity_type, 3)

    async def _send_security_alert(self, activity: Dict[str, Any]):
        """Отправка алерта безопасности"""
        # Здесь должна быть логика отправки уведомлений
        logger.critical(f"HIGH_SECURITY_ALERT: {json.dumps(activity)}")

    async def get_security_report(self, hours: int = 24) -> Dict[str, Any]:
        """Получение отчета по безопасности"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        recent_activities = [
            activity for activity in self.suspicious_activities
            if datetime.fromisoformat(activity['timestamp']) > cutoff_time
        ]
        
        return {
            "period_hours": hours,
            "total_suspicious_activities": len(recent_activities),
            "high_severity_count": len([a for a in recent_activities if a['severity'] >= 8]),
            "activities_by_type": self._group_activities_by_type(recent_activities),
            "recommendations": self._generate_security_recommendations(recent_activities)
        }

    def _group_activities_by_type(self, activities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Группировка активностей по типам"""
        grouped = defaultdict(int)
        for activity in activities:
            grouped[activity['activity_type']] += 1
        return dict(grouped)

    def _generate_security_recommendations(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Генерация рекомендаций по безопасности"""
        recommendations = []
        
        if len(activities) > 10:
            recommendations.append("Рассмотрите ужесточение лимитов запросов")
        
        high_severity = [a for a in activities if a['severity'] >= 8]
        if len(high_severity) > 3:
            recommendations.append("Необходима проверка системы безопасности")
        
        return recommendations

def get_alerts(query: AlertGetQuery) -> AlertResponse:
    # TODO: Реализовать получение алертов
    return AlertResponse(alerts=[
        AlertItem(id="1", event="Model degradation", level="critical", timestamp=str(datetime.now()), details={"metric": "accuracy", "value": 0.72}),
        AlertItem(id="2", event="Integration error", level="warning", timestamp=str(datetime.now()), details={"service": "CRM"})
    ])

def create_alert(request: AlertCreateRequest) -> AlertResponse:
    # TODO: Реализовать создание алерта
    return AlertResponse(alerts=[
        AlertItem(id="3", event=request.event, level="info", timestamp=str(datetime.now()), details=request.details)
    ])

monitoring_service = SecurityMonitoringService()
