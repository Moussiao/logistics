from base64 import b64decode, b64encode
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, cast
from urllib import parse

from django.core.paginator import InvalidPage
from django.db.models import Model, QuerySet
from django.db.models.query import ModelIterable, ValuesIterable
from pydantic import PositiveInt


class PaginatorInvalidPage(InvalidPage):
    pass


class InvalidRawCursorError(PaginatorInvalidPage):
    pass


@dataclass(frozen=True, slots=True)
class Cursor:
    position: str | None
    reverse: bool
    # Смещение в курсоре используется когда есть не уникальные значения,
    # используемые при позиционировании курсора.
    # Например: User.objects.order_by('created_at') где есть записи
    # с идентичным (с точностью до миллисекунды) значением created_at.
    offset: PositiveInt


DEFAULT_CURSOR = Cursor(offset=0, reverse=False, position=None)


@dataclass(frozen=True, slots=True)
class CursorPage[T: Model | dict[str, Any]]:
    objects: tuple[T, ...]
    next_cursor: str | None
    previous_cursor: str | None


def reverse_ordering(queryset_ordering: tuple[str, ...]) -> tuple[str, ...]:
    """
    Используется для сортировки queryset в обратную сторону.

    >>> reverse_ordering(('-created_at', 'id'))
    ('created_at', '-id')
    """

    def invert(x: str) -> str:
        return x[1:] if x.startswith("-") else f"-{x}"

    return tuple(invert(item) for item in queryset_ordering)


