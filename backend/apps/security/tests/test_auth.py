from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest
from freezegun.api import FrozenDateTimeFactory, StepTickTimeFactory

from backend.apps.security.auth import AccessTokenAuth
from backend.apps.security.jwt import (
    create_access_token,
    create_user_access_token,
    decode_user_access_token,
)

if TYPE_CHECKING:
    from django.conf import LazySettings

    from backend.apps.users.models import User


type Freezer = FrozenDateTimeFactory | StepTickTimeFactory


@pytest.mark.django_db
def test_decode_token(user: "User") -> None:
    token = create_user_access_token(user_id=user.pk)
    expected_payload = decode_user_access_token(token)

    token_payload = AccessTokenAuth.decode_token(token)

    assert token_payload == expected_payload


@pytest.mark.django_db
def test_expired_decode_access_token(
    user: "User", freezer: Freezer, settings: "LazySettings"
) -> None:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # type: ignore[misc]
    token = create_user_access_token(user_id=user.pk)
    freezer.move_to(datetime.now(UTC) + expires_delta)

    token_payload = AccessTokenAuth.decode_token(token)

    assert token_payload is None


def test_invalid_decode_access_token() -> None:
    token = create_access_token({"some": "some", "some2": "some2"})
    token_payload = AccessTokenAuth.decode_token(token)
    assert token_payload is None
