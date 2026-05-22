DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
]

LOCAL_APPS = [
    "apps.users",
    "apps.products",
    "apps.orders",
    "apps.payments",
    "apps.reviews",
    "apps.notifications",
    "apps.core",
    "apps.cart",
]