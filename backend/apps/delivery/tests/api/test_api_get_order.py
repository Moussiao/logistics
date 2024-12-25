from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from backend.apps.delivery.models import Order

pytestmark = [pytest.mark.django_db]


def test_get_order(logistician_client: "Client", order: "Order") -> None:
    response = logistician_client.get(reverse("api:get_order", args=(order.pk,)))

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == order.pk
    assert response_json["external_id"] == order.external_id
    assert response_json["external_verbose"] == order.external_verbose
    assert response_json["state"] == order.state
    assert response_json["comment"] == order.comment


def test_not_found_error(logistician_client: "Client") -> None:
    response = logistician_client.get(reverse("api:get_order", args=(-1,)))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_auth_get_order(client: "Client", order: "Order") -> None:
    response = client.get(reverse("api:get_order", args=(order.pk,)))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
