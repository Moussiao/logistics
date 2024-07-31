from contextlib import nullcontext as does_not_raise

import pytest
from django.core.exceptions import ValidationError

from core.validators import validate_country_code, validate_phone


@pytest.mark.parametrize("valid_phone", ["+79111111111"])
def test_validate_phone(valid_phone: str) -> None:
    with does_not_raise():
        validate_phone(valid_phone)


@pytest.mark.parametrize("valid_country_code", ["RU", "US", "CN", "JP", "FR"])
def test_validate_country_code(valid_country_code: str) -> None:
    with does_not_raise():
        validate_country_code(alpha_2=valid_country_code)


@pytest.mark.parametrize("invalid_phone", ["invalid", "111", "+711"])
def test_invalid_validate_phone(invalid_phone: str) -> None:
    with pytest.raises(ValidationError):
        validate_phone(invalid_phone)


@pytest.mark.parametrize("invalid_country_code", ["invalid", "RUU", "XX"])
def test_invalid_validate_country_code(invalid_country_code: str) -> None:
    with pytest.raises(ValidationError):
        validate_country_code(alpha_2=invalid_country_code)
