import os
import dj_database_url
from corsheaders.defaults import default_headers

# ================================
# BASIC SETTINGS
# ================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]


# ================================
# INSTALLED APPS
# ================================
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'payouts',
]


# ================================
# MIDDLEWARE (ORDER IMPORTANT)
# ================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# ================================
# DATABASE (LOCAL + RENDER)
# ================================
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL)
    }
else:
    # Local fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'playto',
            'USER': 'postgres',
            'PASSWORD': 'Karthik1563',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ================================
# URL CONFIG
# ================================
ROOT_URLCONF = 'config.urls'


# ================================
# STATIC FILES
# ================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')


# ================================
# DEFAULT FIELD
# ================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================================
# CORS (FRONTEND CONNECTION)
# ================================
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "idempotency-key",
]


# ================================
# CELERY (LOCAL + RENDER)
# ================================
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://127.0.0.1:6379/0"
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = None
