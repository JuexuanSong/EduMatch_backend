from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*acq0w4v-oz!1t31d7+z4c@sn741zt@5u9s$cx$%)6cld^8df5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # For PostGIS support
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'social_django',  # For social authentication
    'users',
    'skills',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'edumatch_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'edumatch_backend.wsgi.application'

# Custom User Model - Add this line
AUTH_USER_MODEL = 'users.User'

# Database with PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'edumatch_db',
        'USER': 'zhenting',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# GeoDjango settings - Auto-detect library paths
import subprocess
import glob

def find_library_path(lib_name):
    """Find library path using multiple methods"""
    # Method 1: Check common Homebrew paths
    for prefix in ['/opt/homebrew', '/usr/local']:
        pattern = f"{prefix}/lib/{lib_name}*.dylib"
        libs = glob.glob(pattern)
        if libs:
            return libs[0]
    
    # Method 2: Use find command
    try:
        result = subprocess.run(['find', '/usr/local', '/opt/homebrew', '-name', f'{lib_name}*.dylib'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None

# Try to auto-detect library paths
gdal_path = find_library_path('libgdal')
geos_path = find_library_path('libgeos_c')

if gdal_path:
    GDAL_LIBRARY_PATH = gdal_path
    print(f"Found GDAL at: {gdal_path}")

if geos_path:
    GEOS_LIBRARY_PATH = geos_path
    print(f"Found GEOS at: {geos_path}")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

}

# Social Auth settings
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-google-client-id'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-google-client-secret'
SOCIAL_AUTH_FACEBOOK_KEY = 'your-facebook-app-id'
SOCIAL_AUTH_FACEBOOK_SECRET = 'your-facebook-app-secret'

# CORS settings - Allow all origins for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.0.2.2:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Email settings for password reset
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
