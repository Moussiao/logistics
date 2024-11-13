from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from django.conf import settings


class InvalidUserAccessTokenPayloadError(jwt.InvalidSignatureError):
    pass


@dataclass(frozen=True, slots=True)
class UserAccessTokenPayload:
    exp: int
    user_id: int


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(UTC)
    if expires_delta is not None:
        expires = now + expires_delta
    else:
        expires = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # type: ignore[misc]

    payload = data.copy()
    payload["exp"] = expires

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)  # type: ignore[misc]


def decode_access_token(token: str) -> dict[str, Any]:
    token_payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])  # type: ignore[misc]
    if not isinstance(token_payload, dict):
        return {}

    return token_payload


def create_user_access_token(user_id: int) -> str:
    token_data = {"user_id": user_id}
    return create_access_token(token_data)


def decode_user_access_token(token: str) -> UserAccessTokenPayload:
    token_payload = decode_access_token(token)

    try:
        exp = int(token_payload["exp"])
        user_id = int(token_payload["user_id"])
    except (KeyError, ValueError) as exc:
        raise InvalidUserAccessTokenPayloadError(f"{token} is invalid") from exc

    return UserAccessTokenPayload(exp=exp, user_id=user_id)
