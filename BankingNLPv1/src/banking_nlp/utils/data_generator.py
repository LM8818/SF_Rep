# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from faker import Faker

import logging
logger = logging.getLogger(__name__)


class BankingDataGenerator:
    """Генератор реалистичных банковских разговоров"""
    
    def __init__(self, locale: str = 'ru_RU'):
        """Инициализация генератора"""
        self.faker = Faker(locale)
        self.faker.seed_instance(42)  # Для воспроизводимости результатов
        
        # Банковские продукты и их ключевые слова
        self.products = {
            'кредит': {
                'keywords': ['кредит', 'займ', 'ссуда', 'кредитование', 'заем'],
                'subcategories': ['потребительский', 'автокредит', 'рефинансирование']
            },
            'вклад': {
                'keywords': ['вклад', 'депозит', 'накопления', 'сбережения', 'проценты'],
                'subcategories': ['срочный', 'до востребования', 'пенсионный']
            },
            'карта': {
                'keywords': ['карта', 'карточка', 'платежная карта', 'дебетовая', 'кредитная'],
                'subcategories': ['дебетовая', 'кредитная', 'зарплатная']
            },
            'ипотека': {
                'keywords': ['ипотека', 'жилищный кредит', 'недвижимость', 'квартира', 'дом'],
                'subcategories': ['первичное жилье', 'вторичное жилье', 'рефинансирование']
            },
            'страхование': {
                'keywords': ['страховка', 'страхование', 'полис', 'КАСКО', 'ОСАГО'],
                'subcategories': ['автострахование', 'жизнь', 'имущество']
            },
            'инвестиции': {
                'keywords': ['инвестиции', 'ИИС', 'брокерский счет', 'ценные бумаги'],
                'subcategories': ['ИИС', 'брокерский счет', 'ПИФ']
            }
        }
        
        # Тематики разговоров с шаблонами
        self.themes = {
            'продажи': {
                'templates': [
                    'Клиент: Здравствуйте, меня интересует {product}. Можете рассказать подробнее?\nОператор: Конечно! С удовольствием расскажу о наших условиях по {product}.',
                    'Клиент: Хочу оформить {product}. Какие у вас условия?\nОператор: Отличный выбор! Расскажу вам о наших предложениях.',
                    'Клиент: Слышал про ваш {product}. Интересно узнать больше.\nОператор: Да, это один из наших популярных продуктов.'
                ],
                'emotion_weight': 0.7
            },
            'поддержка': {
                'templates': [
                    'Клиент: У меня проблема с {product}. Не могу воспользоваться.\nОператор: Давайте разберемся с вашей проблемой.',
                    'Клиент: Не работает {product}. Что делать?\nОператор: Сейчас поможем решить этот вопрос.',
                    'Клиент: Возникли трудности с {product}.\nОператор: Понимаю вашу ситуацию, поможем разобраться.'
                ],
                'emotion_weight': 0.3
            },
            'жалобы': {
                'templates': [
                    'Клиент: Я недоволен обслуживанием по {product}.\nОператор: Приносим извинения, поможем решить вопрос.',
                    'Клиент: Плохо работает {product}. Хочу пожаловаться.\nОператор: Принимаем вашу жалобу, разберемся.',
                    'Клиент: Не устраивают условия {product}.\nОператор: Давайте найдем решение вместе.'
                ],
                'emotion_weight': 0.1
            },
            'информация': {
                'templates': [
                    'Клиент: Расскажите, как работает {product}?\nОператор: Объясню все детали нашего {product}.',
                    'Клиент: Какие условия по {product}?\nОператор: С удовольствием расскажу об условиях.',
                    'Клиент: Хочу узнать больше про {product}.\nОператор: Конечно, объясню все подробно.'
                ],
                'emotion_weight': 0.5
            },
            'техподдержка': {
                'templates': [
                    'Клиент: Не могу войти в мобильное приложение.\nОператор: Поможем восстановить доступ.',
                    'Клиент: Заблокирована карта, как разблокировать?\nОператор: Сейчас проверим и разблокируем.',
                    'Клиент: Не приходят SMS с кодами.\nОператор: Проверим настройки SMS-уведомлений.'
                ],
                'emotion_weight': 0.4
            }
        }
        
        # Конкуренты для реалистичности
        self.competitors = [
            'Сбербанк', 'ВТБ', 'Газпромбанк', 'Альфа-Банк', 'Тинькофф',
            'Россельхозбанк', 'Банк Открытие', 'Промсвязьбанк'
        ]
        
    def generate_conversation(self, conv_id: int) -> Dict[str, Any]:
        """Генерирует один банковский разговор"""
        
        # Выбираем случайную тематику и продукт
        theme = random.choice(list(self.themes.keys()))
        product_category = random.choice(list(self.products.keys()))
        product_info = self.products[product_category]
        
        # Создаем текст разговора
        conversation_text = self._create_conversation_text(theme, product_category)
        
        # Определяем эмоциональную окраску
        emotion = self._analyze_emotion(conversation_text, theme)
        
        # Генерируем дополнительные поля
        client_id = f"client_{random.randint(10000, 99999)}"
        agent_id = f"agent_{random.randint(100, 999)}"
        
        return {
            'conversation_id': conv_id,
            'client_id': client_id,
            'agent_id': agent_id,
            'timestamp': self._random_timestamp(),
            'conversation_text': conversation_text,
            'theme': theme,
            'product': product_category,
            'product_keywords': ', '.join(product_info['keywords'][:3]),
            'emotion': emotion,
            'client_satisfaction': self._generate_satisfaction_score(emotion),
            'duration_minutes': random.randint(2, 45),
            'call_result': self._determine_call_result(theme),
            'follow_up_required': random.choice([True, False]),
            'region': self._random_region(),
            'channel': random.choice(['телефон', 'чат', 'email', 'офис'])
        }
    
    def _create_conversation_text(self, theme: str, product: str) -> str:
        """Создает реалистичный текст разговора"""
        template = random.choice(self.themes[theme]['templates'])
        conversation = template.format(product=product)
        
        # Добавляем дополнительные реплики для реалистичности
        additional_phrases = self._get_additional_phrases(theme, product)
        if additional_phrases:
            conversation += f"\n{additional_phrases}"
            
        return conversation
    
    def _get_additional_phrases(self, theme: str, product: str) -> str:
        """Генерирует дополнительные фразы для разговора"""
        additional = []
        
        if theme == 'продажи':
            additional.extend([
                f"Клиент: А какие проценты по {product}?",
                "Оператор: Процентная ставка зависит от суммы и срока.",
                "Клиент: Спасибо за информацию, подумаю."
            ])
        elif theme == 'поддержка':
            additional.extend([
                "Клиент: Когда это можно будет исправить?",
                "Оператор: Постараемся решить в течение дня.",
                "Клиент: Хорошо, буду ждать."
            ])
        elif theme == 'жалобы':
            additional.extend([
                "Клиент: Это уже не первый раз!",
                "Оператор: Понимаем ваше недовольство, примем меры.",
                "Клиент: Надеюсь, что ситуация изменится."
            ])
            
        return '\n'.join(additional) if additional else ""
    
    def _analyze_emotion(self, text: str, theme: str) -> str:
        """Анализ эмоций на основе тематики и ключевых слов"""
        text_lower = text.lower()
        
        # Позитивные и негативные маркеры
        positive_words = ['спасибо', 'отлично', 'хорошо', 'интересует', 'понравилось', 'удобно']
        negative_words = ['проблема', 'недоволен', 'плохо', 'жалуюсь', 'не работает', 'ошибка']
        
        # Базовая эмоция по тематике
        emotion_base = self.themes[theme]['emotion_weight']
        
        # Корректировка по ключевым словам
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count > positive_count:
            return 'негативная'
        elif positive_count > negative_count:
            return 'позитивная'
        else:
            # Используем вероятность на основе тематики
            return 'позитивная' if random.random() < emotion_base else 'негативная'
    
    def _generate_satisfaction_score(self, emotion: str) -> float:
        """Генерирует оценку удовлетворенности клиента"""
        if emotion == 'позитивная':
            return round(random.uniform(3.5, 5.0), 1)
        elif emotion == 'негативная':
            return round(random.uniform(1.0, 2.5), 1)
        else:
            return round(random.uniform(2.5, 3.5), 1)
    
    def _determine_call_result(self, theme: str) -> str:
        """Определяет результат звонка"""
        results_by_theme = {
            'продажи': ['заявка оформлена', 'требуется консультация', 'отказ', 'перезвонить позже'],
            'поддержка': ['проблема решена', 'эскалация', 'требуется время', 'дополнительная информация'],
            'жалобы': ['жалоба рассмотрена', 'компенсация', 'эскалация', 'повторный контакт'],
            'информация': ['информация предоставлена', 'отправлены документы', 'консультация завершена'],
            'техподдержка': ['проблема решена', 'тикет создан', 'инструкции отправлены', 'требуется визит']
        }
        
        return random.choice(results_by_theme.get(theme, ['обработано']))
    
    def _random_region(self) -> str:
        """Генерирует случайный регион"""
        regions = [
            'Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск',
            'Казань', 'Ростов-на-Дону', 'Краснодар', 'Воронеж', 'Самара'
        ]
        return random.choice(regions)
    
    def _random_timestamp(self) -> str:
        """Генерирует случайную временную метку за последние 30 дней"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Генерируем время в рабочие часы (9:00-18:00)
        random_date = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(9, 17),
            minutes=random.randint(0, 59)
        )
        
        return random_date.strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_csv_files(self, num_conversations: int = 1000) -> None:
        """Генерирует CSV файлы с банковскими разговорами"""
        
        logger.info("🏦 Banking NLP System - Генератор CSV данных")
        logger.info("🚀 Начинаем генерацию {num_conversations} разговоров...")
        
        # Создаем необходимые директории
        self._create_directories()
        
        # Генерируем данные
        conversations = []
        
        for i in range(num_conversations):
            conversation = self.generate_conversation(i + 1)
            conversations.append(conversation)
            
            # Показываем прогресс каждые 100 записей
            if (i + 1) % 100 == 0:
                logger.info("   Сгенерировано: {i + 1}/{num_conversations}")
        
        # Создаем DataFrame
        df = pd.DataFrame(conversations)
        
        # Сохраняем в различных форматах
        self._save_to_csv(df, conversations)
        
        logger.info("✅ Генерация завершена! Создано записей: {num_conversations}")
        logger.info("📁 Файлы сохранены в директории: data/")
        
        # Показываем статистику
        self._print_statistics(df)
    
    def _create_directories(self) -> None:
        """Создает необходимые директории для данных"""
        directories = ['data', 'data/raw', 'data/processed', 'logs']
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info("✅ Создана директория: {directory}")
    
    def _save_to_csv(self, df: pd.DataFrame, conversations: List[Dict]) -> None:
        """Сохраняет данные в CSV файлы"""
        
        # Основной файл с обработанными данными
        processed_file = 'data/processed/conversations_processed.csv'
        df.to_csv(processed_file, index=False, encoding='utf-8-sig')
        logger.info("💾 Сохранен файл: {processed_file}")
        
        # Сырые данные с временной меткой
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_file = f'data/raw/conversations_raw_{timestamp}.csv'
        df.to_csv(raw_file, index=False, encoding='utf-8-sig')
        logger.info("💾 Сохранен файл: {raw_file}")
        
        # Аналитический файл с агрегированными данными
        analytics_df = self._create_analytics(df)
        analytics_file = 'data/processed/conversation_analytics.csv'
        analytics_df.to_csv(analytics_file, index=False, encoding='utf-8-sig')
        logger.info("📊 Сохранен аналитический файл: {analytics_file}")
        
        # Сводка по тематикам
        themes_summary = df.groupby(['theme', 'product']).agg({
            'conversation_id': 'count',
            'client_satisfaction': 'mean',
            'duration_minutes': 'mean'
        }).round(2).reset_index()
        themes_summary.columns = ['theme', 'product', 'count', 'avg_satisfaction', 'avg_duration']
        
        themes_file = 'data/processed/themes_summary.csv'
        themes_summary.to_csv(themes_file, index=False, encoding='utf-8-sig')
        logger.info("📋 Сохранена сводка тематик: {themes_file}")
    
    def _create_analytics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Создает аналитические данные"""
        analytics = {
            'metric': [
                'total_conversations', 'avg_duration', 'avg_satisfaction', 
                'positive_emotions', 'negative_emotions',
                'themes_count', 'products_count', 'unique_clients'
            ],
            'value': [
                len(df),
                round(df['duration_minutes'].mean(), 2),
                round(df['client_satisfaction'].mean(), 2),
                len(df[df['emotion'] == 'позитивная']),
                len(df[df['emotion'] == 'негативная']),
                df['theme'].nunique(),
                df['product'].nunique(),
                df['client_id'].nunique()
            ]
        }
        
        return pd.DataFrame(analytics)
    
    def _print_statistics(self, df: pd.DataFrame) -> None:
        """Выводит статистику сгенерированных данных"""
        logger.info("\n📊 Статистика сгенерированных данных:")
        logger.info("-" * 40)
        logger.info("Всего разговоров: {len(df)}")
        logger.info("Уникальных клиентов: {df['client_id'].nunique()}")
        logger.info("Тематик: {df['theme'].nunique()}")
        logger.info("Продуктов: {df['product'].nunique()}")
        logger.info("Средняя продолжительность: {df['duration_minutes'].mean():.1f} мин")
        logger.info("Средняя удовлетворенность: {df['client_satisfaction'].mean():.1f}/5.0")
        
        logger.info("\nРаспределение по тематикам:")
        theme_counts = df['theme'].value_counts()
        for theme, count in theme_counts.items():
            logger.info("  {theme}: {count} ({count/len(df)*100:.1f}%)")
        
        logger.info("\nРаспределение эмоций:")
        emotion_counts = df['emotion'].value_counts()
        for emotion, count in emotion_counts.items():
            logger.info("  {emotion}: {count} ({count/len(df)*100:.1f}%)")


