"""
Сервис для классификации текста с использованием малой LLM Phi-2.
"""

import logging
from typing import Dict, Any, List
from llama_cpp import Llama
import os

logger = logging.getLogger(__name__)

class PhiClassificationService:
    """
    Сервис для классификации банковских текстов с использованием Phi-2.
    """
    
    def __init__(self, model_path: str = "./models/phi-2.gguf"):
        """
        Инициализация сервиса с моделью Phi-2.
        
        Args:
            model_path: Путь к квантизированной модели в формате GGUF
        """
        self.model_path = model_path
        self.model = None
        self.themes = [
            'информация', 'ипотека', 'жалоба', 'конкурент', 
            'жизненное событие', 'страхование', 'вклад', 'кредит'
        ]
        
        # Загрузка модели при инициализации
        self._load_model()
    
    def _load_model(self):
        """Загружает модель Phi-2."""
        try:
            logger.info(f"Загрузка модели из {self.model_path}")
            
            # Загрузка модели с оптимальными параметрами для классификации
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=512,        # Размер контекста
                n_threads=4,      # Количество потоков
                n_gpu_layers=0    # Для CPU-only режима
            )
            
            logger.info("Модель Phi-2 успешно загружена")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели Phi-2: {e}")
            raise
    
    async def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Классифицирует текст на тематики с помощью Phi-2.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь с результатами классификации
        """
        try:
            # Формирование промпта для классификации
            prompt = self._create_classification_prompt(text)
            
            # Получение ответа от модели
            response = self.model(
                prompt, 
                max_tokens=50,
                temperature=0.1,  # Низкая температура для детерминированных ответов
                stop=["
