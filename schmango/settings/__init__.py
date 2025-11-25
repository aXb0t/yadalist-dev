"""
Django settings for schmango project.

Settings are split into:
- base.py: Common settings for all environments
- development.py: Local development settings
- testing.py: CI/test environment settings
- production.py: Production deployment settings

To use a specific settings file, set the DJANGO_SETTINGS_MODULE environment variable:
    export DJANGO_SETTINGS_MODULE=schmango.settings.production
"""
import os

# Default to development settings if not specified
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'schmango.settings.development')

# Import the appropriate settings
if 'production' in settings_module:
    from .production import *
elif 'testing' in settings_module:
    from .testing import *
else:
    from .development import *
