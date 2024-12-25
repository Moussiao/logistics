from django.http import HttpRequest
from ninja import Query, Router

from backend.apps.delivery.api.schemas import PartnersFilters, PartnersResponse
from backend.apps.delivery.services.partners.get_partners import GetPartners

router = Router()


@router.get("", response=PartnersResponse)
def get_partners(request: HttpRequest, filters: Query[PartnersFilters]) -> PartnersResponse:
    return GetPartners(filters)()
