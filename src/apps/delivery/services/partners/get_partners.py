from typing import final

import attr
from django.core.paginator import Paginator
from pydantic import TypeAdapter

from apps.delivery.api.schemas import PartnerResponse, PartnersFilters, PartnersResponse
from apps.delivery.models import Partner

_partner_response_adapter = TypeAdapter(list[PartnerResponse])


@final
@attr.dataclass(slots=True, frozen=True)
class GetPartners:
    COUNT_PER_PAGE = 10

    _filters: PartnersFilters

    def __call__(self) -> PartnersResponse:
        partners_qs = (
            Partner.objects.filter(is_active=True)
            .values(*PartnerResponse.Meta.fields)
            .order_by("name")
        )

        paginator = Paginator(partners_qs, per_page=self.COUNT_PER_PAGE)
        page = paginator.get_page(self._filters.page)

        partners = _partner_response_adapter.validate_python(page.object_list)
        return PartnersResponse(
            items=partners,
            page=page.number,
            has_next_page=page.has_next(),
        )
