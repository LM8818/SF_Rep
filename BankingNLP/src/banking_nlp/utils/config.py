"""
Система конфигурации для банковского NLP проекта
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class Config:
    """Класс для управления конфигурацией проекта"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.project_root = Path(__file__).parent.parent
        self.config_path = config_path or self.project_root / "configs" / "base_config.yaml"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из YAML файла"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            # Обновление путей относительно корня проекта
            self._update_paths(config)
            return config
        except FileNotFoundError:
            logging.warning(f"Файл конфигурации {self.config_path} не найден. Используется конфигурация по умолчанию.")
            return self._default_config()
    
    def _update_paths(self, config: Dict[str, Any]) -> None:
        """Обновление путей в конфигурации относительно корня проекта"""
        if 'data' in config:
            for key, path in config['data'].items():
                if isinstance(path, str) and not os.path.isabs(path):
                    config['data'][key] = str(self.project_root / path)
    
    def _default_config(self) -> Dict[str, Any]:
        """Конфигурация по умолчанию"""
        return {
            'data': {
                'raw_data_path': str(self.project_root / 'data' / 'raw'),
                'processed_data_path': str(self.project_root / 'data' / 'processed'),
                'synthetic_data_path': str(self.project_root / 'data' / 'synthetic'),
            },
            'model': {
                'max_sequence_length': 512,
                'batch_size': 32,
                'learning_rate': 2e-5,
                'num_epochs': 3,
                'random_seed': 42
            },
            'banking': {
                'topics': [
                    'кредиты', 'депозиты', 'карты', 'переводы', 'инвестиции',
                    'страхование', 'ипотека', 'автокредит', 'потребительский_кредит',
                    'интернет_банк', 'мобильное_приложение', 'техподдержка'
                ],
                'products': [
                    'дебетовая_карта', 'кредитная_карта', 'срочный_депозит',
                    'накопительный_счет', 'потребительский_кредит', 'ипотека',
                    'автокредит', 'рефинансирование', 'овердрафт'
                ]
            },
            'preprocessing': {
                'remove_urls': True,
                'remove_emails': True,
                'remove_phones': True,
                'normalize_whitespace': True,
                'min_text_length': 10,
                'max_text_length': 2048
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Получение значения по пути ключа (например: 'data.raw_data_path')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """Установка значения по пути ключа"""
        keys = key_path.split('.')
        config_ref = self.config
        
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
            
        config_ref[keys[-1]] = value

# Глобальный экземпляр конфигурации
config = Config()
