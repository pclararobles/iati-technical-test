import os

from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

STACK = "dev"

# STATIC
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [root("static")]
MEDIA_ROOT = root("tmp")
MEDIA_URL = "/tmp/"

# SHELL_PLUS
SHELL_PLUS = "ipython"
