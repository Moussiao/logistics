from django.core.exceptions import ValidationError
from ninja import Field, Schema
from pydantic import field_validator

from src.core.validators import validate_country_code


class CustomerAddressRequest(Schema):
    postcode: str = Field(max_length=10)
    country_code: str = Field(min_length=2, max_length=2, description="alpha_2 code")
    region_name: str = Field(max_length=200)
    city_name: str = Field(max_length=200)
    street: str = Field(max_length=200)
    house_number: str = Field(max_length=50)
    flat_number: str = Field(max_length=10, default="")
    comment: str = Field(max_length=255, default="")

    @field_validator("country_code")
    @classmethod
    def check_country_code(cls, value: str) -> str:
        try:
            validate_country_code(alpha_2=value)
        except ValidationError as exc:
            raise ValueError(", ".join(exc.messages)) from exc

        return value


class CustomerAddressResponse(Schema):
    id: int = Field(ge=0)
    postcode: str
    country_name: str = Field(alias="country.name")
    region_name: str = Field(alias="region.name")
    city_name: str = Field(alias="city.name")
    street: str = Field(max_length=200)
    house_number: str = Field(max_length=50)
    flat_number: str = Field(max_length=10)
    comment: str = Field(max_length=255)
