# Добавьте новые импорты
from ..src.banking_nlp.utils.data_initializer import DataInitializer

# Создайте экземпляр инициализатора
data_initializer = DataInitializer()

@router.get("/data/conversations")
async def get_conversations(limit: int = 100):
    """Получение данных разговоров из CSV"""
    try:
        df = await data_initializer.get_conversations_data(limit=limit)
        
        # Конвертируем в список словарей для JSON ответа
        conversations = df.to_dict('records')
        
        return {
            "status": "success",
            "total_returned": len(conversations),
            "conversations": conversations,
            "message": f"Возвращено {len(conversations)} разговоров"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Ошибка получения данных"
        }

@router.get("/data/info")
async def get_data_info():
    """Получение информации о доступных данных"""
    return await data_initializer.get_data_info()

@router.get("/data/analytics")
async def get_data_analytics():
    """Получение аналитических данных"""
    try:
        df = await data_initializer.get_conversations_data()
        
        analytics = {
            "total_conversations": len(df),
            "themes_distribution": df['theme'].value_counts().to_dict(),
            "products_distribution": df['product'].value_counts().to_dict(),
            "emotions_distribution": df['emotion'].value_counts().to_dict(),
            "average_satisfaction": df['client_satisfaction'].mean(),
            "average_duration": df['duration_minutes'].mean()
        }
        
        return {
            "status": "success",
            "analytics": analytics,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
