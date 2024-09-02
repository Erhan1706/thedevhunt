import os

# Default to development settings
settings_module = 'thedevhunt.settings.dev'

if os.environ.get('DJANGO_PRODUCTION') == 'True':
    settings_module = 'thedevhunt.settings.prod'

# Import the settings module
from importlib import import_module
globals().update(import_module(settings_module).__dict__)