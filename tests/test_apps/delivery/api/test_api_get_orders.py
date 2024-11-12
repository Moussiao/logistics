from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from src.apps.delivery.models import Order
from src.apps.delivery.services.orders.get_orders import GetOrders

if TYPE_CHECKING:
    from django.test import Client

    from tests.plugins.apps.delivery import OrdersFactory

pytestmark = [pytest.mark.django_db]


def test_get_orders(
    logistician_client: "Client",
    orders_factory: "OrdersFactory",
) -> None:
    orders_factory(GetOrders.PAGE_SIZE, state=Order.State.CANCELED)
    new_orders = orders_factory(GetOrders.PAGE_SIZE, state=Order.State.NEW)

    response = logistician_client.get(
        reverse("api:get_orders"),
        data={"states": Order.State.NEW.value},
    )

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["next_cursor"] is None
    assert response_json["previous_cursor"] is None
    assert len(response_json["items"]) == len(new_orders)


def test_not_auth_get_orders(client: "Client") -> None:
    response = client.get(reverse("api:get_orders"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
