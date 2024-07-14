from django.core.exceptions import ValidationError
from ninja import Field, ModelSchema
from pydantic import field_validator

from apps.orders.models import CustomerAddress
from core.validators import validate_country_code


class CustomerAddressInput(ModelSchema):
    country_code: str = Field(min_length=2, max_length=2, description="alpha_2 code")
    region_name: str
    city_name: str

    class Meta:
        model = CustomerAddress
        fields = ("postcode", "street", "house_number", "flat_number", "comment")

    @field_validator("country_code")
    @classmethod
    def check_country_code(cls, value: str) -> str:
        try:
            validate_country_code(alpha_2=value)
        except ValidationError as exc:
            raise ValueError(", ".join(exc.messages)) from exc

        return value
