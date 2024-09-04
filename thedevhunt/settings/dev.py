from .base import *

DEBUG = True

INSTALLED_APPS = [
    *INSTALLED_APPS,
    'django_browser_reload',
]

MIDDLEWARE = [
    *MIDDLEWARE,
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]