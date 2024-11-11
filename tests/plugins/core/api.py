from typing import TYPE_CHECKING

import pytest
from django.test import Client
from ninja.security import django_auth

from core.api import api

if TYPE_CHECKING:
    from apps.users.models import User


@pytest.fixture(autouse=True)
def _global_api_auth() -> None:
    api.auth = [django_auth]


@pytest.fixture
def logistician_client(logistician_user: "User") -> Client:
    client = Client()
    client.force_login(user=logistician_user)
    return client


@pytest.fixture
def partner_client(partner_user: "User") -> Client:
    client = Client()
    client.force_login(user=partner_user)
    return client
