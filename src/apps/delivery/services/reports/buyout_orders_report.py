from collections.abc import Sequence
from datetime import timedelta
from decimal import Decimal
from typing import final

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet

from src.apps.delivery.models import Order
from src.apps.delivery.services.reports.base import OrdersReport
from src.apps.delivery.services.reports.types import ReportType


class BaseBuyoutedOrdersReport(OrdersReport):
    """Базовый отчет по выкупленным заказам."""

    report_type = ReportType.BYUYOUT_ORDERS

    def _get_base_orders_qs(self) -> QuerySet[Order]:
        return (
            Order.objects.filter(partner=self._partner, state=Order.State.PAID)
            .prefetch_related("products")
            .order_by()
        )

    def _get_products_total_price(self, orders: Sequence[Order]) -> Decimal:
        products_total_price = Decimal()
        for order in orders:
            for product in order.products.all():
                products_total_price += product.total_price

        return products_total_price


@final
class PreviousDayBuyoutedOrders(BaseBuyoutedOrdersReport):
    """Отчет выкупленных заказов за прошлый день."""

    ALLOWED_HOUR = 14

    EMPTY_ORDERS_TEXT = ""

    def _is_report_allowed(self) -> bool:
        return self._partner_current_time.hour == self.ALLOWED_HOUR

    def _get_orders_to_report(self) -> tuple[Order, ...]:
        previous_date = self._partner_current_date - timedelta(days=1)

        orders_qs = self._get_base_orders_qs()
        return tuple(orders_qs.filter(delivery_date=previous_date))

    def _prepare_orders_report(self, orders: Sequence[Order]) -> str:
        if not orders:
            return self.EMPTY_ORDERS_TEXT

        len_orders = len(orders)
        products_total_price = self._get_products_total_price(orders)

        return (
            f"{self._partner_current_date} - Финансовый отчет за прошедший день:\n\n"
            f"Всего успешно доставлено заказов: {len_orders}\n"
            f"Сумма стоимости товаров: {products_total_price}"
        )


@final
class PreviousMonthBuyoutedOrders(BaseBuyoutedOrdersReport):
    """Отчет выкупленных заказов за прошедший месяц."""

    ALLOWED_DAY = 1
    ALLOWED_HOUR = 14

    EMPTY_ORDERS_TEXT = "За прошедший месяц нет выкупленных заказов"

    def _is_report_allowed(self) -> bool:
        return (
            self._partner_current_time.day == self.ALLOWED_DAY
            and self._partner_current_time.hour == self.ALLOWED_HOUR
        )

    def _get_orders_to_report(self) -> tuple[Order, ...]:
        previous_date = self._partner_current_date - timedelta(days=1)
        previous_month_first_date = self._partner_current_date - relativedelta(months=1)

        orders_qs = self._get_base_orders_qs()
        delivery_date_range = (previous_month_first_date, previous_date)
        return tuple(orders_qs.filter(delivery_date__range=delivery_date_range))

    def _prepare_orders_report(self, orders: Sequence[Order]) -> str:
        if not orders:
            return self.EMPTY_ORDERS_TEXT

        len_orders = len(orders)
        products_total_price = self._get_products_total_price(orders)

        return (
            f"{self._partner_current_date} - Финансовый отчет за прошедший месяц:\n\n"
            f"Всего успешно доставлено заказов: {len_orders}\n"
            f"Сумма стоимости товаров: {products_total_price}"
        )
