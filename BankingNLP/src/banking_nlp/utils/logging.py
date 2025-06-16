"""
Система логирования для банковского NLP проекта
"""
import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

class BankingNLPLogger:
    """Настройка логирования для банковского NLP проекта"""
    
    def __init__(self, 
                 log_level: int = logging.INFO,
                 log_file: Optional[str] = None,
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        
        self.log_level = log_level
        self.log_file = log_file or self._get_default_log_file()
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        self._setup_logging()
    
    def _get_default_log_file(self) -> str:
        """Создание пути к файлу логов по умолчанию"""
        project_root = Path(__file__).parent.parent
        logs_dir = project_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        return str(logs_dir / f"banking_nlp_{timestamp}.log")
    
    def _setup_logging(self) -> None:
        """Настройка системы логирования"""
        # Создание форматтера
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Настройка root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Очистка существующих handlers
        root_logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler с ротацией
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Специальный logger для аудита работы с данными
        audit_logger = logging.getLogger('banking_nlp.audit')
        audit_handler = logging.handlers.RotatingFileHandler(
            str(Path(self.log_file).parent / "audit.log"),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        audit_handler.setFormatter(audit_formatter)
        audit_logger.addHandler(audit_handler)
        audit_logger.setLevel(logging.INFO)
        audit_logger.propagate = False

def get_logger(name: str) -> logging.Logger:
    """Получение logger с указанным именем"""
    return logging.getLogger(name)

def log_data_operation(operation: str, file_path: str, record_count: int = 0) -> None:
    """Логирование операций с данными для аудита"""
    audit_logger = logging.getLogger('banking_nlp.audit')
    audit_logger.info(f"OPERATION: {operation}, FILE: {file_path}, RECORDS: {record_count}")

# Инициализация логирования при импорте модуля
banking_logger = BankingNLPLogger()
