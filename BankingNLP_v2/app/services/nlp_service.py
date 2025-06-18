import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

from src.data.load_data import load_transcripts, clean_and_normalize
from src.features.build_features import build_features
from src.models.train_model import train_model
from src.evaluation.evaluate import evaluate

logger = logging.getLogger(__name__)

class NLPService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.themes = [
            'информация', 'ипотека', 'жалоба', 'конкурент', 
            'жизненное событие', 'страхование', 'вклад', 'кредит'
        ]
        self.load_model()

    def load_model(self):
        """Загружает обученную модель или обучает новую"""
        try:
            self.model = joblib.load('models/latest_model.joblib')
            self.vectorizer = joblib.load('models/vectorizer.joblib')
            logger.info("Модель успешно загружена")
        except FileNotFoundError:
            logger.warning("Модель не найдена, обучение новой модели")
            self.train_new_model()

    def train_new_model(self):
        """Обучает новую модель NLP"""
        try:
            # Загрузка и подготовка данных
            df = load_transcripts()
            df = clean_and_normalize(df)
            df = build_features(df)
            
            # Обучение модели
            train_model()
            self.load_model()
            logger.info("Новая модель обучена и загружена")
        except Exception as e:
            logger.error(f"Ошибка при обучении модели: {e}")
            raise

    async def analyze_conversation(self, text: str) -> Dict[str, Any]:
        """Анализирует текст разговора и возвращает результаты"""
        try:
            # Предобработка текста
            processed_text = self._preprocess_text(text)
            
            # Извлечение признаков
            features = self._extract_features(processed_text)
            
            # Предсказание темы
            theme_prediction = self.model.predict([features])[0]
            theme_probability = max(self.model.predict_proba([features])[0])
            
            # Анализ эмоций
            emotion = self._analyze_emotion(text)
            
            # Извлечение продуктов
            products = self._extract_products(text)
            
            # Оценка удовлетворенности
            satisfaction = self._estimate_satisfaction(text, emotion)
            
            return {
                "theme": theme_prediction,
                "confidence": float(theme_probability),
                "emotion": emotion,
                "products": products,
                "satisfaction_score": satisfaction,
                "processed_at": datetime.utcnow().isoformat(),
                "text_length": len(text),
                "word_count": len(text.split())
            }
        except Exception as e:
            logger.error(f"Ошибка при анализе разговора: {e}")
            raise

    def _preprocess_text(self, text: str) -> str:
        """Предобработка текста"""
        # Здесь используется логика из clean_and_normalize
        return text.lower().strip()

    def _extract_features(self, text: str) -> List[float]:
        """Извлечение признаков из текста"""
        if self.vectorizer:
            return self.vectorizer.transform([text]).toarray()[0]
        return [len(text), len(text.split())]  # Базовые признаки

    def _analyze_emotion(self, text: str) -> str:
        """Анализ эмоциональной окраски"""
        positive_words = ['хорошо', 'отлично', 'спасибо', 'доволен', 'рад']
        negative_words = ['плохо', 'ужасно', 'жалоба', 'недоволен', 'проблема']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "позитивная"
        elif negative_count > positive_count:
            return "негативная"
        else:
            return "нейтральная"

    def _extract_products(self, text: str) -> List[str]:
        """Извлечение упоминаний банковских продуктов"""
        products = {
            'кредит': ['кредит', 'займ', 'ссуда'],
            'ипотека': ['ипотека', 'жилищный кредит'],
            'карта': ['карта', 'дебетовая', 'кредитная'],
            'вклад': ['вклад', 'депозит', 'накопления'],
            'страхование': ['страховка', 'страхование', 'полис']
        }
        
        found_products = []
        text_lower = text.lower()
        
        for product, keywords in products.items():
            if any(keyword in text_lower for keyword in keywords):
                found_products.append(product)
        
        return found_products

    def _estimate_satisfaction(self, text: str, emotion: str) -> int:
        """Оценка удовлетворенности клиента от 1 до 5"""
        base_score = 3
        
        if emotion == "позитивная":
            base_score += 1
        elif emotion == "негативная":
            base_score -= 1
        
        # Дополнительные факторы
        if 'спасибо' in text.lower():
            base_score += 1
        if any(word in text.lower() for word in ['жалоба', 'недоволен', 'ужасно']):
            base_score -= 1
        
        return max(1, min(5, base_score))

nlp_service = NLPService()
