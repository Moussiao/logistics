from typing import final

import attr
from django.core.paginator import Paginator
from pydantic import TypeAdapter

from apps.orders.api.schemas import PartnerOutput, PartnersFilters, PartnersOutput
from apps.orders.models import Partner

_partner_output_adapter = TypeAdapter(list[PartnerOutput])


@final
@attr.dataclass(slots=True, frozen=True)
class ListPartners:
    COUNT_PER_PAGE = 10

    _filters: PartnersFilters

    def __call__(self) -> PartnersOutput:
        partners_qs = (
            Partner.objects.filter(is_active=True)
            .values(*PartnerOutput.Meta.fields)
            .order_by("name")
        )

        paginator = Paginator(partners_qs, per_page=self.COUNT_PER_PAGE)
        page = paginator.get_page(self._filters.page)

        partners = _partner_output_adapter.validate_python(page.object_list)
        return PartnersOutput(
            items=partners,
            page=page.number,
            has_next_page=page.has_next(),
        )
