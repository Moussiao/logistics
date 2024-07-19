from typing import final

import attr

from apps.orders.models import Order
from apps.orders.services.exceptions import OrderNotFoundError


@final
@attr.dataclass(frozen=True, slots=True)
class RetrieveOrder:
    _order_id: int

    def __call__(self) -> Order:
        try:
            order = (
                Order.objects.select_related(
                    "customer",
                    "customer_address__country",
                    "customer_address__region",
                    "customer_address__city",
                )
                .prefetch_related("products")
                .get(id=self._order_id)
            )
        except Order.DoesNotExist as exc:
            raise OrderNotFoundError(
                f"Order with id={self._order_id} not exists"
            ) from exc

        return order
