from typing import Any, Protocol

import pytest
from django_fakery.faker_factory import Factory

from backend.apps.geo.models import Country, TimeZone


class CountryFactory(Protocol):
    def __call__(self, **fields: Any) -> Country: ...


class TimeZoneFactory(Protocol):
    def __call__(self, **fields: Any) -> TimeZone: ...


@pytest.fixture
def country_factory(fakery: Factory[Country]) -> CountryFactory:
    def factory(**fields: Any) -> Country:
        return fakery.make(model=Country, fields=fields)  # type: ignore[call-overload, no-any-return]

    return factory


@pytest.fixture
def time_zone_factory(fakery: Factory[TimeZone]) -> TimeZoneFactory:
    def factory(**fields: Any) -> TimeZone:
        return fakery.make(model=TimeZone, fields=fields)  # type: ignore[call-overload, no-any-return]

    return factory


@pytest.fixture
def russia_country(country_factory: CountryFactory) -> Country:
    return country_factory(name="Russia", code="RU")


@pytest.fixture
def utc_time_zone(time_zone_factory: TimeZoneFactory) -> TimeZone:
    return time_zone_factory(name="UTC", minutes_offset_from_utc=0, is_canonical=True)
