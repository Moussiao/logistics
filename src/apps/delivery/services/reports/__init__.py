import asyncio
from collections import defaultdict
from datetime import datetime
from typing import TYPE_CHECKING, final

from django.utils.timezone import now

from src.apps.delivery.models import Partner
from src.apps.delivery.services.reports.buyout_orders_report import (
    PreviousDayBuyoutedOrders,
    PreviousMonthBuyoutedOrders,
)
from src.apps.delivery.services.reports.exceptions import NotAvailableReportError, SenderError
from src.apps.delivery.services.reports.new_orders_report import TodayNewOrders, TomorrowNewOrders
from src.apps.delivery.services.reports.senders import TelegramSender
from src.apps.delivery.services.reports.types import ReportType

if TYPE_CHECKING:
    from .base import OrdersReport, OrdersReportSender

__all__ = (
    # Отчеты
    "ReportType",
    "TrySendReports",
    "TodayNewOrders",
    "TomorrowNewOrders",
    "PreviousDayBuyoutedOrders",
    "PreviousMonthBuyoutedOrders",
    "NotAvailableReportError",
    # Отправители
    "SenderError",
    "TelegramSender",
)

_reports_classes: tuple[type["OrdersReport"], ...] = (
    TodayNewOrders,
    TomorrowNewOrders,
    PreviousDayBuyoutedOrders,
    PreviousMonthBuyoutedOrders,
)

_report_classes_by_type = defaultdict(list)
for report in _reports_classes:
    _report_classes_by_type[report.report_type].append(report)


@final
class TrySendReports:
    def __init__(
        self,
        report_type: ReportType,
        sender: "OrdersReportSender",
        current_time: datetime | None = None,
    ) -> None:
        self._sender = sender
        self._report_classes = _report_classes_by_type.get(report_type, [])
        self._current_time = current_time if current_time is not None else now()

    async def send_to_active_partners(self) -> None:
        sender_partners_qs = self._sender.get_valid_partners_qs()
        active_partners_qs = Partner.objects.filter(is_active=True).order_by()
        partners_qs = sender_partners_qs & active_partners_qs
        # Для отчетов необходима работа с данным полем
        partners_qs = partners_qs.select_related("working_time_zone")

        await asyncio.gather(*[self.send_to_partner(x) async for x in partners_qs])

    async def send_to_partner(self, partner: Partner) -> None:
        for report_class in self._report_classes:
            report = report_class(partner=partner, current_time=self._current_time)
            try:
                await self._send_report(partner=partner, report=report)
            except NotAvailableReportError:
                continue

    def get_reports_count(self) -> int:
        return len(self._report_classes)

    async def _send_report(self, partner: Partner, report: "OrdersReport") -> None:
        report_text = await report.aget_text()
        if not report_text:
            return

        await self._sender.send(text=report_text, partner=partner)
