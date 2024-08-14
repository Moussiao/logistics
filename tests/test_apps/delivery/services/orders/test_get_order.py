from typing import TYPE_CHECKING

import pytest

from apps.delivery.services.orders.get_order import GetOrder, OrderNotFoundError

if TYPE_CHECKING:
    from apps.delivery.models import Order

pytestmark = [pytest.mark.django_db]


def test_get_order(order: "Order") -> None:
    result = GetOrder(order.pk)()

    assert order == result


def test_not_found_error() -> None:
    with pytest.raises(OrderNotFoundError):
        # Не валидный id в нашей системе
        GetOrder(-1)()
