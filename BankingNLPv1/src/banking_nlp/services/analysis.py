"""
Сервис анализа банковских разговоров
===================================

Основной сервис для обработки и анализа текстов банковских разговоров.
Включает классификацию тематик, анализ продуктовых упоминаний и эмоциональный анализ.
"""

import logging
import re
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Настройка логгера
logger = logging.getLogger(__name__)


class AnalysisRequest(BaseModel):
    """Модель запроса на анализ"""
    text: str = Field(..., description="Текст для анализа", min_length=1)
    language: str = Field(default="ru", description="Язык текста")
    include_emotions: bool = Field(default=True, description="Включить эмоциональный анализ")
    include_products: bool = Field(default=True, description="Включить анализ продуктов")
    include_themes: bool = Field(default=True, description="Включить анализ тематик")


class AnalysisResult(BaseModel):
    """Модель результата анализа"""
    themes: List[str] = Field(default=[], description="Выявленные тематики")
    products: List[str] = Field(default=[], description="Упомянутые продукты")
    emotions: Dict[str, float] = Field(default={}, description="Эмоциональная окраска")
    confidence: float = Field(default=0.0, description="Уверенность в анализе")
    processing_time: Optional[float] = Field(default=None, description="Время обработки в секундах")
    timestamp: Optional[str] = Field(default=None, description="Время анализа")
    error: Optional[str] = Field(default=None, description="Ошибка анализа")


