"""
Модуль для предобработки текстовых данных в банковской сфере
"""
import re
import unicodedata
from typing import List, Dict, Any, Optional
import logging

from utils.config import config
from utils.logging import get_logger

logger = get_logger(__name__)

class BankingTextPreprocessor:
    """
    Класс для предобработки текстов банковской тематики
    """
    
    def __init__(self, config_params: Optional[Dict[str, Any]] = None):
        """
        Инициализация препроцессора с параметрами из конфигурации
        
        Args:
            config_params: Параметры конфигурации (если None, берутся из глобальной конфигурации)
        """
        self.config = config_params or config.get('preprocessing', {})
        self.min_text_length = self.config.get('min_text_length', 10)
        self.max_text_length = self.config.get('max_text_length', 2048)
        
        # Регулярные выражения для очистки текста
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
        self.phone_pattern = re.compile(r'(\+7|8)[- ]?(\(?\d{3}\)?)[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})')
        self.card_number_pattern = re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b')
        self.account_number_pattern = re.compile(r'\b\d{20}\b')
        self.whitespace_pattern = re.compile(r'\s+')
        
        # Словарь для нормализации банковских терминов
        self.banking_terms = {
            'кредитка': 'кредитная карта',
            'дебетка': 'дебетовая карта',
            'ипотека': 'ипотечный кредит',
            'автокредит': 'автомобильный кредит',
            'овердрафт': 'превышение кредитного лимита',
            'депозит': 'вклад',
            'процент': 'процентная ставка',
            'наличка': 'наличные деньги',
            'карта': 'банковская карта',
            'счёт': 'банковский счет',
            'счет': 'банковский счет'
        }
        
        logger.info(f"Инициализирован препроцессор текста с параметрами: {self.config}")
    
    def preprocess(self, text: str) -> str:
        """
        Полная предобработка текста
        
        Args:
            text: Исходный текст
        
        Returns:
            Предобработанный текст
        """
        if not text or not isinstance(text, str):
            logger.warning(f"Получен некорректный текст для обработки: {type(text)}")
            return ""
        
        # Базовая очистка
        text = self._basic_clean(text)
        
        # Анонимизация конфиденциальных данных
        text = self._anonymize_sensitive_data(text)
        
        # Нормализация банковских терминов
        text = self._normalize_banking_terms(text)
        
        # Проверка длины текста
        if len(text) < self.min_text_length:
            logger.debug(f"Текст слишком короткий: {len(text)} символов")
            return ""
        
        if len(text) > self.max_text_length:
            logger.debug(f"Текст слишком длинный: {len(text)} символов, обрезаем до {self.max_text_length}")
            text = text[:self.max_text_length]
        
        return text
    
    def _basic_clean(self, text: str) -> str:
        """
        Базовая очистка текста
        
        Args:
            text: Исходный текст
        
        Returns:
            Очищенный текст
        """
        # Приведение к нижнему регистру
        text = text.lower()
        
        # Нормализация Unicode
        text = unicodedata.normalize('NFKC', text)
        
        # Удаление URL
        if self.config.get('remove_urls', True):
            text = self.url_pattern.sub(' [URL] ', text)
        
        # Удаление email
        if self.config.get('remove_emails', True):
            text = self.email_pattern.sub(' [EMAIL] ', text)
        
        # Удаление телефонов
        if self.config.get('remove_phones', True):
            text = self.phone_pattern.sub(' [ТЕЛЕФОН] ', text)
        
        # Нормализация пробелов
        if self.config.get('normalize_whitespace', True):
            text = self.whitespace_pattern.sub(' ', text)
        
        return text.strip()
    
    def _anonymize_sensitive_data(self, text: str) -> str:
        """
        Анонимизация конфиденциальных данных
        
        Args:
            text: Исходный текст
        
        Returns:
            Текст с анонимизированными данными
        """
        # Маскирование номеров карт
        text = self.card_number_pattern.sub(' [НОМЕР_КАРТЫ] ', text)
        
        # Маскирование номеров счетов
        text = self.account_number_pattern.sub(' [НОМЕР_СЧЕТА] ', text)
        
        return text
    
    def _normalize_banking_terms(self, text: str) -> str:
        """
        Нормализация банковских терминов
        
        Args:
            text: Исходный текст
        
        Returns:
            Текст с нормализованными терминами
        """
        words = text.split()
        normalized_words = []
        
        for word in words:
            # Очистка слова от знаков препинания для проверки
            clean_word = word.strip('.,!?():;')
            
            # Проверка наличия в словаре банковских терминов
            if clean_word in self.banking_terms:
                normalized_words.append(self.banking_terms[clean_word])
            else:
                normalized_words.append(word)
        
        return ' '.join(normalized_words)
    
    def batch_preprocess(self, texts: List[str]) -> List[str]:
        """
        Пакетная обработка текстов
        
        Args:
            texts: Список исходных текстов
        
        Returns:
            Список предобработанных текстов
        """
        return [self.preprocess(text) for text in texts]


class DialoguePreprocessor:
    """
    Класс для предобработки диалогов между клиентом и оператором банка
    """
    
    def __init__(self):
        """
        Инициализация препроцессора диалогов
        """
        self.text_preprocessor = BankingTextPreprocessor()
        logger.info("Инициализирован препроцессор диалогов")
    
    def preprocess_dialogue(self, dialogue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Предобработка диалога
        
        Args:
            dialogue: Словарь с данными диалога
                {
                    'id': str,
                    'timestamp': str,
                    'turns': [
                        {'speaker': 'client', 'text': str},
                        {'speaker': 'operator', 'text': str},
                        ...
                    ]
                }
        
        Returns:
            Предобработанный диалог
        """
        if not dialogue or 'turns' not in dialogue:
            logger.warning(f"Получен некорректный диалог: {dialogue}")
            return dialogue
        
        processed_dialogue = dialogue.copy()
        
        # Обработка каждой реплики в диалоге
        for i, turn in enumerate(processed_dialogue['turns']):
            if 'text' in turn:
                processed_dialogue['turns'][i]['text'] = self.text_preprocessor.preprocess(turn['text'])
                processed_dialogue['turns'][i]['processed'] = True
        
        return processed_dialogue
    
    def extract_client_queries(self, dialogue: Dict[str, Any]) -> List[str]:
        """
        Извлечение запросов клиента из диалога
        
        Args:
            dialogue: Словарь с данными диалога
        
        Returns:
            Список запросов клиента
        """
        if not dialogue or 'turns' not in dialogue:
            return []
        
        client_queries = []
        
        for turn in dialogue['turns']:
            if turn.get('speaker') == 'client' and 'text' in turn:
                processed_text = self.text_preprocessor.preprocess(turn['text'])
                if processed_text:
                    client_queries.append(processed_text)
        
        return client_queries
    
    def extract_operator_responses(self, dialogue: Dict[str, Any]) -> List[str]:
        """
        Извлечение ответов оператора из диалога
        
        Args:
            dialogue: Словарь с данными диалога
        
        Returns:
            Список ответов оператора
        """
        if not dialogue or 'turns' not in dialogue:
            return []
        
        operator_responses = []
        
        for turn in dialogue['turns']:
            if turn.get('speaker') == 'operator' and 'text' in turn:
                processed_text = self.text_preprocessor.preprocess(turn['text'])
                if processed_text:
                    operator_responses.append(processed_text)
        
        return operator_responses
