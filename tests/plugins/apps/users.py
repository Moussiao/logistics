from typing import Any, Protocol, final

import pytest
from django_fakery.faker_factory import Factory

from src.apps.users.models import User


@final
class UserFactory(Protocol):
    def __call__(self, **fields: Any) -> User: ...


@final
class UsersFactory(Protocol):
    def __call__(self, objs_quantity: int, **fields: Any) -> list[User]: ...


@pytest.fixture
def user_factory(fakery: Factory[User]) -> UserFactory:
    def factory(**fields: Any) -> User:
        fields.setdefault("is_active", True)
        fields.setdefault("is_superuser", False)
        return fakery.make(model=User, fields=fields)  # type: ignore[call-overload]

    return factory


@pytest.fixture
def users_factory(fakery: Factory[User]) -> UsersFactory:
    def factory(objs_quantity: int, **fields: Any) -> list[User]:
        fields.setdefault("is_active", True)
        fields.setdefault("is_superuser", False)
        return fakery.make(model=User, fields=fields, quantity=objs_quantity)  # type: ignore[call-overload]

    return factory


@pytest.fixture
def user(user_factory: UserFactory) -> User:
    return user_factory()


@pytest.fixture
def logistician_user(user_factory: UserFactory) -> User:
    return user_factory(role=User.Role.LOGISTICIAN)


@pytest.fixture
def partner_user(user_factory: UserFactory) -> User:
    return user_factory(role=User.Role.DELIVERY_PARTNER)


@pytest.fixture
def unknown_user(user_factory: UserFactory) -> User:
    return user_factory(role=User.Role.UNKNOWN)
