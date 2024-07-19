from ninja import Field, ModelSchema, Schema

from apps.orders.models import Partner


class PartnerOutput(ModelSchema):
    class Meta:
        model = Partner
        fields = ("id", "name")


class PartnersOutput(Schema):
    items: list[PartnerOutput]

    page: int
    has_next_page: bool


class PartnersFilters(Schema):
    page: int = Field(1, gt=0)
