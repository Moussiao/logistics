from typing import Any, Protocol, final

import pytest
from django_fakery.faker_factory import Factory

from apps.geo.models import TimeZone


@final
class TimeZoneFactory(Protocol):
    def __call__(self, **fields: Any) -> TimeZone: ...


@pytest.fixture()
def time_zone_factory(fakery: Factory[TimeZone]) -> TimeZoneFactory:
    def factory(**fields: Any) -> TimeZone:
        return fakery.make(model=TimeZone, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def utc_time_zone(time_zone_factory: TimeZoneFactory) -> TimeZone:
    return time_zone_factory(name="UTC", minutes_offset_from_utc=0, is_canonical=True)
