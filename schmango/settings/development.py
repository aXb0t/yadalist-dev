"""
Development settings - used for local development with docker-compose.
"""
import os
import dj_database_url
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database - PostgreSQL via docker-compose
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://schmango:development_password@db:5432/schmango"
    )
}

# Security settings - relaxed for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = "csrftoken"

# No HSTS in development
SECURE_HSTS_SECONDS = 0

# Always-on security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# Static files - use volume-mounted frontend/dist in development
STATICFILES_DIRS = []
if (BASE_DIR / "frontend" / "dist").exists():
    STATICFILES_DIRS = [BASE_DIR / "frontend" / "dist"]
