from backend.core.settings.environ import env

BASE_REDIS_URL = env("REDIS_URL")

# Настройки Celery Broker
# (https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-settings)
CELERY_BROKER_URL = BASE_REDIS_URL + "/1"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Настройки Celery Result
# (https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-result-backend-settings)
# Результаты складируем при помощи сторонней библиотеки django-celery-results
# (https://django-celery-results.readthedocs.io/en/latest/getting_started.html#getting-started)
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True

# Настройки Celery Task (https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-settings)
CELERY_TASK_COMPRESSION = "gzip"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60 * 60
