DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fulldeck',
        }
}
INTERNAL_IPS = ("127.0.0.1", "10.0.2.2")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "tmp/django_cache",
    }
}

COMPRESS_ENABLED = True