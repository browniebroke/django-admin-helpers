from __future__ import annotations

SECRET_KEY = "NOTASECRET"  # noqa S105

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": True,
    },
}

USE_TZ = True
TIME_ZONE = "UTC"
ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django_admin_helpers",
    "testapp",
]
