from ninja import Field, ModelSchema, Schema

from src.apps.delivery.models import Partner


class PartnerResponse(ModelSchema):
    class Meta:
        model = Partner
        fields = ("id", "name")


class PartnersResponse(Schema):
    items: list[PartnerResponse]

    page: int
    has_next_page: bool


class PartnersFilters(Schema):
    page: int = Field(1, gt=0)
