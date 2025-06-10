# -*- coding: utf-8 -*-
"""
Модуль автоматической инициализации данных для Banking NLP System
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
from ..utils.data_generator import BankingDataGenerator

import logging
logger = logging.getLogger(__name__)

class DataInitializer:
    """Класс для автоматической инициализации и управления данными"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.processed_dir = self.data_dir / "processed"
        self.raw_dir = self.data_dir / "raw"
        self.conversations_file = self.processed_dir / "conversations_processed.csv"
        self.metadata_file = self.processed_dir / "data_metadata.json"
        
    async def ensure_data_available(self) -> bool:
        """Обеспечивает наличие данных, генерируя их при необходимости"""
        
        # Проверяем существование основного файла данных
        if self.conversations_file.exists():
            logger.info("📊 Найдены существующие данные: {self.conversations_file}")
            
            # Проверяем актуальность данных
            if await self._is_data_fresh():
                logger.info("✅ Данные актуальны, генерация не требуется")
                return True
            else:
                logger.info("🔄 Данные устарели, обновляем...")
        else:
            logger.info("📂 CSV данные не найдены, запускаем автоматическую генерацию...")
        
        # Генерируем новые данные
        await self._generate_fresh_data()
        return True
    
    async def _is_data_fresh(self) -> bool:
        """Проверяет актуальность существующих данных"""
        if not self.metadata_file.exists():
            return False
            
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Проверяем, что данные созданы не более 7 дней назад
            creation_date = datetime.fromisoformat(metadata.get('creation_date', ''))
            days_old = (datetime.now() - creation_date).days
            
            return days_old < 7 and metadata.get('conversations_count', 0) >= 500
            
        except (json.JSONDecodeError, ValueError, KeyError):
            return False
    
    async def _generate_fresh_data(self) -> None:
        """Генерирует свежие данные асинхронно"""
        logger.info("🔧 Создание директорий...")
        self._create_directories()
        
        logger.info("🤖 Запуск генератора банковских разговоров...")
        generator = BankingDataGenerator()
        
        # Генерируем данные в отдельном потоке для не блокирования
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, 
            generator.generate_csv_files, 
            1000  # Количество разговоров
        )
        
        # Сохраняем метаданные
        await self._save_metadata(1000)
        
        logger.info("✅ Автоматическая генерация данных завершена!")
    
    def _create_directories(self) -> None:
        """Создает необходимые директории"""
        for directory in [self.data_dir, self.processed_dir, self.raw_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def _save_metadata(self, conversations_count: int) -> None:
        """Сохраняет метаданные о сгенерированных данных"""
        metadata = {
            "creation_date": datetime.now().isoformat(),
            "conversations_count": conversations_count,
            "data_version": "1.0",
            "generator_version": "auto",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    async def get_data_info(self) -> Dict[str, Any]:
        """Возвращает информацию о доступных данных"""
        if not self.conversations_file.exists():
            return {"status": "no_data", "total_conversations": 0}
        
        try:
            # Быстрая загрузка только для подсчета строк
            df = pd.read_csv(self.conversations_file)
            
            metadata = {}
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            return {
                "status": "available",
                "total_conversations": len(df),
                "themes_available": df['theme'].nunique() if 'theme' in df.columns else 0,
                "products_available": df['product'].nunique() if 'product' in df.columns else 0,
                "last_updated": metadata.get("last_updated", "неизвестно"),
                "file_path": str(self.conversations_file)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e), "total_conversations": 0}
    
    async def get_conversations_data(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Возвращает данные разговоров"""
        if not self.conversations_file.exists():
            await self.ensure_data_available()
        
        df = pd.read_csv(self.conversations_file)
        
        if limit:
            return df.head(limit)
        
        return df
