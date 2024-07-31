import json
from datetime import timedelta
from logging import getLogger
from typing import TYPE_CHECKING, final

import attr

from apps.security.jwt import create_user_access_token
from apps.tg_bots.mini_app import InitDataValidator, InvalidInitDataError
from apps.users.models import User

if TYPE_CHECKING:
    from apps.security.api.schemas import TokenRequest

log = getLogger(__name__)


class CreateAccessTokenError(Exception):
    pass


class InvalidDataError(CreateAccessTokenError):
    pass


class InvalidParsedInitDataSignatureError(CreateAccessTokenError):
    pass


class OneUserNotFoundError(CreateAccessTokenError):
    pass


@final
@attr.dataclass(frozen=True, slots=True)
class CreateAccessToken:
    INIT_DATA_PERIOD_OF_VALIDITY = timedelta(hours=8)

    _data: "TokenRequest"

    def __call__(self) -> str:
        parsed_tma_init_data = self._validate_tma_init_data()
        tg_user_id = self._get_tg_user_id(parsed_tma_init_data)

        user_id = self._get_user_id(tg_user_id)
        return create_user_access_token(user_id=user_id)

    def _validate_tma_init_data(self) -> dict[str, str]:
        tma_validator = InitDataValidator(raw_init_data=self._data.tma_init_data)
        try:
            tma_validator.validate(self.INIT_DATA_PERIOD_OF_VALIDITY)
        except InvalidInitDataError as exc:
            error_msg = f"{self._data.tma_init_data} - invalid init_data"
            log.exception(error_msg)
            raise InvalidDataError(error_msg) from exc

        return tma_validator.parsed_raw_init_data

    @classmethod
    def _get_tg_user_id(cls, parsed_tma_init_data: dict[str, str]) -> int:
        try:
            raw_tg_user = json.loads(parsed_tma_init_data["user"])
            tg_user_id = int(raw_tg_user["id"])
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            error_msg = f"{parsed_tma_init_data} - invalid signature init_data"
            log.exception(error_msg)
            raise InvalidParsedInitDataSignatureError(error_msg) from exc

        return tg_user_id

    @classmethod
    def _get_user_id(cls, tg_user_id: int) -> int:
        try:
            user = (
                User.objects.filter(
                    is_active=True,
                    tg_user__external_id=tg_user_id,
                    tg_user__is_bot=False,
                )
                .values("id")
                .get()
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned) as exc:
            raise OneUserNotFoundError("User not found or duplicate") from exc

        return user["id"]
