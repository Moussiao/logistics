from http import HTTPStatus

import pytest
from django.test import Client


def test_admin_unauthorized(client: Client) -> None:
    """This test ensures that admin panel requires auth."""
    response = client.get("/admin/")

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_admin_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel is accessible."""
    response = admin_client.get("/admin/")

    assert response.status_code == HTTPStatus.OK
