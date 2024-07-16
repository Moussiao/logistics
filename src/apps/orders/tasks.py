from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils.timezone import now

from apps.orders.services.reports import ReportType, TelegramSender, TrySendReports


@shared_task(name="orders.tasks.notify_of_new_orders")
def notify_of_new_orders() -> None:
    reports_sender = TrySendReports(
        current_time=now(),
        sender=TelegramSender(),
        report_type=ReportType.NEW_ORDERS,
    )
    async_to_sync(reports_sender.send_to_active_partners)()


@shared_task(name="orders.tasks.notify_of_buyout_orders")
def notify_of_buyout_orders() -> None:
    reports_sender = TrySendReports(
        current_time=now(),
        sender=TelegramSender(),
        report_type=ReportType.BYUYOUT_ORDERS,
    )
    async_to_sync(reports_sender.send_to_active_partners)()
