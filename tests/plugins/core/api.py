from typing import TYPE_CHECKING

import pytest
from django.test import Client

if TYPE_CHECKING:
    from apps.users.models import User


@pytest.fixture()
def logistician_client(logistician_user: "User") -> Client:
    client = Client()
    client.force_login(user=logistician_user)
    return client


@pytest.fixture()
def partner_client(partner_user: "User") -> Client:
    client = Client()
    client.force_login(user=partner_user)
    return client
