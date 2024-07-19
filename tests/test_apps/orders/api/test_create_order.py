from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from apps.orders.models import Order

if TYPE_CHECKING:
    from django.test import Client

    from apps.orders.models import Partner
    from tests.test_apps.orders.api.conftest import (
        CustomerInputFactory,
        OrderInputFactory,
    )


pytestmark = [pytest.mark.django_db]


def test_create_order(
    partner: "Partner",
    admin_client: "Client",
    order_input_factory: "OrderInputFactory",
) -> None:
    create_order_data = order_input_factory.build(partner=partner.name).dict()

    response = admin_client.post(
        reverse("api:create_order"),
        data=create_order_data,
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert Order.objects.filter(partner=partner).count() == 1


def test_invalid_phone_create_order(
    partner: "Partner",
    admin_client: "Client",
    order_input_factory: "OrderInputFactory",
    customer_input_factory: "CustomerInputFactory",
) -> None:
    customer_input = customer_input_factory.build(
        phone="invalid_phone", factory_use_construct=True
    )
    create_order_data = order_input_factory.build(
        partner=partner.name, customer=customer_input, factory_use_construct=True
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