class AnalysisService:
    """Сервис анализа банковских разговоров"""

    def __init__(self):
        """Инициализация сервиса анализа"""
        self.themes_dict = self._load_themes()
        self.products_dict = self._load_products()
        self.emotion_keywords = self._load_emotion_keywords()
        logger.info("Сервис анализа инициализирован")

    def _load_themes(self) -> Dict[str, List[str]]:
        """Загрузка словаря тематик и ключевых слов"""
        return {
            "кредиты": [
                "кредит", "займ", "ссуда", "кредитная линия", "овердрафт",
                "процентная ставка", "переплата", "долг", "задолженность"
            ],
            "ипотека": [
                "ипотека", "ипотечный", "жилищный кредит", "недвижимость",
                "квартира", "дом", "покупка жилья", "первоначальный взнос"
            ],
            "вклады": [
                "вклад", "депозит", "накопления", "сбережения", "процент по вкладу",
                "капитализация", "пополнение", "срочный вклад"
            ],
            "карты": [
                "карта", "кредитная карта", "дебетовая карта", "пластик",
                "снятие наличных", "лимит", "cashback", "кешбэк"
            ],
            "страхование": [
                "страхование", "страховка", "полис", "страховая премия",
                "страховой случай", "выплата", "КАСКО", "ОСАГО"
            ],
            "инвестиции": [
                "инвестиции", "ИИС", "брокерский счет", "акции", "облигации",
                "паи", "доходность", "портфель", "риски"
            ],
            "жалобы": [
                "жалоба", "недовольство", "проблема", "ошибка", "не работает",
                "плохое обслуживание", "некорректно", "неправильно"
            ],
            "техническая_поддержка": [
                "не работает", "ошибка", "сбой", "технические проблемы",
                "приложение", "интернет-банк", "мобильный банк", "восстановление"
            ]
        }

    def _load_products(self) -> Dict[str, List[str]]:
        """Загрузка словаря банковских продуктов"""
        return {
            "потребительский_кредит": [
                "потребительский кредит", "кредит наличными", "личный кредит",
                "кредит на покупки", "нецелевой кредит"
            ],
            "автокредит": [
                "автокредит", "кредит на машину", "кредит на автомобиль",
                "автомобильный кредит"
            ],
            "кредитная_карта": [
                "кредитная карта", "кредитка", "карта с лимитом"
            ],
            "срочный_вклад": [
                "срочный вклад", "депозит", "сберегательный вклад"
            ],
            "дебетовая_карта": [
                "дебетовая карта", "зарплатная карта", "карта для расчетов"
            ],
            "страхование_жизни": [
                "страхование жизни", "полис жизни", "накопительное страхование"
            ],
            "страхование_имущества": [
                "страхование квартиры", "страхование дома", "имущественное страхование"
            ]
        }

    def _load_emotion_keywords(self) -> Dict[str, List[str]]:
        """Загрузка словаря эмоциональных ключевых слов"""
        return {
            "positive": [
                "отлично", "хорошо", "замечательно", "спасибо", "благодарю",
                "доволен", "рад", "удобно", "быстро", "качественно"
            ],
            "negative": [
                "плохо", "ужасно", "недоволен", "расстроен", "злой",
                "медленно", "некачественно", "проблема", "ошибка", "сбой"
            ],
            "neutral": [
                "хочу узнать", "интересует", "расскажите", "объясните",
                "можно ли", "как получить", "какие условия"
            ]
        }

    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Выполнение анализа текста

        Args:
            request: Запрос на анализ

        Returns:
            AnalysisResult: Результат анализа
        """
        start_time = datetime.now()

        try:
            # Подготовка текста
            text_lower = request.text.lower()

            # Анализ тематик
            themes = []
            if request.include_themes:
                themes = self._analyze_themes(text_lower)

            # Анализ продуктов  
            products = []
            if request.include_products:
                products = self._analyze_products(text_lower)

            # Эмоциональный анализ
            emotions = {}
            if request.include_emotions:
                emotions = self._analyze_emotions(text_lower)

            # Расчет общей уверенности
            confidence = self._calculate_confidence(themes, products, emotions)

            # Время обработки
            processing_time = (datetime.now() - start_time).total_seconds()

            result = AnalysisResult(
                themes=themes,
                products=products,
                emotions=emotions,
                confidence=confidence,
                processing_time=processing_time,
                timestamp=datetime.now().isoformat()
            )

            logger.info(f"Анализ завершен за {processing_time:.3f}с. Уверенность: {confidence:.2f}")
            return result

        except Exception as e:
            logger.error(f"Ошибка анализа: {e}")
            return AnalysisResult(
                error=str(e),
                timestamp=datetime.now().isoformat()
            )

    def _analyze_themes(self, text: str) -> List[str]:
        """Анализ тематик в тексте"""
        found_themes = []

        for theme, keywords in self.themes_dict.items():
            for keyword in keywords:
                if keyword in text:
                    found_themes.append(theme)
                    break  # Найдена тематика, переходим к следующей

        return found_themes

    def _analyze_products(self, text: str) -> List[str]:
        """Анализ упоминаний банковских продуктов"""
        found_products = []

        for product, keywords in self.products_dict.items():
            for keyword in keywords:
                if keyword in text:
                    found_products.append(product)
                    break

        return found_products

    def _analyze_emotions(self, text: str) -> Dict[str, float]:
        """Эмоциональный анализ текста"""
        emotion_scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        word_count = len(text.split())

        if word_count == 0:
            return emotion_scores

        for emotion, keywords in self.emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            emotion_scores[emotion] = matches / word_count

        # Нормализация к сумме 1.0
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
        else:
            emotion_scores = {"positive": 0.33, "negative": 0.33, "neutral": 0.34}

        return emotion_scores

    def _calculate_confidence(self, themes: List[str], products: List[str], emotions: Dict[str, float]) -> float:
        """Расчет общей уверенности в анализе"""
        confidence = 0.0

        # Уверенность от найденных тематик
        if themes:
            confidence += 0.4 * min(len(themes) / 3, 1.0)

        # Уверенность от найденных продуктов
        if products:
            confidence += 0.3 * min(len(products) / 2, 1.0)

        # Уверенность от эмоционального анализа
        if emotions:
            max_emotion_score = max(emotions.values()) if emotions else 0
            confidence += 0.3 * max_emotion_score

        return round(confidence, 3)

    def get_available_themes(self) -> List[str]:
        """Получение списка доступных тематик"""
        return list(self.themes_dict.keys())

    def get_available_products(self) -> List[str]:
        """Получение списка банковских продуктов"""
        return list(self.products_dict.keys())
