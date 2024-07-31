import pytest

from apps.security.api.schemas import TokenRequest
from apps.security.services import CreateAccessToken, CreateAccessTokenError


def test_invalid_init_data() -> None:
    data = TokenRequest(tma_init_data="")
    with pytest.raises(CreateAccessTokenError):
        CreateAccessToken(data)()
