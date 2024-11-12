from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from src.apps.delivery.models import Order, Partner

if TYPE_CHECKING:
    from tests.test_apps.delivery.api.conftest import CustomerRequestFactory, OrderRequestFactory


pytestmark = [pytest.mark.django_db]


def test_create_order(
    partner: Partner,
    admin_client: Client,
    order_request_factory: "OrderRequestFactory",
) -> None:
    create_order_data = order_request_factory.build(partner_id=partner.pk).dict()

    response = admin_client.post(
        reverse("api:create_order"),
        data=create_order_data,
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert Order.objects.filter(partner=partner).count() == 1


def test_invalid_phone_create_order(
    partner: Partner,
    admin_client: Client,
    order_request_factory: "OrderRequestFactory",
    customer_request_factory: "CustomerRequestFactory",
) -> None:
    customer_request = customer_request_factory.build(
        phone="invalid_phone", factory_use_construct=True
    )
    create_order_data = order_request_factory.build(
        partner=partner.name, customer=customer_request, factory_use_construct=True
    ).dict()

    response = admin_client.post(
        reverse("api:create_order"),
        data=create_order_data,
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert Order.objects.filter(partner=partner).count() == 0


def test_duplicate_create_order(
    order: Order,
    partner: Partner,
    admin_client: Client,
    order_request_factory: "OrderRequestFactory",
) -> None:
    create_order_data = order_request_factory.build(
        partner=partner.name, external_id=order.external_id
    ).dict()

    response = admin_client.post(
        reverse("api:create_order"),
        data=create_order_data,
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert Order.objects.filter(partner=partner).count() == 0


def test_not_auth_create_order(client: "Client") -> None:
    response = client.post(reverse("api:create_order"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
