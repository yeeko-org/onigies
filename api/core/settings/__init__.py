import os
from django.core.exceptions import ImproperlyConfigured
from core.settings.get_env import getenv_bool, getenv_list
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = getenv_list("ALLOWED_HOSTS", ["*"])

_CSRF_TRUSTED_ORIGINS = getenv_list("CSRF_TRUSTED_ORIGINS")
if _CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = _CSRF_TRUSTED_ORIGINS

# Allowlist de CORS (task-24): el puente UNAM, Netlify y el dev local.
# CORS_ALLOW_ALL_ORIGINS=True en el .env reabre todo (solo para dev).
CORS_ALLOW_ALL_ORIGINS = getenv_bool("CORS_ALLOW_ALL_ORIGINS", False)
CORS_ALLOWED_ORIGINS = getenv_list("CORS_ALLOWED_ORIGINS", [
    "https://onigies.unam.mx",
    "https://onigies.netlify.app",
    "https://localhost:3018",
    "http://localhost:3018",
])
USE_X_FORWARDED_HOST = getenv_bool("USE_X_FORWARDED_HOST", True)
HTTP_X_FORWARDED_HOST = os.getenv("HTTP_X_FORWARDED_HOST")

# Endurecimiento (task-24). El nginx de Yeeko termina TLS y manda
# X-Forwarded-Proto; sin este header confiado, is_secure() es False
# detrás del proxy y ni cookies Secure ni HSTS se emiten.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = getenv_bool("SECURE_COOKIES", not DEBUG)
CSRF_COOKIE_SECURE = getenv_bool("SECURE_COOKIES", not DEBUG)
# 0 = sin HSTS; producción lo fija en el .env. No se activa
# SECURE_SSL_REDIRECT: la redirección http→https ya la hace nginx.
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))

FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',

    'ies',
    'example',
    'indicator',
    'question',
    'survey',
    'answer',
    'ps_schema',
    'email_send',
    'flow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'ies.User'


POSTGRESQL_DB = getenv_bool('POSTGRESQL_DB', False)
DATABASE_NAME = os.getenv("DATABASE_NAME", "db.sqlite3")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")

if POSTGRESQL_DB:

    INSTALLED_APPS += ("django.contrib.postgres",)
    

    default_database = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': int(os.getenv("DATABASE_PORT", 5432)),
    }
else:

    default_database = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, DATABASE_NAME)
    }

# Only apply schema options for PostgreSQL
if DATABASE_SCHEMA and POSTGRESQL_DB:
    default_database['OPTIONS'] = {  # type: ignore
        'options': f'-c search_path={DATABASE_SCHEMA}',
    }

DATABASES = {
    "default": default_database
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'SEARCH_PARAM': 'q',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

}


# Seams configurables del registry de ps_schema (ver ps_schema/registry.py).
# Resueltos vía import_string; desacoplan la mecánica de catálogos del
# proyecto concreto. Los catálogos de onigies no tienen status_validation,
# por eso el base por defecto es "generic" (no "status").
PS_SCHEMA = {
    "BASE_VIEWSETS": {
        "status": "api.views.common_views.BaseStatusViewSet",
        "generic": "api.views.common_views.BaseGenericViewSet",
        "viewset": "rest_framework.viewsets.ModelViewSet",
    },
    "PERMISSIONS": {
        "editor": "api.permissions.IsFullEditorOrReadOnly",
        "admin": "api.permissions.IsAdminOrReadOnly",
        "any": "rest_framework.permissions.AllowAny",
    },
    "DEFAULT_CATALOG_BASE": "generic",
    "DEFAULT_CATALOG_PERMISSION": "editor",
}


# ---------------------------------STORAGE-----------------------------------
COMPRESS_ENABLED = getenv_bool("COMPRESS_ENABLED", True)
COMPRESS_OFFLINE = getenv_bool("COMPRESS_OFFLINE", True)

# Los estáticos (admin, DRF) siempre son locales: los sirve nginx o
# WhiteNoise. Solo los archivos subidos pueden migrar a S3.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Puente temporal a un bucket privado de S3 mientras llega el servidor
# de la UNAM. Apagado por defecto: en local los archivos siguen en disco.
USE_S3_FILES = getenv_bool('USE_S3_FILES', False)

# Siempre definido, incluso con S3 encendido: es el origen de la
# migración de archivos y el respaldo en disco del servidor.
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')

if USE_S3_FILES:
    INSTALLED_APPS += ("storages",)

    _s3_bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
    _s3_region = os.getenv('AWS_S3_REGION_NAME')
    _s3_location = os.getenv('AWS_LOCATION', 'files')
    # Sin región no hay firma válida y sin bucket no hay a dónde
    # escribir: mejor reventar al arrancar que servir 404s o 307s.
    if not _s3_bucket or not _s3_region:
        raise ImproperlyConfigured(
            "USE_S3_FILES exige AWS_STORAGE_BUCKET_NAME y "
            "AWS_S3_REGION_NAME en el entorno.")
    _s3_domain = f'{_s3_bucket}.s3.{_s3_region}.amazonaws.com'

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": _s3_bucket,
                "region_name": _s3_region,
                # NO agregar custom_domain: en django-storages 1.14
                # activa una rama de url() que devuelve la URL SIN
                # firmar, y el bucket es privado.
                # Sin signature_version explícita botocore presigna con
                # SigV2, que los buckets nuevos ya no aceptan; sin
                # addressing_style el host pierde la región
                # (bucket.s3.amazonaws.com) y S3 contesta 307.
                "signature_version": "s3v4",
                "addressing_style": "virtual",
                "location": _s3_location,
                # Explícitas para no caer en silencio al perfil de la
                # instancia EC2 si el .env viene mal: el acceso al
                # bucket es de un usuario IAM acotado.
                "access_key": os.getenv('AWS_ACCESS_KEY_ID'),
                "secret_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
                # El bucket tiene las ACL deshabilitadas.
                "default_acl": None,
                # Bucket privado: file.url devuelve una URL firmada.
                "querystring_auth": True,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.StaticFilesStorage"),
        },
    }
    # Absoluta a propósito: el guard de core/urls.py apaga la ruta
    # abierta /files/ en cuanto MEDIA_URL trae esquema.
    MEDIA_URL = f'https://{_s3_domain}/{_s3_location}/'
else:
    MEDIA_URL = '/files/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'files')


# -------------------------------END STORAGE---------------------------------

# ------------------------------- MEDIA -------------------------------------

# STATIC_URL = 'static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# STATIC_PATH = os.path.join(BASE_DIR, os.getenv("STATIC_PATH", 'static'))
# MEDIA_PATH = os.path.join(BASE_DIR, os.getenv("MEDIA_PATH", 'media'))

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------END MEDIA------------------------------------
