import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv('ALLOWED_HOSTS', '.onrender.com').split(',')
    if h.strip()
]

# Trust Render's reverse proxy for HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Supabase PostgreSQL (via connection pooler)
_DATABASE_URL = os.environ.get('DATABASE_URL', '')
if not _DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL environment variable is not set. "
        "Set it in Render's Environment Variables panel."
    )

_db_config = dj_database_url.config(default=_DATABASE_URL, conn_max_age=600, ssl_require=True)

if _db_config.get('ENGINE') != 'django.db.backends.postgresql':
    raise ImproperlyConfigured(
        f"DATABASE_URL must resolve to a PostgreSQL database. "
        f"Got ENGINE='{_db_config.get('ENGINE', 'empty')}'. "
        f"DATABASE_URL value starts with: '{_DATABASE_URL[:40]}'"
    )

DATABASES = {'default': _db_config}

# CORS — set CORS_ALLOWED_ORIGINS env var to your Vercel/custom frontend URL(s)
CORS_ALLOW_ALL_ORIGINS = False
_cors_default = '.vercel.app'   # covers all *.vercel.app preview/production URLs
CORS_ALLOWED_ORIGIN_REGEXES = [r'^https://.*\.vercel\.app$']
_cors_env = os.getenv('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_env.split(',') if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# ── Supabase S3 Storage ───────────────────────────────────────────
_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME', 'media')
_PROJECT = 'flebrclfzzleupwbligo'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = _BUCKET
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')   # Supabase S3 endpoint
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-north-1')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False    # public URLs, no signed params
AWS_S3_VERIFY = True

# Public URL for uploaded media files
AWS_S3_CUSTOM_DOMAIN = (
    f'{_PROJECT}.supabase.co/storage/v1/object/public/{_BUCKET}'
)
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Static files — Whitenoise serves from STATIC_ROOT.
# Clear STATICFILES_DIRS so collectstatic doesn't warn about the local
# 'static/' directory that doesn't exist on Render.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
