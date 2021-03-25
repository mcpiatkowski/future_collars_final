from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ['tortura.herokuapp.com', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SECRET_KEY = 'iz5ztn=d=lddscqk9i4ou4hkmrl@yru=a4hh6y@nbj#-t(p@ta'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')