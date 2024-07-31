import hashlib
import hmac
from datetime import UTC, datetime, timedelta
from typing import final
from urllib.parse import unquote

from django.conf import settings


class InvalidInitDataError(Exception):
    pass


class InvalidFormatInitDataError(InvalidInitDataError):
    pass


class InvalidHashInitDataError(InvalidInitDataError):
    pass


class ExpiredInitDataError(InvalidInitDataError):
    pass


def parse_raw_init_data(raw_init_data: str) -> dict[str, str]:
    unquote_init_data = unquote(raw_init_data)
    return dict(param.split("=") for param in unquote_init_data.split("&"))


@final
class InitDataValidator:
    BASE_HASH_KEY = b"WebAppData"

    # Ключи для доступа к обязательным полям
    DATA_HASH_KEY = "hash"
    DATA_AUTH_DATE_KEY = "auth_date"

    # Переменные экземпляра
    _bot_token: str
    _raw_init_data: str
    _parsed_init_data: dict[str, str] | None

    def __init__(self, raw_init_data: str, bot_token: str = settings.BOT_TOKEN) -> None:
        self._bot_token = bot_token
        self._raw_init_data = raw_init_data

        self._parsed_init_data = None

    def validate(self, period_of_validity: timedelta | None = None) -> None:
        self.check_hash()
        if period_of_validity is not None:
            self.check_auth_date(period_of_validity)

    def check_hash(self) -> None:
        try:
            expected_hash = self.parsed_raw_init_data[self.DATA_HASH_KEY]
        except (KeyError, ValueError) as exc:
            raise InvalidFormatInitDataError("raw_init_data is invalid") from exc

        hash_by_bot_token = self._get_init_data_hash_by_bot_token()
        if not hmac.compare_digest(expected_hash, hash_by_bot_token):
            raise InvalidHashInitDataError("hash is not equal to expected_hash")

    def check_auth_date(self, period_of_validity: timedelta) -> None:
        try:
            auth_date_timestapm = self.parsed_raw_init_data[self.DATA_AUTH_DATE_KEY]
            auth_datetime = datetime.fromtimestamp(int(auth_date_timestapm), tz=UTC)
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidFormatInitDataError("raw_init_data is invalid") from exc

        min_valid_datetime = datetime.now(tz=UTC) - period_of_validity
        if auth_datetime < min_valid_datetime:
            raise ExpiredInitDataError(f"raw_init_data[{auth_datetime}] is expired")

    @property
    def parsed_raw_init_data(self) -> dict[str, str]:
        if self._parsed_init_data is None:
            self._parsed_init_data = parse_raw_init_data(self._raw_init_data)

        return self._parsed_init_data

    def _get_init_data_hash_by_bot_token(self) -> str:
        secret_key_hash = self._get_hash(key=self.BASE_HASH_KEY, msg=self._bot_token)
        secret_key = secret_key_hash.digest()

        init_data = self.parsed_raw_init_data.copy()
        init_data.pop(self.DATA_HASH_KEY, None)
        sorted_data_items = sorted(init_data.items())
        sorted_data_items_msg = "\n".join(f"{k}={v}" for k, v in sorted_data_items)

        return self._get_hash(key=secret_key, msg=sorted_data_items_msg).hexdigest()

    @classmethod
    def _get_hash(cls, key: bytes, msg: str) -> hmac.HMAC:
        return hmac.new(key=key, msg=msg.encode(), digestmod=hashlib.sha256)
