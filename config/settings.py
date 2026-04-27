SECRET_KEY = "test"
DEBUG = True

ALLOWED_HOSTS = ["*"]


# ✅ Installed apps
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',          # REQUIRED
    'django.contrib.messages',          # REQUIRED
    'django.contrib.staticfiles',       # REQUIRED

    'rest_framework',
    'corsheaders',
    'payouts',
]


# ✅ Middleware (ORDER MATTERS)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# ✅ Database
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


# ✅ Templates
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


# ✅ URLs
ROOT_URLCONF = 'config.urls'


# ✅ Static files (needed for DRF UI)
STATIC_URL = '/static/'


# ✅ Default primary key fix (removes warnings)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ✅ CORS (for React frontend)
CORS_ALLOW_ALL_ORIGINS = True

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    "idempotency-key",
]


# ✅ Celery (Redis)
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = None