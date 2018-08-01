from .base import *

DEBUG = True

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR,]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'