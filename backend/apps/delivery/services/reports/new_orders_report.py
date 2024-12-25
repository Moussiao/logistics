from collections.abc import Sequence
from datetime import timedelta
from typing import final

from django.conf import settings
from django.db.models import QuerySet

from backend.apps.delivery.models import Order
from backend.apps.delivery.services.reports.base import OrdersReport
from backend.apps.delivery.services.reports.types import ReportType


class BaseNewOrdersReport(OrdersReport):
    """Базовый отчет по новым заказам."""

    EMPTY_ORDERS_TEXT = ""

    report_type = ReportType.NEW_ORDERS

    def _get_base_ordres_qs(self) -> QuerySet[Order]:
        return (
            Order.objects.filter(partner=self._partner, state=Order.State.NEW)
            .select_related("customer")
            .prefetch_related("products")
            .order_by("id")
        )

    def _prepare_orders_text(self, orders: Sequence[Order]) -> str:
        return "\n".join(self._prepare_order_report(x) for x in orders)

    def _prepare_order_report(self, order: Order) -> str:
        total_price = sum(x.total_price for x in order.products.all())

        return (
            f"ID: {order.external_id}\n"
            f"Телефон: {order.customer.phone}\n"
            f"Стоимость товаров: {total_price}\n"
            f"{settings.TG_ORDERS_URL}?startapp={order.pk}\n"  # type: ignore[misc]
        )


@final
class TodayNewOrders(BaseNewOrdersReport):
    """Дневной отчет о новых заказах на сегодня."""

    ALLOWED_HOUR = 13

    def _is_report_allowed(self) -> bool:
        return self._partner_current_time.hour == self.ALLOWED_HOUR

    def _get_orders_to_report(self) -> tuple[Order, ...]:
        current_date = self._partner_current_date

        orders_qs = self._get_base_ordres_qs()
        return tuple(orders_qs.filter(expected_delivery_date__lte=current_date))

    def _prepare_orders_report(self, orders: Sequence[Order]) -> str:
        if not orders:
            return self.EMPTY_ORDERS_TEXT

        current_date = self._partner_current_date
        orders_text = self._prepare_orders_text(orders)
        base_text = f"{current_date} - {len(orders)} новых заказов на сегодня:\n\n"
        return base_text + orders_text


@final
class TomorrowNewOrders(BaseNewOrdersReport):
    """Вечерний отчет о новых заказах на завтра."""

    ALLOWED_HOUR = 22

    def _is_report_allowed(self) -> bool:
        return self._partner_current_time.hour == self.ALLOWED_HOUR

    def _get_orders_to_report(self) -> tuple[Order, ...]:
        tomorrow_date = self._partner_current_date + timedelta(days=1)

        orders_qs = self._get_base_ordres_qs()
        return tuple(orders_qs.filter(expected_delivery_date=tomorrow_date))

    def _prepare_orders_report(self, orders: Sequence[Order]) -> str:
        if not orders:
            return self.EMPTY_ORDERS_TEXT

        current_date = self._partner_current_date
        orders_text = self._prepare_orders_text(orders)
        base_text = f"{current_date} - {len(orders)} новых заказов на завтра:\n\n"
        return base_text + orders_text
