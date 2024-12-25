from typing import TYPE_CHECKING

import pytest
from django.utils.timezone import now

from backend.apps.users.models import User
from backend.core.paginator import CursorPaginator

if TYPE_CHECKING:
    from backend.apps.users.tests.fixtures import UsersFactory

pytestmark = [pytest.mark.django_db]


def test_paginator(users_factory: "UsersFactory") -> None:
    users_factory(CursorPaginator.DEFAULT_PAGE_SIZE)
    qs = User.objects.order_by("date_joined")
    paginator = CursorPaginator(qs)

    page = paginator.get_page()

    assert len(page.objects) == CursorPaginator.DEFAULT_PAGE_SIZE
    assert page.next_cursor is None
    assert page.previous_cursor is None


def test_page_size(users_factory: "UsersFactory") -> None:
    page_size = 20
    users_factory(page_size * 2)
    qs = User.objects.order_by("date_joined")
    paginator = CursorPaginator(qs, page_size)

    page = paginator.get_page()

    assert len(page.objects) == page_size
    assert page.next_cursor is not None
    assert page.previous_cursor is None


def test_decoded_next_cursor(users_factory: "UsersFactory") -> None:
    users_factory(CursorPaginator.DEFAULT_PAGE_SIZE * 2, date_joined=now())
    qs = User.objects.order_by("date_joined")
    paginator = CursorPaginator(qs)

    page = paginator.get_page()

    assert page.next_cursor is not None
    decoded_next_cursor = paginator.decode_cursor(page.next_cursor)
    assert decoded_next_cursor.reverse is False
    assert decoded_next_cursor.offset == CursorPaginator.DEFAULT_PAGE_SIZE
    assert decoded_next_cursor.position is None


def test_iter(users_factory: "UsersFactory") -> None:
    expected_pages_count = 10
    users_factory(CursorPaginator.DEFAULT_PAGE_SIZE * expected_pages_count)
    paginator = CursorPaginator(User.objects.order_by("date_joined"))

    all_pages = list(paginator)

    assert len(all_pages) == expected_pages_count
    assert all_pages[-1].next_cursor is None
    assert all_pages[-1].previous_cursor is not None
    decoded_previous_cursor = paginator.decode_cursor(all_pages[-1].previous_cursor)
    assert decoded_previous_cursor.reverse is True


def test_empty_db() -> None:
    qs = User.objects.all()
    paginator = CursorPaginator(qs)

    page = paginator.get_page()

    assert page.objects == ()
    assert page.next_cursor is None
    assert page.previous_cursor is None


@pytest.mark.parametrize("invalid_page_size", [0, -1, -100])
def test_invalid_page_size(invalid_page_size: int) -> None:
    qs = User.objects.all()

    with pytest.raises(TypeError):
        CursorPaginator(qs, page_size=invalid_page_size)


def test_many_get_page(users_factory: "UsersFactory") -> None:
    users_factory(CursorPaginator.DEFAULT_PAGE_SIZE * 3)
    paginator = CursorPaginator(User.objects.order_by("date_joined"))

    first_page = paginator.get_page()
    second_page = paginator.get_page(first_page.next_cursor)
    third_page = paginator.get_page(second_page.next_cursor)

    expected_second_page = paginator.get_page(third_page.previous_cursor)
    assert second_page.objects == expected_second_page.objects

    expected_first_page = paginator.get_page(second_page.previous_cursor)
    assert first_page.objects == expected_first_page.objects

    expected_third_page = paginator.get_page(expected_second_page.next_cursor)
    assert third_page.objects == expected_third_page.objects
