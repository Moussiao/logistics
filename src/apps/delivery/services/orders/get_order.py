from typing import final

import attr
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from src.apps.delivery.models import Order
from src.apps.delivery.services.orders.exceptions import OrderNotFoundError
from src.apps.users.models import User


@final
@attr.dataclass(frozen=True, slots=True)
class GetOrder:
    _user: User | AnonymousUser
    _order_id: int

    def __call__(self) -> Order:
        if self._user.is_anonymous or not self._user.role:
            raise OrderNotFoundError

        filters_q = Q()
        if self._user.role == User.Role.DELIVERY_PARTNER:
            filters_q &= Q(partner__user=self._user)

        try:
            order = (
                Order.objects.filter(filters_q)
                .select_related(
                    "customer",
                    "customer_address__country",
                    "customer_address__region",
                    "customer_address__city",
                )
                .prefetch_related("products__product")
                .get(id=self._order_id)
            )
        except Order.DoesNotExist as exc:
            raise OrderNotFoundError(f"Order with id={self._order_id} not exists") from exc

        return order
