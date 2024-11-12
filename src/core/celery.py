# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django
import os
from logging import getLogger
from typing import Any

from celery import Celery
from celery.schedules import crontab

log = getLogger(__name__)

# Устанавливаем значение по умолчания
# для среды DJANGO_SETTINGS_MODULE, чтобы Celery могла работать с Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")

app = Celery("app")

# Загружаем значения конфигурации Celery из настроек Django проекта
# namespace='CELERY' используется для предотвращения коллизий с другими настройками
# Таким образом все конфигурации Celery должны начинаться с префикса CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Загружает все задачи в tasks.py модулях из django приложений
app.autodiscover_tasks()
# With the line above Celery will automatically discover tasks
# from all of your installed apps, following the tasks.py convention:
# - app1/
#     - tasks.py
#     - models.py
# - app2/
#     - tasks.py
#     - models.py


@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs: Any) -> None:
    """
    Регистрирует задачи, которые выполняются в определенные периоды времени.
    (https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#entries)
    """
    from src.apps.delivery.tasks import notify_of_buyout_orders, notify_of_new_orders

    sender.add_periodic_task(
        schedule=crontab(hour="*/1", minute="0"),
        sig=notify_of_new_orders.s(),
        name="new_orders_notification",
    )
    sender.add_periodic_task(
        schedule=crontab(hour="*/1", minute="0"),
        sig=notify_of_buyout_orders.s(),
        name="buyout_orders_notification",
    )
