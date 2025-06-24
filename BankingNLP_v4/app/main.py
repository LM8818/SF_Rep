"""
app/main.py
Главная точка входа FastAPI-приложения Banking NLP v2.0.
"""

import logging
import logging.config
import yaml
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.api.api_v1.api import api_router
from app.core.config import settings


# ────────────────────────────
#  Настройка логирования
# ────────────────────────────
def setup_logging() -> None:
    """
    Загружает конфигурацию логирования из logging.yaml.
    При ошибке применяет базовую настройку.
    """
    try:
        # Используем путь относительно текущего файла main.py
        config_path = Path(__file__).parent / "core/config/logging.yaml"
        with open(config_path, encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        logging.config.dictConfig(config)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().warning("Не удалось загрузить logging.yaml – использована базовая конфигурация.")


setup_logging()
logger = logging.getLogger(__name__)

# ────────────────────────────
#  Создание приложения
# ────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ────────────────────────────
#  CORS-middleware
# ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # при необходимости ограничьте домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────
#  Шаблоны и статика
# ────────────────────────────
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# ────────────────────────────
#  HTML-страницы
# ────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    return templates.TemplateResponse("test_forms.html", {"request": request})


@app.get("/test_forms", response_class=HTMLResponse)
async def test_forms(request: Request):
    return templates.TemplateResponse("test_forms.html", {"request": request})


@app.get("/test-new", response_class=HTMLResponse)
async def test_page_new(request: Request):
    return templates.TemplateResponse("test_forms_new.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})


@app.get("/prompts", response_class=HTMLResponse)
async def prompts(request: Request):
    return templates.TemplateResponse("prompts.html", {"request": request, "prompt": None})


# ────────────────────────────
#  Health-check
# ────────────────────────────
@app.get("/health")
async def health():
    return {"status": "healthy", "version": app.version}


# ────────────────────────────
#  API-роутеры
# ────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)
