from backend.core.settings.environ import env

# fmt: off
INSTALLED_APPS: list[str] = [
    # Additional deps
    "axes",
    "daphne",
    "django_celery_results",
    "simple_history",

    # Default django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "backend.core",
    "backend.apps.delivery",
    "backend.apps.geo",
    "backend.apps.security",
    "backend.apps.tg_bots",
    "backend.apps.users",
]

if env("DEBUG", cast=bool):
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]

# fmt: on
