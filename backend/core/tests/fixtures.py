from typing import TYPE_CHECKING

import pytest
from django.conf import LazySettings
from django.core.cache import BaseCache, caches
from django.test import Client
from ninja.security import django_auth

from backend.core.api import api

if TYPE_CHECKING:
    from backend.apps.users.models import User


@pytest.fixture(autouse=True)
def _media_root(
    settings: LazySettings,
    tmpdir_factory: pytest.TempPathFactory,
) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings: LazySettings) -> None:
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings: LazySettings) -> None:
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


@pytest.fixture(autouse=True)
def _debug(settings: LazySettings) -> None:
    """Sets proper DEBUG and TEMPLATE debug mode for coverage."""
    settings.DEBUG = False
    for template in settings.TEMPLATES:
        template["OPTIONS"]["debug"] = True


@pytest.fixture(autouse=True)
def cache(settings: LazySettings) -> BaseCache:
    """Modifies how cache is used in Django tests."""
    test_cache = "test"

    # Patching cache settings:
    settings.CACHES[test_cache] = {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
    settings.RATELIMIT_USE_CACHE = test_cache
    settings.AXES_CACHE = test_cache

    # Clearing cache:
    caches[test_cache].clear()
    return caches[test_cache]


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
