from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from django.utils.timezone import localdate

from apps.delivery.models import Order
from apps.delivery.services.orders.get_orders import GetOrders

if TYPE_CHECKING:
    from django.test import Client

    from tests.plugins.apps.delivery import OrdersFactory

pytestmark = [pytest.mark.django_db]


def test_get_orders(
    logistician_client: "Client",
    orders_factory: "OrdersFactory",
) -> None:
    orders_factory(GetOrders.COUNT_PER_PAGE, status=Order.Status.RETURN)
    new_orders = orders_factory(GetOrders.COUNT_PER_PAGE, status=Order.Status.NEW)

    response = logistician_client.get(
        reverse("api:get_orders"),
        data={"page": 1, "status": Order.Status.NEW.value},
    )

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["page"] == 1
    assert response_json["has_next_page"] is False
    assert len(response_json["items"]) == len(new_orders)


def test_invalid_page_get_orders(
    logistician_client: "Client",
    orders_factory: "OrdersFactory",
) -> None:
    local_date = localdate()
    orders = orders_factory(GetOrders.COUNT_PER_PAGE, delivery_date=local_date)

    response = logistician_client.get(
        reverse("api:get_orders"),
        data={"page": 5, "delivery_date_start": local_date.isoformat()},
    )

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["page"] == 1
    assert response_json["has_next_page"] is False
    assert len(response_json["items"]) == len(orders)


def test_not_auth_get_orders(client: "Client") -> None:
    response = client.get(reverse("api:get_orders"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
