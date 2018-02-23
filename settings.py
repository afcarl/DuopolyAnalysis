import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# example) SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}

# example) MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

INSTALLED_APPS = (
    'game',
)

SECRET_KEY = 'REPLACE_ME'

DEBUG = True
# TIME_ZONE = "Europe/Paris"
# USE_TZ = True
