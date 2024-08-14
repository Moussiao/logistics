from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumbers import NumberParseException, PhoneNumber, is_valid_number, parse
from pycountry import countries

__all__ = ("validate_phone", "validate_country_code")


def validate_phone(phone: str) -> None:
    try:
        phone_number: PhoneNumber = parse(phone)
    except NumberParseException as exc:
        raise ValidationError(_("Not valid phone")) from exc

    if not is_valid_number(phone_number):
        raise ValidationError(_("Not valid phone"))


def validate_country_code(alpha_2: str) -> None:
    try:
        country = countries.get(alpha_2=alpha_2, default=None)
    except (KeyError, LookupError) as exc:
        raise ValidationError(_("Not valid alpha_2 country code")) from exc

    if country is None:
        raise ValidationError(_("Not valid alpha_2 country code"))
