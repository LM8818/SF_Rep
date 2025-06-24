"""
Модуль для управления промтами системы BankingNLP
Позволяет выбирать и настраивать промты в процессе эксплуатации
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, field_validator


class PromptType(Enum):
    """Типы промтов"""
    TOPIC_EXTRACTION = "topic_extraction"
    PRODUCT_ANALYSIS = "product_analysis"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    INTENT_CLASSIFICATION = "intent_classification"
    SUMMARIZATION = "summarization"
    BENCHMARK = "benchmark"
    CUSTOM = "custom"


class PromptTemplate(BaseModel):
    """Шаблон промта"""
    name: str
    description: str
    prompt_type: PromptType
    template: str
    parameters: List[str] = []
    version: str = "1.0"
    is_active: bool = True
    metadata: Dict[str, Any] = {}
    
    @field_validator('template')
    @classmethod
    def validate_template(cls, v):
        if not v.strip():
            raise ValueError('Промт не может быть пустым')
        return v


class PromptManager:
    """Менеджер промтов для системы BankingNLP"""
    
    def __init__(self, prompts_file: str = "prompts.json"):
        self.prompts_file = Path(__file__).parent.parent.parent / prompts_file
        self.logger = logging.getLogger(__name__)
        self.prompts: Dict[str, PromptTemplate] = {}
        self._load_default_prompts()
        self._load_custom_prompts()
    
    def _load_default_prompts(self):
        """Загружает стандартные промты"""
        default_prompts = {
            "topic_extraction_v1": PromptTemplate(
                name="Извлечение тематик v1",
                description="Стандартный промт для извлечения тематик из банковских разговоров",
                prompt_type=PromptType.TOPIC_EXTRACTION,
                template="""Ты - эксперт по анализу банковских разговоров с клиентами. 
Проанализируй следующий транскрибированный разговор и выдели основные тематики:

РАЗГОВОР:
{conversation_text}

ИНСТРУКЦИИ:
1. Определи не менее 3-5 основных тематик
2. Для каждой тематики укажи:
   - Название тематики
   - Уверенность (0-100%)
   - Контекст упоминания
3. Тематики могут включать:
   - Финансовые продукты (кредиты, вклады, карты)
   - Проблемные ситуации (технические сбои, претензии)
   - Жизненные события (свадьба, покупка жилья)
   - Конкурентные предложения

ОТВЕТ В ФОРМАТЕ JSON:
{{
  "topics": [
    {{
      "name": "название тематики",
      "confidence": 85,
      "context": "описание контекста",
      "category": "категория"
    }}
  ]
}}""",
                parameters=["conversation_text"],
                version="1.0"
            ),
            
            "product_analysis_v1": PromptTemplate(
                name="Анализ продуктов v1",
                description="Промт для анализа продуктовых упоминаний в разговорах",
                prompt_type=PromptType.PRODUCT_ANALYSIS,
                template="""Ты - аналитик банковских продуктов. 
Проанализируй разговор и выяви все упоминания банковских продуктов:

РАЗГОВОР:
{conversation_text}

ИНСТРУКЦИИ:
1. Найди все упоминания банковских продуктов
2. Для каждого продукта определи:
   - Название продукта
   - Тип продукта (кредит, вклад, карта, страхование)
   - Контекст упоминания (интерес, отказ, сравнение)
   - Эмоциональный окрас
   - Причина отказа (если есть)

ОТВЕТ В ФОРМАТЕ JSON:
{{
  "products": [
    {{
      "name": "название продукта",
      "type": "тип продукта",
      "context": "контекст упоминания",
      "sentiment": "позитивный/негативный/нейтральный",
      "rejection_reason": "причина отказа (если есть)"
    }}
  ]
}}""",
                parameters=["conversation_text"],
                version="1.0"
            ),
            
            "sentiment_analysis_v1": PromptTemplate(
                name="Анализ настроений v1",
                description="Промт для анализа эмоционального окраса разговора",
                prompt_type=PromptType.SENTIMENT_ANALYSIS,
                template="""Ты - эксперт по анализу эмоций в банковских разговорах.
Проанализируй эмоциональный окрас следующего разговора:

РАЗГОВОР:
{conversation_text}

ИНСТРУКЦИИ:
1. Определи общий эмоциональный окрас разговора
2. Выяви ключевые эмоциональные моменты
3. Оцени уровень удовлетворенности клиента
4. Определи триггеры эмоций

ОТВЕТ В ФОРМАТЕ JSON:
{{
  "overall_sentiment": "позитивный/негативный/нейтральный",
  "sentiment_score": 0.75,
  "emotional_moments": [
    {{
      "moment": "описание момента",
      "emotion": "эмоция",
      "intensity": "высокая/средняя/низкая"
    }}
  ],
  "satisfaction_level": "высокий/средний/низкий",
  "triggers": ["список триггеров"]
}}""",
                parameters=["conversation_text"],
                version="1.0"
            ),
            
            "benchmark_v1": PromptTemplate(
                name="Бенчмарк производительности v1",
                description="Промт для тестирования производительности системы",
                prompt_type=PromptType.BENCHMARK,
                template="""Ты - система анализа банковских разговоров.
