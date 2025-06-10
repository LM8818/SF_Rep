"""
Утилиты предобработки текста для NLP анализа
==========================================

Функции для очистки, нормализации и подготовки текста
для анализа банковских разговоров.
"""

import re
import string
from typing import List, Optional


def clean_text(text: str) -> str:
    """
    Очистка текста от лишних символов и форматирования

    Args:
        text: Исходный текст

    Returns:
        str: Очищенный текст
    """
    if not text:
        return ""

    # Удаление HTML тегов (если есть)
    text = re.sub(r'<[^>]+>', '', text)

    # Удаление URL
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Удаление email адресов
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Удаление номеров телефонов (простой паттерн)
    text = re.sub(r'\+?[1-9][0-9]{7,14}', '', text)

    # Удаление множественных пробелов
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def normalize_text(text: str) -> str:
    """
    Нормализация текста для анализа

    Args:
        text: Текст для нормализации

    Returns:
        str: Нормализованный текст
    """
    if not text:
        return ""

    # Приведение к нижнему регистру
    text = text.lower()

    # Удаление знаков пунктуации
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Удаление цифр (опционально)
    # text = re.sub(r'\d+', '', text)

    # Удаление множественных пробелов
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Извлечение ключевых слов из текста

    Args:
        text: Исходный текст
        min_length: Минимальная длина слова

    Returns:
        List[str]: Список ключевых слов
    """
    if not text:
        return []

    # Очистка и нормализация
    text = normalize_text(text)

    # Разбивка на слова
    words = text.split()

    # Фильтрация по длине
    keywords = [word for word in words if len(word) >= min_length]

    # Удаление дубликатов с сохранением порядка
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)

    return unique_keywords


def mask_personal_data(text: str) -> str:
    """
    Маскировка персональных данных в тексте

    Args:
        text: Текст с потенциальными персональными данными

    Returns:
        str: Текст с замаскированными персональными данными
    """
    if not text:
        return ""

    # Маскировка номеров телефонов
    text = re.sub(r'\+?[1-9][0-9]{7,14}', '[PHONE]', text)

    # Маскировка email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

    # Маскировка номеров карт (простой паттерн)
    text = re.sub(r'\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b', '[CARD_NUMBER]', text)

    # Маскировка имен (простая эвристика - слова с заглавной буквы)
    text = re.sub(r'\b[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\b', '[NAME]', text)

    return text


def split_into_sentences(text: str) -> List[str]:
    """
    Разбивка текста на предложения

    Args:
        text: Исходный текст

    Returns:
        List[str]: Список предложений
    """
    if not text:
        return []

    # Простая разбивка по знакам препинания
    sentences = re.split(r'[.!?]+', text)

    # Очистка и фильтрация пустых строк
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences
