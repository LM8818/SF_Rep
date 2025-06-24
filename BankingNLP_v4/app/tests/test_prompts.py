"""
Тесты для модуля управления промтами
"""

import pytest
import json
import logging
import time
from unittest.mock import patch, MagicMock
from pathlib import Path

from app.core.prompts import (
    PromptManager, 
    PromptTemplate, 
    PromptType, 
    get_prompt_manager
)

logger = logging.getLogger("test_prompts")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_prompts.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_prompts.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

class TestPromptTemplate:
    """Тесты для класса PromptTemplate"""
    
    def test_prompt_template_creation(self):
        """Тест создания промта"""
        prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание тестового промта",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Тестовый шаблон {parameter}",
            parameters=["parameter"],
            version="1.0"
        )
        logger.info("Проверка создания промта — успешно")
        assert prompt.name == "Тестовый промт"
        assert prompt.description == "Описание тестового промта"
        assert prompt.prompt_type == PromptType.TOPIC_EXTRACTION
        assert prompt.template == "Тестовый шаблон {parameter}"
        assert prompt.parameters == ["parameter"]
        assert prompt.version == "1.0"
        assert prompt.is_active is True
    
    def test_prompt_template_validation(self):
        """Тест валидации промта"""
        with pytest.raises(ValueError, match="Промт не может быть пустым"):
            PromptTemplate(
                name="Тест",
                description="Описание",
                prompt_type=PromptType.TOPIC_EXTRACTION,
                template="",  # Пустой шаблон
                parameters=[]
            )
        logger.info("Проверка валидации пустого шаблона — успешно")


