# settings.py — Central config for the entire Django project.
# Controls installed apps, database connection, middleware order,
# template engine, and every other project-wide setting.

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Never expose this key in production — use an environment variable instead.
SECRET_KEY = 'django-insecure-dev-only-replace-in-production'

DEBUG = True   # Shows detailed error pages locally — always False in prod
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',        # built-in admin panel at /admin/
    'django.contrib.auth',         # authentication framework
    'django.contrib.contenttypes', # tracks model content types
    'django.contrib.sessions',     # session management
    'django.contrib.messages',     # one-time flash messages
    'django.contrib.staticfiles',  # serves static files in dev
    'courses',
    'rest_framework',                     # our Course Management app
]

# Each middleware wraps the request/response — runs top→bottom on request,
# bottom→top on response. Order matters here.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # HTTPS, headers
    'django.contrib.sessions.middleware.SessionMiddleware',   # loads sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',# injects request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # prevents iframe abuse
]

ROOT_URLCONF = 'coursemanager.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'coursemanager.wsgi.application'

# SQLite is fine for local development — zero setup required.
# Swap ENGINE to postgresql and fill in credentials for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS — allows the React frontend (localhost:3000) to make requests to this API.
# CORS headers are enforced by the browser, not the server.
# Add corsheaders to INSTALLED_APPS and MIDDLEWARE to activate.
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
