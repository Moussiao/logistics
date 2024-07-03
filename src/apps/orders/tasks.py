from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone

from apps.orders.services.new_orders_report import NotifyNewOrders


@shared_task(name="orders.tasks.notify_of_new_orders")
def notify_of_new_orders() -> None:
    new_orders_notifier = NotifyNewOrders(started_at=timezone.now())
    async_to_sync(new_orders_notifier)()
