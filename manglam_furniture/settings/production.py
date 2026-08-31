import dj_database_url

from .base import *

DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="dev-only-change-me")
ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="localhost,127.0.0.1,.vercel.app,.now.sh").split(",")
    if host.strip()
]
DATABASE_URL = config("DATABASE_URL", default="sqlite:///db.sqlite3")
DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

if config("AWS_STORAGE_BUCKET_NAME", default=""):
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default=None)
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False