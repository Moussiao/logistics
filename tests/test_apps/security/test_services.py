import json
from typing import TYPE_CHECKING

import pytest

from apps.security.api.schemas import TokenRequest
from apps.security.jwt import decode_user_access_token
from apps.security.services import (
    CreateAccessToken,
    CreateAccessTokenError,
    InvalidParsedInitDataSignatureError,
    OneUserNotFoundError,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture, MockType

    from apps.users.models import User
    from tests.plugins.apps.tg_bots import TgUserFactory


@pytest.fixture
def mock_init_data_validate(mocker: "MockerFixture") -> "MockType":
    return mocker.patch("apps.tg_bots.mini_app.InitDataValidator.validate", return_value=None)


@pytest.mark.django_db
def test_create_access_token(
    user: "User",
    tg_user_factory: "TgUserFactory",
    mock_init_data_validate: "MockType",
) -> None:
    tg_user = tg_user_factory(user=user)
    user_json = json.dumps({"id": tg_user.external_id})
    data = TokenRequest(tma_init_data=f"user={user_json}")

    access_token = CreateAccessToken(data)()

    decoded_token = decode_user_access_token(access_token)
    assert access_token
    assert decoded_token.user_id == user.pk
    mock_init_data_validate.assert_called_once_with(CreateAccessToken.INIT_DATA_PERIOD_OF_VALIDITY)


@pytest.mark.django_db
def test_user_not_found_error(
    tg_user_factory: "TgUserFactory",
    mock_init_data_validate: "MockType",
) -> None:
    tg_user = tg_user_factory(user=None)
    user_json = json.dumps({"id": tg_user.external_id})
    data = TokenRequest(tma_init_data=f"user={user_json}")

    with pytest.raises(OneUserNotFoundError):
        CreateAccessToken(data)()

    mock_init_data_validate.assert_called_once_with(CreateAccessToken.INIT_DATA_PERIOD_OF_VALIDITY)


def test_invalid_init_data() -> None:
    data = TokenRequest(tma_init_data="")
    with pytest.raises(CreateAccessTokenError):
        CreateAccessToken(data)()


def test_invalid_parsed_init_data_signature(mock_init_data_validate: "MockType") -> None:
    data = TokenRequest(tma_init_data="user=user")

    with pytest.raises(InvalidParsedInitDataSignatureError):
        CreateAccessToken(data)()

    mock_init_data_validate.assert_called_once_with(CreateAccessToken.INIT_DATA_PERIOD_OF_VALIDITY)
