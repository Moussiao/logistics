from src.core.settings.environ import env

# fmt: off
INSTALLED_APPS: list[str] = [
    # Additional deps
    "axes",
    "daphne",
    "django_celery_results",

    # Default django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "src.core",
    "src.apps.delivery",
    "src.apps.geo",
    "src.apps.security",
    "src.apps.tg_bots",
    "src.apps.users",
]

if env("DEBUG", cast=bool):
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]

# fmt: on
