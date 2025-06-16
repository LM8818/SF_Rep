"""
Модуль для лемматизации русскоязычных текстов
"""
import logging
from typing import List, Dict, Any, Optional
from utils.logging import get_logger

logger = get_logger(__name__)

class RussianLemmatizer:
    """
    Лемматизатор для русского языка с поддержкой различных библиотек
    """
    
    def __init__(self, backend: str = 'pymorphy2'):
        self.backend = backend
        self.analyzer = None
        self._init_backend()
    
    def _init_backend(self):
        """Инициализация выбранного backend'а"""
        if self.backend == 'pymorphy2':
            try:
                import pymorphy2
                self.analyzer = pymorphy2.MorphAnalyzer()
                logger.info("Инициализирован Pymorphy2 лемматизатор")
            except ImportError:
                logger.error("Pymorphy2 не установлен. Установите: pip install pymorphy2")
                raise
        elif self.backend == 'natasha':
            try:
                from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc
                self.segmenter = Segmenter()
                self.morph_vocab = MorphVocab()
                self.emb = NewsEmbedding()
                self.morph_tagger = NewsMorphTagger(self.emb)
                logger.info("Инициализирован Natasha лемматизатор")
            except ImportError:
                logger.error("Natasha не установлен. Установите: pip install natasha")
                raise
    
    def lemmatize_word(self, word: str) -> str:
        """Лемматизация одного слова"""
        if self.backend == 'pymorphy2':
            return self._pymorphy2_lemmatize(word)
        elif self.backend == 'natasha':
            return self._natasha_lemmatize(word)
        return word
    
    def _pymorphy2_lemmatize(self, word: str) -> str:
        """Лемматизация с помощью Pymorphy2"""
        parsed = self.analyzer.parse(word)[0]
        return parsed.normal_form
    
    def _natasha_lemmatize(self, word: str) -> str:
        """Лемматизация с помощью Natasha"""
        doc = Doc(word)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)
            return token.lemma
        return word
    
    def lemmatize_text(self, text: str) -> str:
        """Лемматизация текста"""
        words = text.split()
        lemmatized_words = [self.lemmatize_word(word.strip('.,!?():;')) for word in words]
        return ' '.join(lemmatized_words)
