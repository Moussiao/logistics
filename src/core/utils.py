from enum import StrEnum
from typing import TypeVar

T = TypeVar("T", bound=StrEnum)


def safe_string_to_enums(string: str, str_enum: type[T]) -> list[T]:
    str_enums = []
    for x in string.replace(" ", "").split(","):
        try:
            str_enums.append(str_enum(x))
        except ValueError:
            continue

    return str_enums


def safe_string_to_integers(string: str) -> list[int]:
    numbers = []
    for number in string.replace(" ", "").split(","):
        try:
            numbers.append(int(number))
        except (KeyError, ValueError):
            continue

    return numbers
