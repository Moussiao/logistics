import json
import time
from contextlib import nullcontext as does_not_raise
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from backend.apps.tg_bots.mini_app import (
    ExpiredInitDataError,
    InitDataValidator,
    InvalidFormatInitDataError,
    InvalidHashInitDataError,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture, MockType

# Слепок валидных данных на вход валидатора на момент когда валидатор работает верно.
_valid_raw_init_data_user = json.dumps(
    {
        "id": 1,
        "first_name": "test",
        "last_name": "test",
        "username": "test",
    }
)
_valid_raw_init_data = (
    f"user={_valid_raw_init_data_user}"
    f"&auth_date=1722282571"
    f"&query_id=AAGSu8c4AAAAAJK7xzjFzRTU"
    f"&hash=24a419664fe28a83fe5fea94c082bc54fcd1eb9e3166d4b8155b9e77cfec0808"
)
_bot_token_for_valid_data = "test"


@pytest.fixture
def mock_check_hash(mocker: "MockerFixture") -> "MockType":
    return mocker.patch.object(InitDataValidator, "check_hash", return_value=None)


def test_validate() -> None:
    validator = InitDataValidator(
        raw_init_data=_valid_raw_init_data, bot_token=_bot_token_for_valid_data
    )

    with does_not_raise():
        validator.validate()


def test_invalid_hash_validate() -> None:
    bot_token = f"another-{_bot_token_for_valid_data}"
    validator = InitDataValidator(raw_init_data=_valid_raw_init_data, bot_token=bot_token)

    with pytest.raises(InvalidHashInitDataError):
        validator.validate()


def test_auth_date_validate(mock_check_hash: "MockType") -> None:
    raw_init_data = f"hash=test&auth_date={int(time.time())}"
    validator = InitDataValidator(raw_init_data=raw_init_data, bot_token="test")

    with does_not_raise():
        validator.validate(timedelta(minutes=1))

    mock_check_hash.assert_called_once()


def test_invalid_auth_date_validate(mock_check_hash: "MockType") -> None:
    period_of_validity = timedelta(minutes=1)
    auth_date = datetime.now(UTC) - period_of_validity
    raw_init_data = f"hash=test&auth_date={int(auth_date.timestamp())}"
    validator = InitDataValidator(raw_init_data=raw_init_data, bot_token="test")

    with pytest.raises(ExpiredInitDataError):
        validator.validate(period_of_validity)
    mock_check_hash.assert_called_once()


def test_invalid_format_validate() -> None:
    validator = InitDataValidator(raw_init_data="test", bot_token="test")
    with pytest.raises(InvalidFormatInitDataError):
        validator.validate()
