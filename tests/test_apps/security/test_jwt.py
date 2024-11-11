from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest
from freezegun.api import (
    FrozenDateTimeFactory,
    StepTickTimeFactory,
    TickingDateTimeFactory,
)
from jwt import ExpiredSignatureError

from apps.security.jwt import (
    InvalidUserAccessTokenPayloadError,
    create_access_token,
    create_user_access_token,
    decode_access_token,
    decode_user_access_token,
)

if TYPE_CHECKING:
    from django.conf import LazySettings

    from apps.users.models import User


type Freezer = FrozenDateTimeFactory | StepTickTimeFactory | TickingDateTimeFactory


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_create_access_token() -> None:
    expires_delta = timedelta(minutes=30)
    payload_data = {"user_id": 1, "role": "partner"}

    token = create_access_token(payload_data, expires_delta)

    token_payload = decode_access_token(token)
    expected_datetime_expire = datetime.now(UTC) + expires_delta
    assert token_payload["role"] == payload_data["role"]
    assert token_payload["user_id"] == payload_data["user_id"]
    assert token_payload["exp"] == int(expected_datetime_expire.timestamp())
    assert list(token_payload.keys()) == list(payload_data.keys()) + ["exp"]


@pytest.mark.django_db
@pytest.mark.freeze_time("2022-07-01 14:00")
def test_create_user_access_token(user: "User", settings: "LazySettings") -> None:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_user_access_token(user.pk)

    token_payload = decode_user_access_token(token)
    expected_datetime_expire = datetime.now(UTC) + expires_delta
    assert token_payload.user_id == user.pk
    assert token_payload.exp == int(expected_datetime_expire.timestamp())


def test_expired_decode_access_token(freezer: Freezer) -> None:
    expires_delta = timedelta(minutes=30)
    token = create_access_token({"user_id": 1}, expires_delta)
    freezer.move_to(datetime.now(UTC) + expires_delta)

    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)


def test_invalid_decode_user_access_token() -> None:
    token = create_access_token({"some": "some", "some2": "some2"})

    with pytest.raises(InvalidUserAccessTokenPayloadError):
        decode_user_access_token(token)
