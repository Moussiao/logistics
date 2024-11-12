from logging import getLogger
from typing import cast

from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject
from jwt import ExpiredSignatureError, InvalidTokenError
from ninja.security import HttpBearer

from src.apps.security.jwt import UserAccessTokenPayload, decode_user_access_token
from src.apps.users.models import User

log = getLogger(__name__)


class AccessTokenAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        token_payload = self.decode_token(token)
        if token_payload is None:
            return None

        if not request.user.is_authenticated:
            request.user = SimpleLazyObject(  # type: ignore[misc]
                lambda: self.get_user(request=request, token_payload=token_payload)
            )

        return token

    @staticmethod
    def decode_token(token: str) -> UserAccessTokenPayload | None:
        try:
            payload = decode_user_access_token(token)
        except ExpiredSignatureError:
            payload = None
        except InvalidTokenError:
            log.exception("Invalid access token")
            payload = None

        return payload

    @staticmethod
    def get_user(
        request: HttpRequest,
        token_payload: UserAccessTokenPayload,
    ) -> User | AnonymousUser:
        user = User.objects.filter(pk=token_payload.user_id, is_active=True).first()
        if user is None:
            user = get_user(request)
            user = cast(User | AnonymousUser, user)

        return user
