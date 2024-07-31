from http import HTTPStatus

from django.test import Client
from django.urls import reverse


def test_invalid_create_access_token(client: Client) -> None:
    invalid_data = {"tma_init_data": "invalid"}

    response = client.post(
        reverse("api:create_access_token"),
        data=invalid_data,
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
