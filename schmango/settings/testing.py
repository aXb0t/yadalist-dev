"""
Testing settings - used for CI/Jenkins tests.
Uses SQLite in-memory database for fast, isolated tests.
"""
from .base import *

DEBUG = False

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
CSRF_TRUSTED_ORIGINS = ["http://localhost"]

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# No static files collection needed for tests
STATICFILES_DIRS = []

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Rate limiting - disabled for testing (no throttling in unit tests)
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # Inherit from base settings
    'DEFAULT_THROTTLE_CLASSES': [],  # Disable throttling in tests
    'DEFAULT_THROTTLE_RATES': {}
}