class CursorPaginator[T: Model]:
    """
    Пагинация курсором по queryset.

    Поле сортировки, в идеале, должно удовлетворять следующим требованиям:
    1. Должно быть неизменяемым значением, например, временной меткой, slug
    или другим полем, которое устанавливается только один раз, при создании.
    2. Должны быть уникальными или почти уникальными. Хорошим примером являются
    временные метки с точностью до миллисекунды. Эта реализация пагинации курсора
    использует умный стиль "позиция плюс смещение", который позволяет правильно
    поддерживать не строго уникальные значения в качестве упорядочивания.
    3. Должно быть полем, которое может быть преобразовано в строку, а также не являться None.
    4. Поле должно иметь индекс.

    Вдохновлен реализацией CursorPagination из Django Rest Framework:
    https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
    """

    DEFAULT_PAGE_SIZE = 10
    DEFAULT_ORDERING = "-pk"

    # Используем жесткое ограничение, в виде максимального значения смещения,
    # для защиты от дорогих запросов к БД (например, от злоумышленников).
    MAX_CURSOR_OFFSET = 1000

    # Поля экземпляра
    _queryset: QuerySet[T, Any]
    _queryset_ordering: tuple[str, ...]
    _page_size: PositiveInt

    def __init__(
        self,
        queryset: QuerySet[T, Any],
        page_size: PositiveInt = DEFAULT_PAGE_SIZE,
    ) -> None:
        if page_size < 1:
            raise TypeError(f"{self.__class__.__name__} is not supported {page_size=}")

        iterable_class = queryset._iterable_class  # noqa: SLF001
        if not issubclass(iterable_class, (ModelIterable | ValuesIterable)):
            raise TypeError(
                f"{self.__class__.__name__} supported only model queryset or queryset.values()"
            )

        if not queryset.query.order_by:
            queryset = queryset.order_by(self.DEFAULT_ORDERING)

        self._queryset = queryset
        self._queryset_ordering = cast(tuple[str, ...], queryset.query.order_by)
        self._page_size = page_size

    def __iter__(self) -> Generator[CursorPage[T], None, None]:
        first_page = self.get_page()
        yield first_page

        next_cursor = first_page.next_cursor
        while next_cursor is not None:
            page = self.get_page(next_cursor)
            yield page
            next_cursor = page.next_cursor

    def get_page(self, raw_cursor: str | None = None) -> CursorPage[T]:
        cursor = DEFAULT_CURSOR if raw_cursor is None else self.decode_cursor(raw_cursor)
        if cursor.reverse:
            queryset = self._queryset.order_by(*reverse_ordering(self._queryset_ordering))
        else:
            queryset = self._queryset

        if cursor.position is not None:
            # Необходима завязка только на первое значение сортировки,
            # так как cursor.position является значением данного поля модели.
            init_queryset_first_ordering = self._queryset_ordering[0]
            is_init_queryset_reversed = init_queryset_first_ordering.startswith("-")
            first_ordering_field = init_queryset_first_ordering.lstrip("-")

            if cursor.reverse != is_init_queryset_reversed:
                queryset = queryset.filter(**{f"{first_ordering_field}__lt": cursor.position})
            else:
                queryset = queryset.filter(**{f"{first_ordering_field}__gt": cursor.position})

        # Получаем один дополнительный элемент, чтобы определить, есть ли следующая страница.
        results = tuple(queryset[cursor.offset : cursor.offset + self._page_size + 1])
        page_results = results[: self._page_size]

        if len(results) > len(page_results):
            next_position = self._get_position_from_instance(results[-1])
        else:
            next_position = None

        previous_position = cursor.position

        if cursor.reverse:
            # Если курсор был определен в обратную сторону, то выше мы изменили
            # order_by у queryset, дабы при использовании offset получить нужные записи.
            # Но для пользователя необходим верный порядок, поэтому снова изменяем порядок.
            page_results = tuple(reversed(page_results))
            # Меняем местами указатели
            next_position, previous_position = (previous_position, next_position)

        next_cursor = None
        if next_position is not None:
            next_cursor = self._get_next_cursor(
                cursor=cursor,
                page_results=page_results,
                next_position=next_position,
                previous_position=previous_position,
            )

        previous_cursor = None
        if previous_position is not None or cursor.offset != 0:
            previous_cursor = self._get_previous_cursor(
                cursor=cursor,
                page_results=page_results,
                next_position=next_position,
                previous_position=previous_position,
            )

        return CursorPage(
            objects=page_results,
            next_cursor=next_cursor,
            previous_cursor=previous_cursor,
        )

    def decode_cursor(self, raw_cursor: str) -> Cursor:
        try:
            querystring = b64decode(raw_cursor).decode()
            tokens = parse.parse_qs(querystring, keep_blank_values=True)

            offset = int(tokens.get("o", ["0"])[0])
            if offset < 0:
                raise InvalidRawCursorError("offset must not be less than zero")
            offset = min(int(offset), self.MAX_CURSOR_OFFSET)

            reverse = tokens.get("r", ["0"])[0]
            is_reverse = bool(int(reverse))

            position = tokens.get("p", [None])[0]
        except (KeyError, ValueError) as exc:
            raise InvalidRawCursorError(f"{raw_cursor=} failed to decode") from exc

        return Cursor(offset=offset, reverse=is_reverse, position=position)

    def encode_cursor(self, cursor: Cursor) -> str:
        tokens = {}

        if cursor.offset > 0:
            tokens["o"] = str(cursor.offset)
        if cursor.reverse:
            tokens["r"] = "1"
        if cursor.position is not None:
            tokens["p"] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)
        encode = b64encode(querystring.encode())
        return encode.decode()

    def _get_position_from_instance(self, instance: Model | dict[str, Any]) -> str:
        field_name = self._queryset_ordering[0].lstrip("-")
        if isinstance(instance, dict):
            field_value = instance[field_name]
        else:
            field_value = getattr(instance, field_name)

        return str(field_value)

    def _get_next_cursor(
        self,
        page_results: tuple[T],
        cursor: Cursor,
        next_position: str,
        previous_position: str | None,
    ) -> str:
        if page_results and cursor.reverse and cursor.offset:
            compare_position = self._get_position_from_instance(page_results[-1])
        else:
            compare_position = next_position

        offset = 0
        position: str | None = next_position
        has_item_with_unique_position = False
        for item in reversed(page_results):
            position = self._get_position_from_instance(item)
            if position != compare_position:
                has_item_with_unique_position = True
                break

            offset += 1  # noqa: SIM113

        if not has_item_with_unique_position:
            if previous_position is None and cursor.offset == 0:
                # Мы находися на первой странице
                offset = self._page_size
                position = None
            elif cursor.reverse:
                offset = 0
                position = previous_position
            else:
                offset = cursor.offset + self._page_size
                position = previous_position

        cursor = Cursor(offset=offset, reverse=False, position=position)
        return self.encode_cursor(cursor)

    def _get_previous_cursor(
        self,
        page_results: tuple[T],
        cursor: Cursor,
        next_position: str | None,
        previous_position: str | None,
    ) -> str:
        if page_results and not cursor.reverse and cursor.offset:
            compare_position = self._get_position_from_instance(page_results[-1])
        else:
            compare_position = next_position  # type: ignore[assignment]

        offset = 0
        position: str | None = previous_position
        has_item_with_unique_position = False
        for item in page_results:
            position = self._get_position_from_instance(item)
            if position != compare_position:
                has_item_with_unique_position = True
                break

            offset += 1  # noqa: SIM113

        if page_results and not has_item_with_unique_position:
            if next_position is None:
                # Мы находися на последней странице
                offset = self._page_size
                position = None
            elif cursor.reverse:
                offset = cursor.offset + self._page_size
                position = next_position
            else:
                offset = 0
                position = next_position

        cursor = Cursor(offset=offset, reverse=True, position=position)
        return self.encode_cursor(cursor)
