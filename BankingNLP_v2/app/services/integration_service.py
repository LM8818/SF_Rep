import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BankingIntegrationService:
    def __init__(self):
        self.crm_base_url = "https://api.crm.bank.com/v1"
        self.dwh_base_url = "https://api.dwh.bank.com/v1"
        self.notification_url = "https://api.notifications.bank.com/v1"

    async def sync_with_crm(self, conversation_data: Dict[str, Any]) -> bool:
        """Синхронизация данных с CRM системой"""
        try:
            crm_payload = {
                "client_id": conversation_data.get("client_id"),
                "conversation_id": conversation_data.get("conversation_id"),
                "theme": conversation_data.get("theme"),
                "satisfaction_score": conversation_data.get("satisfaction_score"),
                "products_mentioned": conversation_data.get("products", []),
                "emotion": conversation_data.get("emotion"),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "nlp_analysis"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.crm_base_url}/conversations",
                    json=crm_payload,
                    headers={"Authorization": "Bearer CRM_TOKEN"}
                ) as response:
                    if response.status == 200:
                        logger.info(f"Данные синхронизированы с CRM для разговора {conversation_data.get('conversation_id')}")
                        return True
                    else:
                        logger.error(f"Ошибка синхронизации с CRM: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Ошибка при синхронизации с CRM: {e}")
            return False

    async def send_to_dwh(self, analytics_data: Dict[str, Any]) -> bool:
        """Отправка аналитических данных в хранилище данных"""
        try:
            dwh_payload = {
                "report_type": "nlp_analytics",
                "data": analytics_data,
                "generated_at": datetime.utcnow().isoformat(),
                "version": "2.0"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.dwh_base_url}/analytics",
                    json=dwh_payload,
                    headers={"Authorization": "Bearer DWH_TOKEN"}
                ) as response:
                    if response.status == 200:
                        logger.info("Аналитические данные отправлены в DWH")
                        return True
                    else:
                        logger.error(f"Ошибка отправки в DWH: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Ошибка при отправке в DWH: {e}")
            return False

    async def send_risk_alert(self, risk_data: Dict[str, Any]) -> bool:
        """Отправка алерта о рисках"""
        try:
            alert_payload = {
                "alert_type": "customer_risk",
                "severity": risk_data.get("risk_score", 0),
                "client_id": risk_data.get("client_id"),
                "risk_factors": risk_data.get("risk_factors", []),
                "recommended_action": risk_data.get("recommended_action"),
                "created_at": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notification_url}/alerts",
                    json=alert_payload,
                    headers={"Authorization": "Bearer NOTIFICATION_TOKEN"}
                ) as response:
                    if response.status == 200:
                        logger.info(f"Алерт о риске отправлен для клиента {risk_data.get('client_id')}")
                        return True
                    else:
                        logger.error(f"Ошибка отправки алерта: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Ошибка при отправке алерта: {e}")
            return False

    async def get_client_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Получение информации о клиенте из CRM"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.crm_base_url}/clients/{client_id}",
                    headers={"Authorization": "Bearer CRM_TOKEN"}
                ) as response:
                    if response.status == 200:
                        client_data = await response.json()
                        return client_data
                    else:
                        logger.error(f"Ошибка получения данных клиента: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Ошибка при получении данных клиента: {e}")
            return None

    async def send_conversion_opportunity(self, opportunity_data: Dict[str, Any]) -> bool:
        """Отправка информации о возможности конверсии"""
        try:
            opportunity_payload = {
                "opportunity_type": "product_recommendation",
                "client_id": opportunity_data.get("client_id"),
                "recommended_products": opportunity_data.get("recommended_products", []),
                "confidence": opportunity_data.get("confidence", 0.5),
                "reason": opportunity_data.get("reason"),
                "priority": self._calculate_priority(opportunity_data),
                "created_at": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.crm_base_url}/opportunities",
                    json=opportunity_payload,
                    headers={"Authorization": "Bearer CRM_TOKEN"}
                ) as response:
                    if response.status == 200:
                        logger.info(f"Возможность конверсии отправлена для клиента {opportunity_data.get('client_id')}")
                        return True
                    else:
                        logger.error(f"Ошибка отправки возможности конверсии: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Ошибка при отправке возможности конверсии: {e}")
            return False

    def _calculate_priority(self, opportunity_data: Dict[str, Any]) -> str:
        """Расчет приоритета возможности конверсии"""
        confidence = opportunity_data.get("confidence", 0.5)
        
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        else:
            return "low"

integration_service = BankingIntegrationService()
