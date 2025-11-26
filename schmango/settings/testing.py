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
CSRF_TRUSTED_ORIGINS = ["http://localhost"]

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
    "DEFAULT_THROTTLE_RATES": {},
}

# Configure logging to capture errors
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/var/log/yadalist/django.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
