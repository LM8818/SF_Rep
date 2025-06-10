"""
Сервис мониторинга здоровья системы
=================================

Обеспечивает проверку работоспособности всех компонентов системы
и сбор статистики производительности.
"""

import logging
import psutil
import asyncio
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SystemMetrics(BaseModel):
    """Метрики системы"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: float
    timestamp: str


class HealthService:
    """Сервис мониторинга здоровья системы"""

    def __init__(self):
        """Инициализация сервиса"""
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        logger.info("Сервис здоровья системы инициализирован")

    async def check_health(self) -> Dict[str, Any]:
        """
        Проверка здоровья всех компонентов системы

        Returns:
            Dict: Статус здоровья системы
        """
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "components": {}
            }

            # Проверка основных компонентов
            health_status["components"]["api"] = await self._check_api_health()
            health_status["components"]["memory"] = await self._check_memory_health()
            health_status["components"]["disk"] = await self._check_disk_health()

            # Определение общего статуса
            component_statuses = [comp["status"] for comp in health_status["components"].values()]
            if "unhealthy" in component_statuses:
                health_status["status"] = "unhealthy"
            elif "degraded" in component_statuses:
                health_status["status"] = "degraded"

            return health_status

        except Exception as e:
            logger.error(f"Ошибка проверки здоровья: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _check_api_health(self) -> Dict[str, Any]:
        """Проверка здоровья API"""
        try:
            return {
                "status": "healthy",
                "request_count": self.request_count,
                "error_count": self.error_count,
                "error_rate": self.error_count / max(self.request_count, 1)
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_memory_health(self) -> Dict[str, Any]:
        """Проверка использования памяти"""
        try:
            memory = psutil.virtual_memory()
            status = "healthy"

            if memory.percent > 90:
                status = "unhealthy"
            elif memory.percent > 80:
                status = "degraded"

            return {
                "status": status,
                "percent_used": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2),
                "total_gb": round(memory.total / (1024**3), 2)
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_disk_health(self) -> Dict[str, Any]:
        """Проверка дискового пространства"""
        try:
            disk = psutil.disk_usage('/')
            status = "healthy"

            if disk.percent > 95:
                status = "unhealthy"
            elif disk.percent > 85:
                status = "degraded"

            return {
                "status": status,
                "percent_used": disk.percent,
                "free_gb": round(disk.free / (1024**3), 2),
                "total_gb": round(disk.total / (1024**3), 2)
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def get_system_statistics(self) -> Dict[str, Any]:
        """
        Получение детальной статистики системы

        Returns:
            Dict: Статистика работы системы
        """
        try:
            stats = {
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "requests": {
                    "total": self.request_count,
                    "errors": self.error_count,
                    "success_rate": 1 - (self.error_count / max(self.request_count, 1))
                },
                "system": {
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "memory": {
                        "percent": psutil.virtual_memory().percent,
                        "available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
                    },
                    "disk": {
                        "percent": psutil.disk_usage('/').percent,
                        "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
                    }
                }
            }

            return stats

        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def increment_request_count(self):
        """Увеличение счетчика запросов"""
        self.request_count += 1

    def increment_error_count(self):
        """Увеличение счетчика ошибок"""
        self.error_count += 1
