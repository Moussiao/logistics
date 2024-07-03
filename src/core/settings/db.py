from core.settings.environ import env

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # env.db() поднимет исключение если DATABASE_URL не указан в os.environ
    "default": env.db(),
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
