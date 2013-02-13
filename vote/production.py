from vote.settings import *
from secret_settings import *

SIDE_ID = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vote',
        'USER': 'vote_user',
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': 'localhost'
    }
}
