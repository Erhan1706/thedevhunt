from .base import *

DEBUG = True

ADMIN_ENABLED = True

INSTALLED_APPS = [
    *INSTALLED_APPS,
    'django_browser_reload',
]

MIDDLEWARE = [
    *MIDDLEWARE,
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]