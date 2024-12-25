from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from backend.apps.users.models import User

pytestmark = [pytest.mark.django_db]


def test_get_logistician(logistician_client: "Client", logistician_user: "User") -> None:
    response = logistician_client.get(reverse("api:get_self_user"))

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == logistician_user.pk
    assert response_json["role"] == logistician_user.role


def test_get_partner(partner_client: "Client", partner_user: "User") -> None:
    response = partner_client.get(reverse("api:get_self_user"))

    response_json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_json["id"] == partner_user.pk
    assert response_json["role"] == partner_user.role


def test_not_auth(client: "Client") -> None:
    response = client.get(reverse("api:get_self_user"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
