# -*- coding: utf-8 -*-
"""
Banking NLP System - Основное приложение с автоматической генерацией данных
"""
import asyncio
import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .core.config import get_settings
from .api.routes import router as api_router
from .utils.data_initializer import DataInitializer
from src.banking_nlp.core.logging_config import setup_logging

# Настройка централизованного логирования
setup_logging(log_level="INFO", log_file="logs/app.log")
import logging
logger = logging.getLogger(__name__)

# Создаем экземпляр приложения
app = FastAPI(
    title="Banking NLP System",
    description="Система анализа банковских разговоров с автоматической генерацией данных",
    version="1.0.0",
)

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Инициализатор данных
data_initializer = DataInitializer()

@app.on_event("startup")
async def startup_event():
    logger.info("🏦 Banking NLP System - Инициализация данных...")
    await data_initializer.ensure_data_available()
    logger.info("✅ Данные готовы к использованию!")

# Красивая форма на главной странице
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Подключение маршрутов API
app.include_router(api_router, prefix="/api", tags=["analysis"])

def main():
    settings = get_settings()
    logger.info(f"🚀 Запуск Banking NLP System на {settings.host}:{settings.port}")
    uvicorn.run(
        "src.banking_nlp.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

if __name__ == "__main__":
    main()


