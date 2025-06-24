"""
Тесты для API эндпоинтов промтов
"""

import pytest
import logging
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.core.prompts import PromptTemplate, PromptType

logger = logging.getLogger("test_prompts_api")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

client = TestClient(app)

def setup_module(module):
    logger.info("=== НАЧАЛО ТЕСТОВ: test_prompts_api.py ===")

def teardown_module(module):
    logger.info("=== ОКОНЧАНИЕ ТЕСТОВ: test_prompts_api.py ===")

def log_test_start(test_name, **kwargs):
    logger.info(f"ТЕСТ: {test_name} | СТАРТ | ВХОД: {kwargs}")

def log_test_end(test_name, duration, result="успешно"):
    logger.info(f"ТЕСТ: {test_name} | ЗАВЕРШЕНИЕ | РЕЗУЛЬТАТ: {result} | Время: {duration:.3f} сек")

@pytest.fixture
def override_prompt_manager():
    mock_manager = MagicMock()
    app.dependency_overrides = { }
    app.dependency_overrides.clear()
    app.dependency_overrides["app.api.api_v1.endpoints.prompts.get_prompt_manager"] = lambda: mock_manager
    yield mock_manager
    app.dependency_overrides = {}

class TestPromptsAPI:
    """Тесты для API эндпоинтов промтов"""
    
    def test_list_prompts(self, override_prompt_manager):
        """Тест получения списка промтов"""
        test_name = "test_list_prompts"
        log_test_start(test_name)
        start = time.time()
        # Подготавливаем тестовые данные
        test_prompts = {
            "topic_extraction_v1": {
                "name": "Извлечение тематик v1",
                "description": "Стандартный промт",
                "type": "topic_extraction",
                "version": "1.0",
                "is_active": True,
                "parameters": ["conversation_text"]
            }
        }
        override_prompt_manager.list_prompts.return_value = test_prompts
        
        response = client.get("/api/v1/prompts/")
        
        try:
            assert response.status_code == 200
            data = response.json()
            assert "topic_extraction_v1" in data
            assert data["topic_extraction_v1"]["name"] == "Извлечение тематик v1"
            log_test_end(test_name, time.time()-start)
        except AssertionError as e:
            logger.error(f"ТЕСТ: {test_name} | ОШИБКА | {e}")
            raise
    
    def test_get_prompt_types(self):
        """Тест получения типов промтов"""
        response = client.get("/api/v1/prompts/types")
        
        assert response.status_code == 200
        data = response.json()
        assert "topic_extraction" in data
        assert "product_analysis" in data
        assert "sentiment_analysis" in data
        assert "benchmark" in data
        assert "custom" in data
        logger.info("Проверка получения типов промтов через API — успешно")
    
    def test_get_prompts_by_type(self, override_prompt_manager):
        """Тест получения промтов по типу"""
        # Подготавливаем тестовые данные
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Шаблон {param}",
            parameters=["param"],
            version="1.0"
        )
        
        override_prompt_manager.prompts = {
            "test_prompt": test_prompt
        }
        override_prompt_manager.get_prompts_by_type.return_value = [test_prompt]
        
        response = client.get("/api/v1/prompts/type/topic_extraction")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["name"] == "Тестовый промт"
        logger.info("Проверка получения промтов по типу через API — успешно")
    
    def test_get_prompts_by_invalid_type(self):
        """Тест получения промтов по неверному типу"""
        response = client.get("/api/v1/prompts/type/invalid_type")
        
        assert response.status_code == 400
        data = response.json()
        assert "Неизвестный тип промта" in data["detail"]
        logger.info("Проверка ошибки при запросе промтов по несуществующему типу через API — успешно")
    
    def test_get_prompt_by_id(self, override_prompt_manager):
        """Тест получения промта по ID"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Шаблон {param}",
            parameters=["param"],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = test_prompt
        
        response = client.get("/api/v1/prompts/test_prompt")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Тестовый промт"
        assert data["prompt_type"] == "topic_extraction"
        logger.info("Проверка получения промта по ID через API — успешно")
    
    def test_get_nonexistent_prompt(self, override_prompt_manager):
        """Тест получения несуществующего промта"""
        override_prompt_manager.get_prompt.return_value = None
        
        response = client.get("/api/v1/prompts/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "не найден" in data["detail"]
        logger.info("Проверка ошибки при запросе несуществующего промта через API — успешно")
    
    def test_create_prompt(self, override_prompt_manager):
        """Тест создания нового промта"""
        # Подготавливаем тестовые данные
        test_prompt = PromptTemplate(
            name="Новый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон {param}",
            parameters=["param"],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = None  # Промт не существует
        override_prompt_manager.add_prompt.return_value = None
        
        request_data = {
            "name": "Новый промт",
            "description": "Описание",
            "prompt_type": "custom",
            "template": "Шаблон {param}",
            "parameters": ["param"],
            "version": "1.0",
            "metadata": {}
        }
        
        response = client.post("/api/v1/prompts/", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Новый промт"
        assert data["prompt_type"] == "custom"
        logger.info("Проверка создания нового промта через API — успешно")
    
    def test_create_prompt_missing_required_fields(self):
        """Тест создания промта с отсутствующими обязательными полями"""
        request_data = {
            "name": "Неполный промт",
            "description": "Описание"
            # Отсутствуют обязательные поля prompt_type и template
        }
        
        response = client.post("/api/v1/prompts/", json=request_data)
        
        assert response.status_code == 422  # Validation error
        logger.info("Проверка ошибки при создании промта с отсутствующими обязательными полями через API — успешно")
    
    def test_create_prompt_already_exists(self, override_prompt_manager):
        """Тест создания промта, который уже существует"""
        existing_prompt = PromptTemplate(
            name="Существующий промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = existing_prompt
        
        request_data = {
            "name": "Существующий промт",
            "description": "Описание",
            "prompt_type": "custom",
            "template": "Шаблон",
            "parameters": [],
            "version": "1.0",
            "metadata": {}
        }
        
        response = client.post("/api/v1/prompts/", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "уже существует" in data["detail"]
        logger.info("Проверка ошибки при создании уже существующего промта через API — успешно")
    
    def test_update_prompt(self, override_prompt_manager):
        """Тест обновления промта"""
        existing_prompt = PromptTemplate(
            name="Обновляемый промт",
            description="Старое описание",
            prompt_type=PromptType.CUSTOM,
            template="Старый шаблон",
            parameters=[],
            version="1.0"
        )
        
        updated_prompt = PromptTemplate(
            name="Обновленный промт",
            description="Новое описание",
            prompt_type=PromptType.CUSTOM,
            template="Новый шаблон",
            parameters=["param"],
            version="1.1"
        )
        
        override_prompt_manager.get_prompt.side_effect = [existing_prompt, updated_prompt]
        override_prompt_manager.update_prompt.return_value = None
        
        request_data = {
            "name": "Обновленный промт",
            "description": "Новое описание",
            "template": "Новый шаблон",
            "parameters": ["param"],
            "version": "1.1"
        }
        
        response = client.put("/api/v1/prompts/test_prompt", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Обновленный промт"
        assert data["description"] == "Новое описание"
        assert data["version"] == "1.1"
        logger.info("Проверка обновления промта через API — успешно")
    
    def test_update_nonexistent_prompt(self, override_prompt_manager):
        """Тест обновления несуществующего промта"""
        override_prompt_manager.get_prompt.return_value = None
        
        request_data = {
            "name": "Обновленный промт",
            "description": "Новое описание"
        }
        
        response = client.put("/api/v1/prompts/nonexistent", json=request_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "не найден" in data["detail"]
        logger.info("Проверка ошибки при обновлении несуществующего промта через API — успешно")
    
    def test_delete_prompt(self, override_prompt_manager):
        """Тест удаления промта"""
        existing_prompt = PromptTemplate(
            name="Удаляемый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = existing_prompt
        override_prompt_manager.delete_prompt.return_value = None
        
        response = client.delete("/api/v1/prompts/test_prompt")
        
        assert response.status_code == 200
        data = response.json()
        assert "успешно удален" in data["message"]
        logger.info("Проверка удаления промта через API — успешно")
    
    def test_delete_standard_prompt_fails(self, override_prompt_manager):
        """Тест удаления стандартного промта (должно завершиться ошибкой)"""
        standard_prompt = PromptTemplate(
            name="Стандартный промт",
            description="Описание",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = standard_prompt
        override_prompt_manager.delete_prompt.side_effect = ValueError("Нельзя удалить стандартный промт")
        
        response = client.delete("/api/v1/prompts/topic_extraction_v1")
        
        assert response.status_code == 400
        data = response.json()
        assert "Нельзя удалить стандартный промт" in data["detail"]
        logger.info("Проверка ошибки при удалении стандартного промта через API — успешно")
    
    def test_format_prompt(self, override_prompt_manager):
        """Тест форматирования промта"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Анализируй: {conversation_text}",
            parameters=["conversation_text"],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = test_prompt
        override_prompt_manager.format_prompt.return_value = "Анализируй: Тестовый разговор"
        
        parameters = {"conversation_text": "Тестовый разговор"}
        
        response = client.post("/api/v1/prompts/test_prompt/format", json=parameters)
        
        assert response.status_code == 200
        data = response.json()
        assert data["formatted_prompt"] == "Анализируй: Тестовый разговор"
        logger.info("Проверка форматирования промта через API — успешно")
    
    def test_format_prompt_missing_parameter(self, override_prompt_manager):
        """Тест форматирования промта с отсутствующим параметром"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.TOPIC_EXTRACTION,
            template="Анализируй: {conversation_text}",
            parameters=["conversation_text"],
            version="1.0"
        )
        
        override_prompt_manager.get_prompt.return_value = test_prompt
        override_prompt_manager.format_prompt.side_effect = ValueError("Отсутствует обязательный параметр: conversation_text")
        
        parameters = {}  # Пустые параметры
        
        response = client.post("/api/v1/prompts/test_prompt/format", json=parameters)
        
        assert response.status_code == 400
        data = response.json()
        assert "Отсутствует обязательный параметр" in data["detail"]
        logger.info("Проверка ошибки при форматировании промта с отсутствующим параметром через API — успешно")
    
    def test_activate_prompt(self, override_prompt_manager):
        """Тест активации промта"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0",
            is_active=False
        )
        
        override_prompt_manager.get_prompt.return_value = test_prompt
        override_prompt_manager.update_prompt.return_value = None
        
        response = client.post("/api/v1/prompts/test_prompt/activate")
        
        assert response.status_code == 200
        data = response.json()
        assert "активирован" in data["message"]
        logger.info("Проверка активации промта через API — успешно")
    
    def test_deactivate_prompt(self, override_prompt_manager):
        """Тест деактивации промта"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0",
            is_active=True
        )
        
        override_prompt_manager.get_prompt.return_value = test_prompt
        override_prompt_manager.update_prompt.return_value = None
        
        response = client.post("/api/v1/prompts/test_prompt/deactivate")
        
        assert response.status_code == 200
        data = response.json()
        assert "деактивирован" in data["message"]
        logger.info("Проверка деактивации промта через API — успешно")


class TestPromptsAPIErrorHandling:
    """Тесты обработки ошибок в API промтов"""
    
    @pytest.fixture
    def mock_prompt_manager_error(self):
        """Мок менеджера промтов с ошибками"""
        with patch('app.api.api_v1.endpoints.prompts.get_prompt_manager') as mock:
            manager = MagicMock()
            mock.return_value = manager
            yield manager
    
    def test_list_prompts_error(self, mock_prompt_manager_error):
        """Тест ошибки при получении списка промтов"""
        mock_prompt_manager_error.list_prompts.side_effect = Exception("Ошибка базы данных")
        
        response = client.get("/api/v1/prompts/")
        
        assert response.status_code == 500
        data = response.json()
        assert "Ошибка получения списка промтов" in data["detail"]
    
    def test_get_prompt_error(self, mock_prompt_manager_error):
        """Тест ошибки при получении промта"""
        mock_prompt_manager_error.get_prompt.side_effect = Exception("Ошибка доступа к файлу")
        
        response = client.get("/api/v1/prompts/test_prompt")
        
        assert response.status_code == 500
        data = response.json()
        assert "Ошибка получения промта" in data["detail"]
    
    def test_create_prompt_error(self, mock_prompt_manager_error):
        """Тест ошибки при создании промта"""
        mock_prompt_manager_error.get_prompt.return_value = None
        mock_prompt_manager_error.add_prompt.side_effect = Exception("Ошибка сохранения")
        
        request_data = {
            "name": "Новый промт",
            "description": "Описание",
            "prompt_type": "custom",
            "template": "Шаблон",
            "parameters": [],
            "version": "1.0",
            "metadata": {}
        }
        
        response = client.post("/api/v1/prompts/", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "Ошибка создания промта" in data["detail"]
    
    def test_update_prompt_error(self, mock_prompt_manager_error):
        """Тест ошибки при обновлении промта"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        
        mock_prompt_manager_error.get_prompt.return_value = test_prompt
        mock_prompt_manager_error.update_prompt.side_effect = Exception("Ошибка обновления")
        
        request_data = {
            "name": "Обновленный промт",
            "description": "Новое описание"
        }
        
        response = client.put("/api/v1/prompts/test_prompt", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "Ошибка обновления промта" in data["detail"]
    
    def test_delete_prompt_error(self, mock_prompt_manager_error):
        """Тест ошибки при удалении промта"""
        test_prompt = PromptTemplate(
            name="Тестовый промт",
            description="Описание",
            prompt_type=PromptType.CUSTOM,
            template="Шаблон",
            parameters=[],
            version="1.0"
        )
        
        mock_prompt_manager_error.get_prompt.return_value = test_prompt
        mock_prompt_manager_error.delete_prompt.side_effect = Exception("Ошибка удаления")
        
        response = client.delete("/api/v1/prompts/test_prompt")
        
        assert response.status_code == 500
        data = response.json()
        assert "Ошибка удаления промта" in data["detail"] 