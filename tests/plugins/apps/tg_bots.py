from typing import Any, Protocol, final

import pytest
from django_fakery.faker_factory import Factory
from faker import Faker

from apps.tg_bots.models import TgChat


@final
class TgChatFactory(Protocol):
    def __call__(self, **fields: Any) -> TgChat: ...


@pytest.fixture()
def tg_chat_factory(faker: Faker, fakery: Factory[TgChat]) -> TgChatFactory:
    def factory(**fields: Any) -> TgChat:
        # django_fakery не верно обрабатывает models.PositiveBigIntegerField
        fields.setdefault("external_id", faker.pyint(min_value=1))
        return fakery.make(model=TgChat, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture()
def tg_chat(tg_chat_factory: TgChatFactory) -> TgChat:
    return tg_chat_factory()
