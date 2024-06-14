from .common import *
from .partials.util import get_secret

DEBUG = True

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = ['localhost', 'http://165.227.70.44']

CSRF_TRUSTED_ORIGINS = [
    'http://165.227.70.44',
]
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
if get_secret('DATABASE_URL'):
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    POSTGRES_USER = get_secret('POSTGRES_USER')
    POSTGRES_PASSWORD = get_secret('POSTGRES_PASSWORD')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'project_name',
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'db',
            'PORT': 5432,
        }
    }



# Email Config
"""
EMAIL_PASSWORD = get_secret('EMAIL_PASSWORD')
EMAIL_HOST = 'smtp.tayra.com'
EMAIL_HOST_USER = 'tayra'
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
"""
