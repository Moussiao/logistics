from typing import Any, Protocol

import pytest
from django_fakery.faker_factory import Factory
from faker import Faker

from src.apps.tg_bots.models import TgChat, TgUser


class TgChatFactory(Protocol):
    def __call__(self, **fields: Any) -> TgChat: ...


class TgUserFactory(Protocol):
    def __call__(self, **fields: Any) -> TgUser: ...


@pytest.fixture
def tg_chat_factory(faker: Faker, fakery: Factory[TgChat]) -> TgChatFactory:
    def factory(**fields: Any) -> TgChat:
        # django_fakery не верно обрабатывает models.PositiveBigIntegerField
        fields.setdefault("external_id", faker.pyint(min_value=1))
        return fakery.make(model=TgChat, fields=fields)  # type: ignore[call-overload, no-any-return]

    return factory


@pytest.fixture
def tg_user_factory(faker: Faker, fakery: Factory[TgUser]) -> TgUserFactory:
    def factory(**fields: Any) -> TgUser:
        fields.setdefault("is_bot", False)
        # django_fakery не верно обрабатывает models.PositiveBigIntegerField
        fields.setdefault("external_id", faker.pyint(min_value=1))
        return fakery.make(model=TgUser, fields=fields)  # type: ignore[call-overload, no-any-return]

    return factory


@pytest.fixture
def tg_chat(tg_chat_factory: TgChatFactory) -> TgChat:
    return tg_chat_factory()


@pytest.fixture
def tg_user(tg_user_factory: TgUserFactory) -> TgUser:
    return tg_user_factory()
