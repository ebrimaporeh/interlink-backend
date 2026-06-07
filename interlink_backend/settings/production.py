import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Trust Render's reverse proxy for HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Supabase PostgreSQL (via connection pooler)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

# CORS — only allow the production frontend domain
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# ── Supabase S3 Storage ───────────────────────────────────────────
_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME', 'interlink-media')
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

# Static files are served by Whitenoise from the collected root
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
