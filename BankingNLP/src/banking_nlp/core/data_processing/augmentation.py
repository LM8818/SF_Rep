"""
Модуль для аугментации текстовых данных в банковской сфере с использованием современных библиотек
"""
import random
import re
from typing import List, Dict, Any, Optional
import logging

# Импорт nlpaug для продвинутой аугментации
import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.flow as naflow

from utils.logging import get_logger

logger = get_logger(__name__)

class RussianBankingAugmenter:
    """
    Комплексный аугментатор для русскоязычных банковских текстов
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        
        # Расширенный словарь синонимов для банковских терминов
        self.banking_synonyms = {
            'кредит': ['заём', 'ссуда', 'займ', 'финансирование', 'кредитование'],
            'депозит': ['вклад', 'сбережение', 'накопление', 'размещение'],
            'карта': ['пластик', 'платежное средство', 'банковская карта', 'карточка'],
            'счет': ['аккаунт', 'банковский счет', 'учетная запись', 'расчетный счет'],
            'процент': ['ставка', 'процентная ставка', 'интерес', 'доходность'],
            'платеж': ['выплата', 'взнос', 'транзакция', 'операция', 'перевод'],
            'банк': ['финансовое учреждение', 'кредитная организация'],
            'клиент': ['пользователь', 'потребитель', 'заемщик', 'вкладчик'],
            'оператор': ['консультант', 'специалист', 'менеджер', 'сотрудник'],
            'проблема': ['вопрос', 'затруднение', 'сложность', 'трудность'],
            'деньги': ['средства', 'денежные средства', 'финансы', 'капитал'],
            'ипотека': ['ипотечный кредит', 'жилищный кредит'],
            'страхование': ['страховка', 'страховое покрытие'],
            'инвестиции': ['вложения', 'капиталовложения', 'инвестирование']
        }
        
        # Инициализация аугментаторов из nlpaug
        self.keyboard_aug = nac.KeyboardAug(aug_char_min=1, aug_char_max=2, aug_word_p=0.3)
        self.word_swap_aug = naw.RandomWordAug(action="swap", aug_p=0.3)
        self.word_delete_aug = naw.RandomWordAug(action="delete", aug_p=0.2)
        
        logger.info("Инициализирован продвинутый аугментатор текста с nlpaug")
    
    def synonym_replacement(self, text: str, n: int = 2) -> str:
        """Замена слов на банковские синонимы"""
        words = text.split()
        if len(words) <= 1:
            return text
        
        n = min(n, len(words) // 3) or 1
        replacement_indices = random.sample(range(len(words)), n)
        
        for i in replacement_indices:
            word = words[i].lower().strip('.,!?():;')
            if word in self.banking_synonyms:
                synonym = random.choice(self.banking_synonyms[word])
                words[i] = synonym
        
        return ' '.join(words)
    
    def nlpaug_augmentation(self, text: str, method: str = 'keyboard') -> str:
        """Аугментация с использованием nlpaug"""
        try:
            if method == 'keyboard':
                return self.keyboard_aug.augment(text)[0]
            elif method == 'swap':
                return self.word_swap_aug.augment(text)[0]
            elif method == 'delete':
                return self.word_delete_aug.augment(text)[0]
        except Exception as e:
            logger.warning(f"Ошибка в nlpaug аугментации: {e}")
            return text
        return text
    
    def augment(self, text: str, methods: List[str] = None) -> List[str]:
        """Комплексная аугментация текста"""
        if methods is None:
            methods = ['synonym', 'keyboard', 'swap', 'delete']
        
        augmented_texts = []
        
        for method in methods:
            if method == 'synonym':
                augmented_texts.append(self.synonym_replacement(text))
            elif method in ['keyboard', 'swap', 'delete']:
                augmented_texts.append(self.nlpaug_augmentation(text, method))
        
        return augmented_texts
