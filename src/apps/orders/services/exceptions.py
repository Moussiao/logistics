from enum import StrEnum

from django.utils.translation import gettext_lazy as _


class ErrorType(StrEnum):
    UNKNOWN = "unknown"
    DUPLICATE = "duplicate_field"
    INVALID_RELATED = "invalid_related"
    NOT_FOUND_RELATED = "not_found_related"


class CreateOrderError(Exception):
    """
    Ошибка при создании заказа.

    Такая сложная специфика нужна для читаемых ошибок при взаимодейсвии по API.
    """

    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.UNKNOWN,
        field: str = "",
    ) -> None:
        self.msg = msg
        self.field = field
        self.error_type = error_type
        super().__init__(f"{error_type}: {field} - {msg}")


class DuplicateExternalIdOrderError(CreateOrderError):
    """
    Заказ с указанным external_id уже сущесвуюет.

    Инкапсулирует в себе базовые значения для ошибки.
    """

    BASE_MSG = _("Заказ с указанным значением поля уже существует")
    BASE_ERROR_TYPE = ErrorType.DUPLICATE
    BASE_FIELD = "external_id"

    def __init__(
        self,
        msg: str = str(BASE_MSG),
        error_type: ErrorType = BASE_ERROR_TYPE,
        field: str = BASE_FIELD,
    ) -> None:
        super().__init__(msg=msg, error_type=error_type, field=field)


class PartnerNotExistsOrderError(CreateOrderError):
    """
    Не удалось найти запись orders.models.Partner для связи с заказом.

    Инкапсулирует в себе базовые значения для ошибки.
    """

    BASE_MSG = _("Не удалось найти 'партнера' к которому будет отнесен заказ")
    BASE_ERROR_TYPE = ErrorType.NOT_FOUND_RELATED
    BASE_FIELD = "partner"

    def __init__(
        self,
        msg: str = str(BASE_MSG),
        error_type: ErrorType = BASE_ERROR_TYPE,
        field: str = BASE_FIELD,
    ) -> None:
        super().__init__(msg=msg, error_type=error_type, field=field)


class InvalidCountryCodeOrderError(CreateOrderError):
    """
    Не удалось получить запись geo.models.Country по указанному коду.

    Инкапсулирует в себе базовые значения для ошибки.
    """

    BASE_MSG = _("Указан не валидный код страны")
    BASE_ERROR_TYPE = ErrorType.INVALID_RELATED
    BASE_FIELD = "customer_address.country"

    def __init__(
        self,
        msg: str = str(BASE_MSG),
        error_type: ErrorType = BASE_ERROR_TYPE,
        field: str = BASE_FIELD,
    ) -> None:
        super().__init__(msg=msg, error_type=error_type, field=field)