class TestPromptManager:
    """Тесты для класса PromptManager"""
    
    @pytest.fixture
    def temp_prompts_file(self, tmp_path):
        """Временный файл для промтов"""
        return tmp_path / "test_prompts.json"
    
    @pytest.fixture
    def prompt_manager(self, temp_prompts_file):
        """Менеджер промтов с временным файлом"""
        with patch('app.core.prompts.Path') as mock_path:
            mock_path.return_value = temp_prompts_file
            return PromptManager(str(temp_prompts_file))
    
    def test_prompt_manager_initialization(self, prompt_manager):
        """Тест инициализации менеджера промтов"""
        logger.info("Проверка инициализации менеджера промтов — успешно")
        assert len(prompt_manager.prompts) > 0
        assert "topic_extraction_v1" in prompt_manager.prompts
        assert "product_analysis_v1" in prompt_manager.prompts
        assert "sentiment_analysis_v1" in prompt_manager.prompts
        assert "benchmark_v1" in prompt_manager.prompts
    
    def test_get_prompt(self, prompt_manager):
        """Тест получения промта по ID"""
        prompt = prompt_manager.get_prompt("topic_extraction_v1")
        logger.info("Проверка получения промта по ID — успешно")
        assert prompt is not None
        assert prompt.name == "Извлечение тематик v1"
        assert prompt.prompt_type == PromptType.TOPIC_EXTRACTION
    
    def test_get_nonexistent_prompt(self, prompt_manager):
        """Тест получения несуществующего промта"""
        prompt = prompt_manager.get_prompt("nonexistent")
        logger.info("Проверка получения несуществующего промта — успешно")
        assert prompt is None
    
    def test_get_prompts_by_type(self, prompt_manager):
        """Тест получения промтов по типу"""
        topic_prompts = prompt_manager.get_prompts_by_type(PromptType.TOPIC_EXTRACTION)
        logger.info("Проверка получения промтов по типу — успешно")
        assert len(topic_prompts) > 0
        assert all(p.prompt_type == PromptType.TOPIC_EXTRACTION for p in topic_prompts)
    
    def test_get_active_prompts(self, prompt_manager):
        """Тест получения активных промтов"""
        active_prompts = prompt_manager.get_active_prompts()
        logger.info("Проверка получения активных промтов — успешно")
        assert len(active_prompts) > 0
        assert all(p.is_active for p in active_prompts)
    
    def test_add_prompt(self, prompt_manager, temp_prompts_file):
        """Тест добавления нового промта"""
        new_prompt = PromptTemplate(
            name="Новый промт",
            description="Описание нового промта",
            prompt_type=PromptType.CUSTOM,
            template="Новый шаблон {param}",
            parameters=["param"],
            version="1.0"
        )
        
        prompt_manager.add_prompt("custom_test", new_prompt)
        logger.info("Проверка добавления нового промта — успешно")
        
        # Проверяем, что промт добавлен
        added_prompt = prompt_manager.get_prompt("custom_test")
        assert added_prompt is not None
        assert added_prompt.name == "Новый промт"
        
        # Проверяем, что файл создан
        assert temp_prompts_file.exists()
    
    def test_update_prompt(self, prompt_manager):
        """Тест обновления промта"""
        # Сначала добавляем кастомный промт
        custom_prompt = PromptTemplate(
            name="Обновляемый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        prompt_manager.add_prompt("update_test", custom_prompt)
        
        # Обновляем промт
        prompt_manager.update_prompt("update_test", name="Обновленное имя", is_active=False)
        logger.info("Проверка обновления промта — успешно")
        
        updated_prompt = prompt_manager.get_prompt("update_test")
        assert updated_prompt.name == "Обновленное имя"
        assert updated_prompt.is_active is False
    
    def test_delete_prompt(self, prompt_manager):
        """Тест удаления промта"""
        # Добавляем кастомный промт
        custom_prompt = PromptTemplate(
            name="Удаляемый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        prompt_manager.add_prompt("delete_test", custom_prompt)
        
        # Проверяем, что промт существует
        assert prompt_manager.get_prompt("delete_test") is not None
        
        # Удаляем промт
        prompt_manager.delete_prompt("delete_test")
        logger.info("Проверка удаления промта — успешно")
        
        # Проверяем, что промт удален
        assert prompt_manager.get_prompt("delete_test") is None
    
    def test_delete_standard_prompt_fails(self, prompt_manager):
        """Тест, что нельзя удалить стандартный промт"""
        with pytest.raises(ValueError, match="Нельзя удалить стандартный промт"):
            prompt_manager.delete_prompt("topic_extraction_v1")
        logger.info("Проверка невозможности удаления стандартного промта — успешно")
    
    def test_format_prompt(self, prompt_manager):
        """Тест форматирования промта"""
        formatted = prompt_manager.format_prompt(
            "topic_extraction_v1", 
            conversation_text="Тестовый разговор"
        )
        logger.info("Проверка форматирования промта — успешно")
        assert "Тестовый разговор" in formatted
        assert "РАЗГОВОР:" in formatted
    
    def test_format_prompt_missing_parameter(self, prompt_manager):
        """Тест форматирования промта с отсутствующим параметром"""
        with pytest.raises(ValueError, match="Отсутствует обязательный параметр"):
            prompt_manager.format_prompt("topic_extraction_v1")
        logger.info("Проверка ошибки при отсутствии обязательного параметра — успешно")
    
    def test_format_nonexistent_prompt(self, prompt_manager):
        """Тест форматирования несуществующего промта"""
        with pytest.raises(ValueError, match="Промт nonexistent не найден"):
            prompt_manager.format_prompt("nonexistent", conversation_text="test")
        logger.info("Проверка ошибки при форматировании несуществующего промта — успешно")
    
    def test_list_prompts(self, prompt_manager):
        """Тест получения списка промтов"""
        prompts_list = prompt_manager.list_prompts()
        
        logger.info("Проверка получения списка промтов — успешно")
        
        assert isinstance(prompts_list, dict)
        assert "topic_extraction_v1" in prompts_list
        
        prompt_info = prompts_list["topic_extraction_v1"]
        assert "name" in prompt_info
        assert "description" in prompt_info
        assert "type" in prompt_info
        assert "version" in prompt_info
        assert "is_active" in prompt_info
        assert "parameters" in prompt_info
    
    def test_load_custom_prompts(self, temp_prompts_file):
        """Тест загрузки пользовательских промтов из файла"""
        # Создаем тестовый файл с промтами
        custom_prompts = {
            "custom_test": {
                "name": "Кастомный промт",
                "description": "Описание",
                "prompt_type": "custom",
                "template": "Шаблон {param}",
                "parameters": ["param"],
                "version": "1.0",
                "is_active": True,
                "metadata": {}
            }
        }
        
        with open(temp_prompts_file, 'w', encoding='utf-8') as f:
            json.dump(custom_prompts, f, ensure_ascii=False, indent=2)
        
        # Создаем менеджер
        with patch('app.core.prompts.Path') as mock_path:
            mock_path.return_value = temp_prompts_file
            manager = PromptManager(str(temp_prompts_file))
        
        # Проверяем, что кастомный промт загружен
        custom_prompt = manager.get_prompt("custom_test")
        logger.info("Проверка загрузки пользовательских промтов из файла — успешно")
        assert custom_prompt is not None
        assert custom_prompt.name == "Кастомный промт"
        assert custom_prompt.prompt_type == PromptType.CUSTOM
    
    def test_save_custom_prompts(self, temp_prompts_file):
        """Тест сохранения пользовательских промтов"""
        with patch('app.core.prompts.Path') as mock_path:
            mock_path.return_value = temp_prompts_file
            manager = PromptManager(str(temp_prompts_file))
        
        # Добавляем кастомный промт
        custom_prompt = PromptTemplate(
            name="Сохраняемый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        manager.add_prompt("save_test", custom_prompt)
        
        # Проверяем, что файл создан и содержит данные
        assert temp_prompts_file.exists()
        
        with open(temp_prompts_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        logger.info("Проверка сохранения пользовательских промтов — успешно")
        assert "save_test" in saved_data
        assert saved_data["save_test"]["name"] == "Сохраняемый промт"


class TestPromptType:
    """Тесты для enum PromptType"""
    
    def test_prompt_type_values(self):
        """Тест значений типов промтов"""
        logger.info("Проверка значений типов промтов — успешно")
        assert PromptType.TOPIC_EXTRACTION.value == "topic_extraction"
        assert PromptType.PRODUCT_ANALYSIS.value == "product_analysis"
        assert PromptType.SENTIMENT_ANALYSIS.value == "sentiment_analysis"
        assert PromptType.INTENT_CLASSIFICATION.value == "intent_classification"
        assert PromptType.SUMMARIZATION.value == "summarization"
        assert PromptType.BENCHMARK.value == "benchmark"
        assert PromptType.CUSTOM.value == "custom"


class TestGetPromptManager:
    """Тесты для функции get_prompt_manager"""
    
    def test_get_prompt_manager(self):
        """Тест получения глобального менеджера промтов"""
        manager = get_prompt_manager()
        logger.info("Проверка получения глобального менеджера промтов — успешно")
        assert isinstance(manager, PromptManager)
        
        # Проверяем, что возвращается тот же экземпляр
        manager2 = get_prompt_manager()
        assert manager is manager2


class TestPromptManagerIntegration:
    """Интеграционные тесты для PromptManager"""
    
    def test_full_workflow(self, tmp_path):
        """Тест полного рабочего процесса"""
        temp_prompts_file = tmp_path / "integration_test_prompts.json"
        
        with patch('app.core.prompts.Path') as mock_path:
            mock_path.return_value = temp_prompts_file
            manager = PromptManager(str(temp_prompts_file))
        
        # 1. Создаем промт
        custom_prompt = PromptTemplate(
            name="Интеграционный тест",
            description="Промт для интеграционного тестирования",
            prompt_type=PromptType.CUSTOM,
            template="Анализируй: {text}\nРезультат: {format}",
            parameters=["text", "format"],
            version="1.0"
        )
        
        manager.add_prompt("integration_test", custom_prompt)
        
        # 2. Проверяем, что промт создан
        created_prompt = manager.get_prompt("integration_test")
        assert created_prompt is not None
        assert created_prompt.name == "Интеграционный тест"
        
        # 3. Форматируем промт
        formatted = manager.format_prompt(
            "integration_test",
            text="Тестовый текст",
            format="JSON"
        )
        assert "Тестовый текст" in formatted
        assert "JSON" in formatted
        
        # 4. Обновляем промт
        manager.update_prompt("integration_test", description="Обновленное описание")
        updated_prompt = manager.get_prompt("integration_test")
        assert updated_prompt.description == "Обновленное описание"
        
        # 5. Деактивируем промт
        manager.update_prompt("integration_test", is_active=False)
        deactivated_prompt = manager.get_prompt("integration_test")
        assert deactivated_prompt.is_active is False
        
        # 6. Удаляем промт
        manager.delete_prompt("integration_test")
        deleted_prompt = manager.get_prompt("integration_test")
        logger.info("Проверка полного рабочего процесса менеджера промтов — успешно")
        assert deleted_prompt is None

def test_add_and_get_prompt():
    test_name = "test_add_and_get_prompt"
    params = {"name": "Тестовый"}
    log_test_start(test_name, **params)
    start = time.time()
    manager = PromptManager()
    prompt = PromptTemplate(
        name="Тестовый",
        description="Описание",
        prompt_type=PromptType.CUSTOM,
        template="Шаблон {param}",
        parameters=["param"],
        version="1.0"
    )
    manager.add_prompt(prompt)
    result = manager.get_prompt("Тестовый")
    try:
        assert result.name == "Тестовый"
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise

def test_update_prompt():
    test_name = "test_update_prompt"
    params = {"name": "Тестовый", "new_version": "1.1"}
    log_test_start(test_name, **params)
    start = time.time()
    manager = PromptManager()
    prompt = PromptTemplate(
        name="Тестовый",
        description="Описание",
        prompt_type=PromptType.CUSTOM,
        template="Шаблон {param}",
        parameters=["param"],
        version="1.0"
    )
    manager.add_prompt(prompt)
    prompt_new = PromptTemplate(
        name="Тестовый",
        description="Новое описание",
        prompt_type=PromptType.CUSTOM,
        template="Шаблон {param}",
        parameters=["param"],
        version="1.1"
    )
    manager.update_prompt("Тестовый", prompt_new)
    result = manager.get_prompt("Тестовый")
    try:
        assert result.description == "Новое описание"
        assert result.version == "1.1"
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise

def test_delete_prompt():
    test_name = "test_delete_prompt"
    params = {"name": "Тестовый"}
    log_test_start(test_name, **params)
    start = time.time()
    manager = PromptManager()
    prompt = PromptTemplate(
        name="Тестовый",
        description="Описание",
        prompt_type=PromptType.CUSTOM,
        template="Шаблон {param}",
        parameters=["param"],
        version="1.0"
    )
    manager.add_prompt(prompt)
    manager.delete_prompt("Тестовый")
    try:
        assert manager.get_prompt("Тестовый") is None
        log_test_end(test_name, time.time()-start)
    except AssertionError as e:
        logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
        raise 