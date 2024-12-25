from typing import TYPE_CHECKING

import pytest

from backend.apps.delivery.services.orders.exceptions import OrderNotFoundError
from backend.apps.delivery.services.orders.get_order import GetOrder

if TYPE_CHECKING:
    from backend.apps.delivery.models import Order
    from backend.apps.users.models import User

pytestmark = [pytest.mark.django_db]


def test_get_order(logistician_user: "User", order: "Order") -> None:
    result = GetOrder(user=logistician_user, order_id=order.pk)()
    assert order == result


def test_not_found_error(logistician_user: "User") -> None:
    with pytest.raises(OrderNotFoundError):
        # Не валидный id в нашей системе
        GetOrder(user=logistician_user, order_id=-1)()
