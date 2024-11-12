from http import HTTPStatus
from typing import cast

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from src.apps.users.api.schemas import UserResponse
from src.apps.users.models import User

router = Router()


@router.get("/me", response=UserResponse)
def get_self_user(request: HttpRequest) -> User:
    if request.user.is_anonymous:
        # Данного случая не должно произойти, только если пользователь
        # удален или глобальная аунтификация была убрана, либо работает не верно.
        raise HttpError(HTTPStatus.FORBIDDEN, message=HTTPStatus.FORBIDDEN.description)

    return cast(User, request.user)
