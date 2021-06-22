import os
from datetime import timedelta
from rest_framework.settings import api_settings
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wkpwid&=r9wp2nl9jyr_%66zjgq4fku9*%g%^%-4iijga+t2lg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'material',
    # 'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'authy',
    'post',
    'comment',
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'knox',
    'djrichtextfield',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'blog.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = '/login/'


CORS_ORIGIN_WHITELIST = [
    'https://gutsnbraces.herokuapp.com',
    'https://gutsnbraces.firebaseapp.com',
    'https://gutsnbraces.web.app',
    'http://gutsnbraces.com',
    'https://gutsnbraces.com'
]
CORS_ALLOW_CREDENTIALS = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ]
}

CORS_ORIGIN_ALLOW_ALL = False


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# AUTHENTICATION_BACKENDS = [
#     'social_core.backends.linkedin.LinkedinOAuth2',
#     'social_core.backends.instagram.InstagramOAuth2',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# ]


# SOCIAL_AUTH_FACEBOOK_KEY = '208657714439748'        # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = '801da49d5c3b821a81eb7e703b1a7b6a'  # App Secret
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']  # add this
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
#     'fields': 'id, name, email, picture.type(large), link'
# }
# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
#     ('name', 'name'),
#     ('email', 'email'),
#     ('picture', 'picture'),
#     ('link', 'profile_url'),
# ]


# id =857600629318-uub686dfm4o6dl1ugg4irul6agvu1k37.apps.googleusercontent.com
# secret =HrIyPkirqhaHmPr7C5Ee_H4s


REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 50,
    'TOKEN_TTL': timedelta(days=30),
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': 1,
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}


DJRICHTEXTFIELD_CONFIG = {
    'js': ['//cdn.ckeditor.com/4.14.0/standard/ckeditor.js'],
    'init_template': 'djrichtextfield/init/ckeditor.js',
    'settings': {  # CKEditor
        'toolbar': [
            {'items': ['Format', '-', 'Bold', 'Italic', '-',
                       'RemoveFormat']},
            {'items': ['Link', 'Unlink', 'Image', 'Table']},
            {'items': ['Source']}
        ],
        'format_tags': 'p;h1;h2;h3',
        'width': 700
    }
}
# DJRICHTEXTFIELD_CONFIG = {
#     'js': ['//cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js'],
#     'init_template': 'djrichtextfield/init/tinymce.js',
#     'settings': {
#         'menubar': False,
#         'plugins': 'link image',
#         'toolbar': 'bold italic | link image | removeformat',
#         'width': 700
#     }
# }


# db = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db)
