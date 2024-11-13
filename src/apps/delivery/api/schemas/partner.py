from ninja import Field, Schema


class PartnerResponse(Schema):
    id: int = Field(ge=0)
    name: str = Field(max_length=150)


class PartnersResponse(Schema):
    items: list[PartnerResponse]

    page: int
    has_next_page: bool


class PartnersFilters(Schema):
    page: int = Field(1, gt=0)
