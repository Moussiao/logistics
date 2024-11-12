from typing import final

import attr
from django.db.models import Q, QuerySet
from pydantic import TypeAdapter

from src.apps.delivery.api.schemas import OrderResponse, OrdersFilters, OrdersResponse
from src.apps.delivery.models import Order
from src.apps.users.models import User
from src.core.paginator import CursorPage, CursorPaginator
from src.core.utils import safe_string_to_enums, safe_string_to_integers

_orders_response_adapter = TypeAdapter(list[OrderResponse])


@final
@attr.dataclass(slots=True, frozen=True)
class GetOrders:
    PAGE_SIZE = 10

    _user: User
    _filters: OrdersFilters

    def __call__(self) -> OrdersResponse:
        if self._user.is_anonymous or not self._user.role:
            return OrdersResponse(items=[], next_cursor=None, previous_cursor=None)

        page = self._get_orders_page()
        orders = _orders_response_adapter.validate_python(page.objects)
        return OrdersResponse(
            items=orders,
            next_cursor=page.next_cursor,
            previous_cursor=page.previous_cursor,
        )

    def _get_orders_page(self) -> CursorPage:
        orders_qs = self._get_orders_qs()
        paginator = CursorPaginator(orders_qs, page_size=self.PAGE_SIZE)
        return paginator.get_page(self._filters.cursor)

    def _get_orders_qs(self) -> QuerySet[Order, dict]:
        filters_q = Q()
        if self._user.role == User.Role.DELIVERY_PARTNER:
            filters_q &= Q(partner__user=self._user)

        if self._filters.ids is not None:
            filters_q &= Q(id__in=safe_string_to_integers(self._filters.ids))
        if self._filters.states is not None:
            filters_q &= Q(state__in=safe_string_to_enums(self._filters.states, Order.State))
        if self._filters.partner_id is not None:
            filters_q &= Q(partner_id=self._filters.partner_id)
        if self._filters.delivery_date_start is not None:
            filters_q &= Q(delivery_date__gte=self._filters.delivery_date_start)
        if self._filters.delivery_date_end is not None:
            filters_q &= Q(delivery_date__lte=self._filters.delivery_date_end)
        if self._filters.expected_delivery_date_start is not None:
            filters_q &= Q(expected_delivery_date__gte=self._filters.expected_delivery_date_start)
        if self._filters.expected_delivery_date_end is not None:
            filters_q &= Q(expected_delivery_date__lte=self._filters.expected_delivery_date_end)

        fields = ("created_at",) + OrderResponse.Meta.fields
        return Order.objects.filter(filters_q).values(*fields).order_by("-created_at")
