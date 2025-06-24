#!/usr/bin/env python3

import os
from app.core.config import Settings

print(f"Environment variable API_AUTH_ENABLED: {os.getenv('API_AUTH_ENABLED')}")

# Создаем новый объект настроек
settings = Settings()
print(f"Settings api_auth_enabled: {settings.api_auth_enabled}")
print(f"Settings type: {type(settings.api_auth_enabled)}") 