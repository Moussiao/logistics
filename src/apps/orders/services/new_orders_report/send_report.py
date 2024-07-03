from collections.abc import Sequence
from datetime import timedelta
from typing import TYPE_CHECKING, final

import attr
from asgiref.sync import sync_to_async
from django.db.models import Q
from django.utils.timezone import localdate

from apps.orders.models import Order
from apps.orders.services.new_orders_report.base import NewOrdersReportType
from apps.tg_bots.services import TgSendMessage

if TYPE_CHECKING:
    from apps.orders.models import Partner


@final
@attr.dataclass(slots=True, frozen=True)
class SendNewOrdersReport:
    """Отправляет отчет по новым заказам."""

    _partner: "Partner"
    _report_type: "NewOrdersReportType"

    async def __call__(self) -> None:
        orders = await self._get_orders_to_report()
        if not orders:
            return

        report_text = self._prepare_orrders_report(orders)
        tg_message_sender = TgSendMessage(text=report_text, chat=self._partner.tg_chat)
        await tg_message_sender()

    @sync_to_async
    def _get_orders_to_report(self) -> tuple[Order, ...]:
        filter_q = Q(partner=self._partner, status=Order.Status.NEW)

        partner_timezone = self._partner.working_time_zone.get_zone_info()
        partner_date = localdate(timezone=partner_timezone)
        if self._report_type == NewOrdersReportType.DAILY:
            filter_q &= Q(expected_delivery_date__lt=partner_date + timedelta(days=1))
        elif self._report_type == NewOrdersReportType.EVENING:
            filter_q &= Q(expected_delivery_date=partner_date + timedelta(days=1))

        return tuple(Order.objects.filter(filter_q).order_by("id"))

    def _prepare_orrders_report(self, orders: Sequence[Order]) -> str:
        return ",".join(str(order.id) for order in orders)
