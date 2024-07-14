from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ninja import ModelSchema
from pydantic import constr, field_validator

from apps.orders.models import Customer
from core.validators import validate_phone


class CustomerInput(ModelSchema):
    phone: str
    email: constr(to_lower=True) = ""
    # Необходимо, так как ModelSchema не подтягивает choices
    gender: Customer.Gender = Customer.Gender.UNKNOWN

    class Meta:
        model = Customer
        fields = ("name",)

    @field_validator("phone")
    @classmethod
    def check_phone(cls, value: str) -> str:
        try:
            validate_phone(value)
        except ValidationError as exc:
            raise ValueError(", ".join(exc.messages)) from exc

        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        if not value:
            return value

        try:
            validate_email(value)
        except ValidationError as exc:
            raise ValueError(", ".join(exc.messages)) from exc

        return value
