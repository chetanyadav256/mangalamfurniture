from .base import *


DEBUG = True
SECRET_KEY = config("SECRET_KEY", default="django-dev-insecure-key")