def main():
    """Основная функция запуска генератора"""
    generator = BankingDataGenerator()
    
    # Генерируем 1000 разговоров (можно изменить количество)
    generator.generate_csv_files(num_conversations=1000)
    
    logger.info("\n🎯 Генерация завершена успешно!")
    logger.info("📁 Проверьте директорию data/ для просмотра созданных файлов")
    logger.info("🔗 Файлы готовы для использования в Banking NLP System")


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from faker import Faker


class BankingDataGenerator:
    """Генератор реалистичных банковских разговоров"""
    
    def __init__(self, locale: str = 'ru_RU'):
        """Инициализация генератора"""
        self.faker = Faker(locale)
        self.faker.seed_instance(42)  # Для воспроизводимости результатов
        
        # Банковские продукты и их ключевые слова
        self.products = {
            'кредит': {
                'keywords': ['кредит', 'займ', 'ссуда', 'кредитование', 'заем'],
                'subcategories': ['потребительский', 'автокредит', 'рефинансирование']
            },
            'вклад': {
                'keywords': ['вклад', 'депозит', 'накопления', 'сбережения', 'проценты'],
                'subcategories': ['срочный', 'до востребования', 'пенсионный']
            },
            'карта': {
                'keywords': ['карта', 'карточка', 'платежная карта', 'дебетовая', 'кредитная'],
                'subcategories': ['дебетовая', 'кредитная', 'зарплатная']
            },
            'ипотека': {
                'keywords': ['ипотека', 'жилищный кредит', 'недвижимость', 'квартира', 'дом'],
                'subcategories': ['первичное жилье', 'вторичное жилье', 'рефинансирование']
            },
            'страхование': {
                'keywords': ['страховка', 'страхование', 'полис', 'КАСКО', 'ОСАГО'],
                'subcategories': ['автострахование', 'жизнь', 'имущество']
            },
            'инвестиции': {
                'keywords': ['инвестиции', 'ИИС', 'брокерский счет', 'ценные бумаги'],
                'subcategories': ['ИИС', 'брокерский счет', 'ПИФ']
            }
        }
        
        # Тематики разговоров с шаблонами
        self.themes = {
            'продажи': {
                'templates': [
                    'Клиент: Здравствуйте, меня интересует {product}. Можете рассказать подробнее?\nОператор: Конечно! С удовольствием расскажу о наших условиях по {product}.',
                    'Клиент: Хочу оформить {product}. Какие у вас условия?\nОператор: Отличный выбор! Расскажу вам о наших предложениях.',
                    'Клиент: Слышал про ваш {product}. Интересно узнать больше.\nОператор: Да, это один из наших популярных продуктов.'
                ],
                'emotion_weight': 0.7
            },
            'поддержка': {
                'templates': [
                    'Клиент: У меня проблема с {product}. Не могу воспользоваться.\nОператор: Давайте разберемся с вашей проблемой.',
                    'Клиент: Не работает {product}. Что делать?\nОператор: Сейчас поможем решить этот вопрос.',
                    'Клиент: Возникли трудности с {product}.\nОператор: Понимаю вашу ситуацию, поможем разобраться.'
                ],
                'emotion_weight': 0.3
            },
            'жалобы': {
                'templates': [
                    'Клиент: Я недоволен обслуживанием по {product}.\nОператор: Приносим извинения, поможем решить вопрос.',
                    'Клиент: Плохо работает {product}. Хочу пожаловаться.\nОператор: Принимаем вашу жалобу, разберемся.',
                    'Клиент: Не устраивают условия {product}.\nОператор: Давайте найдем решение вместе.'
                ],
                'emotion_weight': 0.1
            },
            'информация': {
                'templates': [
                    'Клиент: Расскажите, как работает {product}?\nОператор: Объясню все детали нашего {product}.',
                    'Клиент: Какие условия по {product}?\nОператор: С удовольствием расскажу об условиях.',
                    'Клиент: Хочу узнать больше про {product}.\nОператор: Конечно, объясню все подробно.'
                ],
                'emotion_weight': 0.5
            },
            'техподдержка': {
                'templates': [
                    'Клиент: Не могу войти в мобильное приложение.\nОператор: Поможем восстановить доступ.',
                    'Клиент: Заблокирована карта, как разблокировать?\nОператор: Сейчас проверим и разблокируем.',
                    'Клиент: Не приходят SMS с кодами.\nОператор: Проверим настройки SMS-уведомлений.'
                ],
                'emotion_weight': 0.4
            }
        }
        
        # Конкуренты для реалистичности
        self.competitors = [
            'Сбербанк', 'ВТБ', 'Газпромбанк', 'Альфа-Банк', 'Тинькофф',
            'Россельхозбанк', 'Банк Открытие', 'Промсвязьбанк'
        ]
        
    def generate_conversation(self, conv_id: int) -> Dict[str, Any]:
        """Генерирует один банковский разговор"""
        
        # Выбираем случайную тематику и продукт
        theme = random.choice(list(self.themes.keys()))
        product_category = random.choice(list(self.products.keys()))
        product_info = self.products[product_category]
        
        # Создаем текст разговора
        conversation_text = self._create_conversation_text(theme, product_category)
        
        # Определяем эмоциональную окраску
        emotion = self._analyze_emotion(conversation_text, theme)
        
        # Генерируем дополнительные поля
        client_id = f"client_{random.randint(10000, 99999)}"
        agent_id = f"agent_{random.randint(100, 999)}"
        
        return {
            'conversation_id': conv_id,
            'client_id': client_id,
            'agent_id': agent_id,
            'timestamp': self._random_timestamp(),
            'conversation_text': conversation_text,
            'theme': theme,
            'product': product_category,
            'product_keywords': ', '.join(product_info['keywords'][:3]),
            'emotion': emotion,
            'client_satisfaction': self._generate_satisfaction_score(emotion),
            'duration_minutes': random.randint(2, 45),
            'call_result': self._determine_call_result(theme),
            'follow_up_required': random.choice([True, False]),
            'region': self._random_region(),
            'channel': random.choice(['телефон', 'чат', 'email', 'офис'])
        }
    
    def _create_conversation_text(self, theme: str, product: str) -> str:
        """Создает реалистичный текст разговора"""
        template = random.choice(self.themes[theme]['templates'])
        conversation = template.format(product=product)
        
        # Добавляем дополнительные реплики для реалистичности
        additional_phrases = self._get_additional_phrases(theme, product)
        if additional_phrases:
            conversation += f"\n{additional_phrases}"
            
        return conversation
    
    def _get_additional_phrases(self, theme: str, product: str) -> str:
        """Генерирует дополнительные фразы для разговора"""
        additional = []
        
        if theme == 'продажи':
            additional.extend([
                f"Клиент: А какие проценты по {product}?",
                "Оператор: Процентная ставка зависит от суммы и срока.",
                "Клиент: Спасибо за информацию, подумаю."
            ])
        elif theme == 'поддержка':
            additional.extend([
                "Клиент: Когда это можно будет исправить?",
                "Оператор: Постараемся решить в течение дня.",
                "Клиент: Хорошо, буду ждать."
            ])
        elif theme == 'жалобы':
            additional.extend([
                "Клиент: Это уже не первый раз!",
                "Оператор: Понимаем ваше недовольство, примем меры.",
                "Клиент: Надеюсь, что ситуация изменится."
            ])
            
        return '\n'.join(additional) if additional else ""
    
    def _analyze_emotion(self, text: str, theme: str) -> str:
        """Анализ эмоций на основе тематики и ключевых слов"""
        text_lower = text.lower()
        
        # Позитивные и негативные маркеры
        positive_words = ['спасибо', 'отлично', 'хорошо', 'интересует', 'понравилось', 'удобно']
        negative_words = ['проблема', 'недоволен', 'плохо', 'жалуюсь', 'не работает', 'ошибка']
        
        # Базовая эмоция по тематике
        emotion_base = self.themes[theme]['emotion_weight']
        
        # Корректировка по ключевым словам
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count > positive_count:
            return 'негативная'
        elif positive_count > negative_count:
            return 'позитивная'
        else:
            # Используем вероятность на основе тематики
            return 'позитивная' if random.random() < emotion_base else 'негативная'
    
    def _generate_satisfaction_score(self, emotion: str) -> float:
        """Генерирует оценку удовлетворенности клиента"""
        if emotion == 'позитивная':
            return round(random.uniform(3.5, 5.0), 1)
        elif emotion == 'негативная':
            return round(random.uniform(1.0, 2.5), 1)
        else:
            return round(random.uniform(2.5, 3.5), 1)
    
    def _determine_call_result(self, theme: str) -> str:
        """Определяет результат звонка"""
        results_by_theme = {
            'продажи': ['заявка оформлена', 'требуется консультация', 'отказ', 'перезвонить позже'],
            'поддержка': ['проблема решена', 'эскалация', 'требуется время', 'дополнительная информация'],
            'жалобы': ['жалоба рассмотрена', 'компенсация', 'эскалация', 'повторный контакт'],
            'информация': ['информация предоставлена', 'отправлены документы', 'консультация завершена'],
            'техподдержка': ['проблема решена', 'тикет создан', 'инструкции отправлены', 'требуется визит']
        }
        
        return random.choice(results_by_theme.get(theme, ['обработано']))
    
    def _random_region(self) -> str:
        """Генерирует случайный регион"""
        regions = [
            'Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск',
            'Казань', 'Ростов-на-Дону', 'Краснодар', 'Воронеж', 'Самара'
        ]
        return random.choice(regions)
    
    def _random_timestamp(self) -> str:
        """Генерирует случайную временную метку за последние 30 дней"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Генерируем время в рабочие часы (9:00-18:00)
        random_date = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(9, 17),
            minutes=random.randint(0, 59)
        )
        
        return random_date.strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_csv_files(self, num_conversations: int = 1000) -> None:
        """Генерирует CSV файлы с банковскими разговорами"""
        
        logger.info("🏦 Banking NLP System - Генератор CSV данных")
        logger.info("🚀 Начинаем генерацию {num_conversations} разговоров...")
        
        # Создаем необходимые директории
        self._create_directories()
        
        # Генерируем данные
        conversations = []
        
        for i in range(num_conversations):
            conversation = self.generate_conversation(i + 1)
            conversations.append(conversation)
            
            # Показываем прогресс каждые 100 записей
            if (i + 1) % 100 == 0:
                logger.info("   Сгенерировано: {i + 1}/{num_conversations}")
        
        # Создаем DataFrame
        df = pd.DataFrame(conversations)
        
        # Сохраняем в различных форматах
        self._save_to_csv(df, conversations)
        
        logger.info("✅ Генерация завершена! Создано записей: {num_conversations}")
        logger.info("📁 Файлы сохранены в директории: data/")
        
        # Показываем статистику
        self._print_statistics(df)
    
    def _create_directories(self) -> None:
        """Создает необходимые директории для данных"""
        directories = ['data', 'data/raw', 'data/processed', 'logs']
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info("✅ Создана директория: {directory}")
    
    def _save_to_csv(self, df: pd.DataFrame, conversations: List[Dict]) -> None:
        """Сохраняет данные в CSV файлы"""
        
        # Основной файл с обработанными данными
        processed_file = 'data/processed/conversations_processed.csv'
        df.to_csv(processed_file, index=False, encoding='utf-8-sig')
        logger.info("💾 Сохранен файл: {processed_file}")
        
        # Сырые данные с временной меткой
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_file = f'data/raw/conversations_raw_{timestamp}.csv'
        df.to_csv(raw_file, index=False, encoding='utf-8-sig')
        logger.info("💾 Сохранен файл: {raw_file}")
        
        # Аналитический файл с агрегированными данными
        analytics_df = self._create_analytics(df)
        analytics_file = 'data/processed/conversation_analytics.csv'
        analytics_df.to_csv(analytics_file, index=False, encoding='utf-8-sig')
        logger.info("📊 Сохранен аналитический файл: {analytics_file}")
        
        # Сводка по тематикам
        themes_summary = df.groupby(['theme', 'product']).agg({
            'conversation_id': 'count',
            'client_satisfaction': 'mean',
            'duration_minutes': 'mean'
        }).round(2).reset_index()
        themes_summary.columns = ['theme', 'product', 'count', 'avg_satisfaction', 'avg_duration']
        
        themes_file = 'data/processed/themes_summary.csv'
        themes_summary.to_csv(themes_file, index=False, encoding='utf-8-sig')
        logger.info("📋 Сохранена сводка тематик: {themes_file}")
    
    def _create_analytics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Создает аналитические данные"""
        analytics = {
            'metric': [
                'total_conversations', 'avg_duration', 'avg_satisfaction', 
                'positive_emotions', 'negative_emotions',
                'themes_count', 'products_count', 'unique_clients'
            ],
            'value': [
                len(df),
                round(df['duration_minutes'].mean(), 2),
                round(df['client_satisfaction'].mean(), 2),
                len(df[df['emotion'] == 'позитивная']),
                len(df[df['emotion'] == 'негативная']),
                df['theme'].nunique(),
                df['product'].nunique(),
                df['client_id'].nunique()
            ]
        }
        
        return pd.DataFrame(analytics)
    
    def _print_statistics(self, df: pd.DataFrame) -> None:
        """Выводит статистику сгенерированных данных"""
        logger.info("\n📊 Статистика сгенерированных данных:")
        logger.info("-" * 40)
        logger.info("Всего разговоров: {len(df)}")
        logger.info("Уникальных клиентов: {df['client_id'].nunique()}")
        logger.info("Тематик: {df['theme'].nunique()}")
        logger.info("Продуктов: {df['product'].nunique()}")
        logger.info("Средняя продолжительность: {df['duration_minutes'].mean():.1f} мин")
        logger.info("Средняя удовлетворенность: {df['client_satisfaction'].mean():.1f}/5.0")
        
        logger.info("\nРаспределение по тематикам:")
        theme_counts = df['theme'].value_counts()
        for theme, count in theme_counts.items():
            logger.info("  {theme}: {count} ({count/len(df)*100:.1f}%)")
        
        logger.info("\nРаспределение эмоций:")
        emotion_counts = df['emotion'].value_counts()
        for emotion, count in emotion_counts.items():
            logger.info("  {emotion}: {count} ({count/len(df)*100:.1f}%)")


def main():
    """Основная функция запуска генератора"""
    generator = BankingDataGenerator()
    
    # Генерируем 1000 разговоров (можно изменить количество)
    generator.generate_csv_files(num_conversations=1000)
    
    logger.info("\n🎯 Генерация завершена успешно!")
    logger.info("📁 Проверьте директорию data/ для просмотра созданных файлов")
    logger.info("🔗 Файлы готовы для использования в Banking NLP System")


if __name__ == "__main__":
    main()
