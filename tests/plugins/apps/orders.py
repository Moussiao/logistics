from typing import Any, Protocol, final

import pytest
from django_fakery.faker_factory import Factory

from apps.orders.models import Partner


@final
class PartnerFactory(Protocol):
    def __call__(self, **fields: Any) -> Partner: ...


@pytest.fixture()
def partner_factory(fakery: Factory[Partner]) -> PartnerFactory:
    def factory(**fields: Any) -> Partner:
        return fakery.make(model=Partner, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def partner(partner_factory: PartnerFactory) -> Partner:
    return partner_factory()
