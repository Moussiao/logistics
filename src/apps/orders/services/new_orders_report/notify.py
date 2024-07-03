import asyncio
from typing import TYPE_CHECKING, final

import attr
from django.utils.timezone import localtime

from apps.orders.models import Partner
from apps.orders.services.new_orders_report.base import REPORT_TYPE_BY_HOUR
from apps.orders.services.new_orders_report.send_report import SendNewOrdersReport

if TYPE_CHECKING:
    from datetime import datetime


@final
@attr.dataclass(slots=True, frozen=True)
class NotifyNewOrders:
    """Оповещает партнеров о новых заказах, если это необходимо."""

    _started_at: "datetime"

    async def __call__(self) -> None:
        active_partners_qs = (
            Partner.objects.filter(is_active=True, tg_chat__isnull=False)
            .select_related("working_time_zone", "tg_chat")
            .order_by()
        )

        await asyncio.gather(
            *[self._notify_partner(partner) async for partner in active_partners_qs]
        )

    async def _notify_partner(self, partner: Partner) -> None:
        partner_zone_info = partner.working_time_zone.get_zone_info()
        partner_time = localtime(self._started_at, timezone=partner_zone_info)
        report_type = REPORT_TYPE_BY_HOUR.get(partner_time.hour)
        if report_type is not None:
            sender = SendNewOrdersReport(partner=partner, report_type=report_type)
            await sender()
