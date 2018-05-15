import os, socket
from django.contrib.admin.sites import AdminSite

AdminSite.site_header = 'DAL ERP'
AdminSite.site_title = 'DAL ERP'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '_^m0rs47dn9)i2k=2jffso7$=(@2k&#=kd*%q1!f*(4u@c^o+b'

HOSTNAME = socket.gethostname()

if HOSTNAME == 'erp':
    ALLOWED_HOSTS = ['172.16.16.4', '111.221.7.58']
    DEBUG = False
else:
    ALLOWED_HOSTS = ['*']
    DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'celery',
    'wkhtmltopdf',

    'attn',
    'attendance',
    'core',
    'billing',
    'requisition',
    'msgs',
    'inv',
    'ticket',
    'europarts',
]

WKHTMLTOPDF_CMD_OPTIONS = {
    'dpi': 380,
}
WKHTMLTOPDF_CMD = '/usr/local/bin/wkhtmltopdf'


EMAIL_HOST = 'mail.groupdesignace.com'
EMAIL_HOST_USER = 'michel@groupdesignace.com'
EMAIL_HOST_PASSWORD = 'mmii123#'
EMAIL_PORT = 5877
EMAIL_USE_TLS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.now',
            ],
            'libraries': {
                'project_tags': 'utils.templatetags.project_extras',
            },
        },
    },
]

WSGI_APPLICATION = 'erp.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/login/'

AUTH_USER_MODEL = 'auth.User'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

CELERY_BROKER_URL = 'redis://localhost:6379/'
