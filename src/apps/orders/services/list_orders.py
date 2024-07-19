from typing import final

import attr
from django.core.paginator import Page, Paginator
from django.db.models import Q, QuerySet
from pydantic import TypeAdapter

from apps.orders.api.schemas import OrderOutput, OrdersFilters, OrdersOutput
from apps.orders.models import Order
from apps.users.models import User
from core.types import SortDirecition

_orders_output_adapter = TypeAdapter(list[OrderOutput])


@final
@attr.dataclass(slots=True, frozen=True)
class ListOrders:
    COUNT_PER_PAGE = 10
    DEFAULT_ORDER_BY = "-pk"

    _user: User
    _filters: OrdersFilters

    def __call__(self) -> OrdersOutput:
        if self._user.is_anonymous or not self._user.role:
            return OrdersOutput(items=[], page=1, has_next_page=False)

        page = self._get_orders_page()
        orders = _orders_output_adapter.validate_python(page.object_list)
        return OrdersOutput(
            items=orders,
            page=page.number,
            has_next_page=page.has_next(),
        )

    def _get_orders_page(self) -> Page:
        orders_qs = self._get_orders_qs()
        paginator = Paginator(orders_qs, per_page=self.COUNT_PER_PAGE)
        return paginator.get_page(self._filters.page)

    def _get_orders_qs(self) -> QuerySet[Order, dict]:
        filters_q = Q()
        if self._user.role == User.Role.DELIVERY_PARTNER:
            filters_q &= Q(partner__user=self._user)

        if self._filters.status is not None:
            filters_q &= Q(status=self._filters.status)
        if self._filters.partner_id is not None:
            filters_q &= Q(partner_id=self._filters.partner_id)
        if self._filters.delivery_date_start is not None:
            filters_q &= Q(delivery_date__gte=self._filters.delivery_date_start)
        if self._filters.delivery_date_end is not None:
            filters_q &= Q(delivery_date__lte=self._filters.delivery_date_end)
        if self._filters.expected_delivery_date_start is not None:
            filters_q &= Q(
                expected_delivery_date__gte=self._filters.expected_delivery_date_start
            )
        if self._filters.expected_delivery_date_end is not None:
            filters_q &= Q(
                expected_delivery_date__lte=self._filters.expected_delivery_date_end
            )

        if self._filters.expected_delivery_date_sort is None:
            order_by = self.DEFAULT_ORDER_BY
        elif self._filters.expected_delivery_date_sort == SortDirecition.ASK:
            order_by = "expected_delivery_date"
        else:
            order_by = "-expected_delivery_date"

        return (
            Order.objects.filter(filters_q)
            .values(*OrderOutput.Meta.fields)
            .order_by(order_by)
        )
