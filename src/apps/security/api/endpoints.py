from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from apps.security.api.schemas import TokenRequest, TokenResponse
from apps.security.services import CreateAccessToken, CreateAccessTokenError

router = Router()


@router.post("/access_token", auth=None, response=TokenResponse)
def create_access_token(request: HttpRequest, data: TokenRequest) -> TokenResponse:
    try:
        token = CreateAccessToken(data)()
    except CreateAccessTokenError as exc:
        raise HttpError(
            status_code=HTTPStatus.FORBIDDEN,
            message="Invalid authentication credentials",
        ) from exc

    return TokenResponse(token=token)
