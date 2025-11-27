"""
Testing settings - used for CI/Jenkins tests.
Uses SQLite in-memory database for fast, isolated tests.
"""

from .base import *

DEBUG = False
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable must be set")

# Use SQLite in-memory database for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Minimal security settings for testing
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# Get CSRF trusted origins from env var, default to testing server
import os

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://10.74.74.66"
).split(",")
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF cookie for AJAX requests
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = "csrftoken"

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# No static files collection needed for tests
STATICFILES_DIRS = []

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Rate limiting - disabled for testing (no throttling in unit tests)
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # Inherit from base settings
    "DEFAULT_THROTTLE_CLASSES": [],  # Disable throttling in tests
    "DEFAULT_THROTTLE_RATES": {
        "upload": "1000000/hour",  # High limit so tests don't actually throttle
    },
}
