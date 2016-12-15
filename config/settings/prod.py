from .base import *

env_file = str(PROJECT_ROOT.path('security/environ_prod.env'))
environ.Env.read_env(str(env_file))

DEBUG = env.bool('DEBUG_PROD')
ALLOWED_HOSTS = ["*"]

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader',
     TEMPLATES[0]['OPTIONS']['loaders']),
]

# DATABASES = {
#     'default': env.db("DATABASE_URL_PROD"),
# }

DATABASES = {
    'default': env.db("SQLITE_URL_PROD"),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 10

DJANGO_APPS = (
)
THIRD_PARTY_APPS = (

)
LOCAL_APPS = (

)
INSTALLED_APPS += DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

ADMIN_URL = env('ADMIN_URL_PROD')

EMAIL_CONFIG = env.email_url('EMAIL_URL_PROD')
vars().update(EMAIL_CONFIG)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
