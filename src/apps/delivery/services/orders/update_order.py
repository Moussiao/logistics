from typing import final

import attr
from django.db.models import Q

from src.apps.delivery.api.schemas import EditOrderRequest
from src.apps.delivery.models import Order
from src.apps.delivery.services.orders.exceptions import OrderNotFoundError
from src.apps.users.models import User


@final
@attr.dataclass(slots=True, frozen=True)
class UpdateOrder:
    _user: User
    _order_id: int
    _payload: EditOrderRequest

    def __call__(self) -> None:
        if self._user.is_anonymous or not self._user.role:
            raise OrderNotFoundError

        filters_q = Q()
        if self._user.role == User.Role.DELIVERY_PARTNER:
            filters_q &= Q(partner__user=self._user)

        try:
            order = Order.objects.filter(filters_q).get(id=self._order_id)
        except Order.DoesNotExist as exc:
            raise OrderNotFoundError from exc

        update_fields = []
        for field_name, field_value in self._payload.dict().items():
            setattr(order, field_name, field_value)
            update_fields.append(field_name)

        if update_fields:
            order.save(update_fields=update_fields)
