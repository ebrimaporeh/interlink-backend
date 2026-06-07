import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .base import *

# Set DEBUG=True in Render env vars only when debugging — never leave it on
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# '*' works safely behind Render/Cloudflare proxy; set ALLOWED_HOSTS env var to
# restrict to specific domains once the app is stable
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '*').split(',') if h.strip()]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ── Database ──────────────────────────────────────────────────────────────────
_DATABASE_URL = os.environ.get('DATABASE_URL', '')
if not _DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL environment variable is not set. "
        "Set it in Render's Environment Variables panel."
    )
DATABASES = {'default': dj_database_url.config(default=_DATABASE_URL, conn_max_age=600, ssl_require=True)}

# ── CORS ─────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGIN_REGEXES = [r'^https://.*\.vercel\.app$']
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# ── Supabase S3 storage ───────────────────────────────────────────────────────
_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME', 'media')
_PROJECT = 'flebrclfzzleupwbligo'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = _BUCKET
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-north-1')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_VERIFY = True
AWS_S3_CUSTOM_DOMAIN = f'{_PROJECT}.supabase.co/storage/v1/object/public/{_BUCKET}'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

STORAGES = {
    'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