Обработай следующий разговор для тестирования производительности:

РАЗГОВОР:
{conversation_text}

ИНСТРУКЦИИ:
1. Выполни полный анализ разговора
2. Извлеки тематики, продукты, настроения
3. Сформируй краткое резюме
4. Ответ должен быть структурированным и полным

ОТВЕТ В ФОРМАТЕ JSON:
{{
  "analysis": {{
    "topics": ["список тематик"],
    "products": ["список продуктов"],
    "sentiment": "общий окрас",
    "summary": "краткое резюме"
  }},
  "processing_time": "время обработки в секундах"
}}""",
                parameters=["conversation_text"],
                version="1.0"
            )
        }
        
        for key, prompt in default_prompts.items():
            self.prompts[key] = prompt
    
    def _load_custom_prompts(self):
        """Загружает пользовательские промты из файла"""
        if self.prompts_file.exists():
            try:
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for key, prompt_data in data.items():
                    prompt = PromptTemplate(**prompt_data)
                    self.prompts[key] = prompt
                    
                self.logger.info(f"Загружено {len(data)} пользовательских промтов")
                
            except Exception as e:
                self.logger.error(f"Ошибка загрузки пользовательских промтов: {e}")
    
    def save_custom_prompts(self):
        """Сохраняет пользовательские промты в файл"""
        custom_prompts = {}
        
        for key, prompt in self.prompts.items():
            if prompt.prompt_type == PromptType.CUSTOM:
                # Преобразуем enum в строку для сериализации
                prompt_dict = prompt.model_dump()
                prompt_dict['prompt_type'] = prompt.prompt_type.value
                custom_prompts[key] = prompt_dict
        
        try:
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(custom_prompts, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Сохранено {len(custom_prompts)} пользовательских промтов")
            
        except Exception as e:
            self.logger.error(f"Ошибка сохранения пользовательских промтов: {e}")
    
    def get_prompt(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Получает промт по ID"""
        return self.prompts.get(prompt_id)
    
    def get_prompts_by_type(self, prompt_type: PromptType) -> List[PromptTemplate]:
        """Получает все промты определенного типа"""
        return [
            prompt for prompt in self.prompts.values() 
            if prompt.prompt_type == prompt_type and prompt.is_active
        ]
    
    def get_active_prompts(self) -> List[PromptTemplate]:
        """Получает все активные промты"""
        return [prompt for prompt in self.prompts.values() if prompt.is_active]
    
    def add_prompt(self, prompt_id: str, prompt: PromptTemplate):
        """Добавляет новый промт"""
        self.prompts[prompt_id] = prompt
        if prompt.prompt_type == PromptType.CUSTOM:
            self.save_custom_prompts()
        
        self.logger.info(f"Добавлен новый промт: {prompt_id}")
    
    def update_prompt(self, prompt_id: str, **kwargs):
        """Обновляет существующий промт"""
        if prompt_id in self.prompts:
            prompt = self.prompts[prompt_id]
            for key, value in kwargs.items():
                if hasattr(prompt, key):
                    setattr(prompt, key, value)
            
            if prompt.prompt_type == PromptType.CUSTOM:
                self.save_custom_prompts()
            
            self.logger.info(f"Обновлен промт: {prompt_id}")
        else:
            raise ValueError(f"Промт {prompt_id} не найден")
    
    def delete_prompt(self, prompt_id: str):
        """Удаляет промт"""
        if prompt_id in self.prompts:
            prompt = self.prompts[prompt_id]
            if prompt.prompt_type == PromptType.CUSTOM:
                del self.prompts[prompt_id]
                self.save_custom_prompts()
                self.logger.info(f"Удален промт: {prompt_id}")
            else:
                raise ValueError(f"Нельзя удалить стандартный промт: {prompt_id}")
        else:
            raise ValueError(f"Промт {prompt_id} не найден")
    
    def format_prompt(self, prompt_id: str, **kwargs) -> str:
        """Форматирует промт с переданными параметрами"""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError(f"Промт {prompt_id} не найден")
        
        try:
            return prompt.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательный параметр: {e}")
    
    def list_prompts(self) -> Dict[str, Dict[str, Any]]:
        """Возвращает список всех промтов с метаданными"""
        return {
            prompt_id: {
                "name": prompt.name,
                "description": prompt.description,
                "type": prompt.prompt_type.value,
                "version": prompt.version,
                "is_active": prompt.is_active,
                "parameters": prompt.parameters
            }
            for prompt_id, prompt in self.prompts.items()
        }


# Глобальный экземпляр менеджера промтов
prompt_manager = PromptManager()


def get_prompt_manager() -> PromptManager:
    """Возвращает глобальный менеджер промтов"""
    return prompt_manager 