from typing import Annotated

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ninja import Field, Schema
from pydantic import StringConstraints, field_validator

from src.apps.delivery.models import Customer
from src.core.validators import validate_phone


class CustomerRequest(Schema):
    name: str = Field(max_length=200)
    phone: str = Field(max_length=32)
    email: Annotated[str, StringConstraints(to_lower=True)] = Field(max_length=254, default="")
    gender: Customer.Gender = Customer.Gender.UNKNOWN

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


class CustomerResponse(Schema):
    id: int = Field(ge=0)
    gender: Customer.Gender
    name: str = Field(max_length=200)
    email: str = Field(max_length=254)
    phone: str = Field(max_length=32)
