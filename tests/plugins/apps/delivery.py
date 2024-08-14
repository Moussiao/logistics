from typing import Any, Protocol, final

import pytest
from django_fakery.faker_factory import Factory

from apps.delivery.models import Order, Partner


@final
class OrderFactory(Protocol):
    def __call__(self, **fields: Any) -> Order: ...


@final
class OrdersFactory(Protocol):
    def __call__(self, objs_quantity: int, **fields: Any) -> list[Order]: ...


@final
class PartnerFactory(Protocol):
    def __call__(self, **fields: Any) -> Partner: ...


@final
class PartnersFactory(Protocol):
    def __call__(self, objs_quantity: int, **fields: Any) -> list[Partner]: ...


@pytest.fixture()
def order_factory(fakery: Factory[Order]) -> OrderFactory:
    def factory(**fields: Any) -> Order:
        return fakery.make(model=Order, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def orders_factory(fakery: Factory[Order]) -> OrdersFactory:
    def factory(objs_quantity: int, **fields: Any) -> list[Order]:
        return fakery.make(model=Order, fields=fields, quantity=objs_quantity)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def partner_factory(fakery: Factory[Partner]) -> PartnerFactory:
    def factory(**fields: Any) -> Partner:
        return fakery.make(model=Partner, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def partners_factory(fakery: Factory[Partner]) -> PartnersFactory:
    def factory(objs_quantity: int, **fields: Any) -> list[Partner]:
        fields.setdefault("active", True)
        return fakery.make(model=Order, fields=fields, quantity=objs_quantity)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def order(order_factory: OrderFactory) -> Order:
    return order_factory()


@pytest.fixture()
def partner(partner_factory: PartnerFactory) -> Partner:
    return partner_factory()


@pytest.fixture()
def another_partner(partner_factory: PartnerFactory) -> Partner:
    return partner_factory()
