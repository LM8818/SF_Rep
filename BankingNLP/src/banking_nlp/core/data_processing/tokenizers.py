"""
Модуль для токенизации текстов банковской тематики
"""
import re
from typing import List, Dict, Any, Optional, Union
import logging

from transformers import AutoTokenizer
from utils.logging import get_logger

logger = get_logger(__name__)

class BankingTokenizer:
    """
    Токенизатор для текстов банковской тематики
    """
    
    def __init__(self, model_name: str = "sberbank-ai/ruBERT-base", max_length: int = 512):
        """
        Инициализация токенизатора
        
        Args:
            model_name: Название предобученной модели для токенизатора
            max_length: Максимальная длина последовательности токенов
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info(f"Загружен токенизатор модели {model_name}")
        except Exception as e:
            logger.error(f"Ошибка загрузки токенизатора {model_name}: {e}")
            raise
        
        self.max_length = max_length
        
        # Специальные токены для банковской тематики
        self.special_tokens = {
            "CARD_NUMBER": "[НОМЕР_КАРТЫ]",
            "ACCOUNT_NUMBER": "[НОМЕР_СЧЕТА]",
            "PHONE": "[ТЕЛЕФОН]",
            "EMAIL": "[EMAIL]",
            "URL": "[URL]",
            "AMOUNT": "[СУММА]",
            "DATE": "[ДАТА]"
        }
        
        # Добавление специальных токенов в словарь токенизатора
        special_tokens_dict = {"additional_special_tokens": list(self.special_tokens.values())}
        self.tokenizer.add_special_tokens(special_tokens_dict)
        
        # Регулярные выражения для обнаружения финансовых сущностей
        self.amount_pattern = re.compile(r'\b\d+([.,]\d+)?\s*(руб|₽|рублей|долларов|\$|евро|€)\b')
        self.date_pattern = re.compile(r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b')
    
    def preprocess_for_tokenization(self, text: str) -> str:
        """
        Предобработка текста перед токенизацией
        
        Args:
            text: Исходный текст
        
        Returns:
            Предобработанный текст
        """
        # Обработка денежных сумм
        text = self.amount_pattern.sub(' [СУММА] ', text)
        
        # Обработка дат
        text = self.date_pattern.sub(' [ДАТА] ', text)
        
        return text
    
    def tokenize(self, text: str) -> Dict[str, Any]:
        """
        Токенизация текста
        
        Args:
            text: Исходный текст
        
        Returns:
            Словарь с токенами и масками внимания
        """
        # Предобработка текста
        preprocessed_text = self.preprocess_for_tokenization(text)
        
        # Токенизация
        encoding = self.tokenizer(
            preprocessed_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"],
            "attention_mask": encoding["attention_mask"]
        }
    
    def batch_tokenize(self, texts: List[str]) -> Dict[str, Any]:
        """
        Пакетная токенизация текстов
        
        Args:
            texts: Список исходных текстов
        
        Returns:
            Словарь с токенами и масками внимания для всех текстов
        """
        # Предобработка текстов
        preprocessed_texts = [self.preprocess_for_tokenization(text) for text in texts]
        
        # Токенизация
        encoding = self.tokenizer(
            preprocessed_texts,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"],
            "attention_mask": encoding["attention_mask"]
        }
    
    def decode(self, token_ids: Union[List[int], List[List[int]]]) -> Union[str, List[str]]:
        """
        Декодирование токенов в текст
        
        Args:
            token_ids: Список ID токенов или список списков ID токенов
        
        Returns:
            Декодированный текст или список текстов
        """
        return self.tokenizer.decode(token_ids, skip_special_tokens=True)
    
    def get_vocab_size(self) -> int:
        """
        Получение размера словаря токенизатора
        
        Returns:
            Размер словаря
        """
        return len(self.tokenizer)
