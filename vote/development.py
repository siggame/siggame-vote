
from vote.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_DIR, "db", "development.db")
    }
}
