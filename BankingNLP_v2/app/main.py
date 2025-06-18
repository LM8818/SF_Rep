from fastapi import FastAPI, Depends, HTTPException, status, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, Request 
from fastapi.responses import HTMLResponse
import logging

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.security import JWTBearer

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Banking NLP API",
    description="Система анализа банковских транскриптов с NLP",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# API роутеры
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Banking NLP API v2.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# Шаблоны
templates = Jinja2Templates(directory="frontend/templates")

# Веб-страницы
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def test_forms(request: Request):
    return templates.TemplateResponse("test_forms.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})
