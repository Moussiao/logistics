import pytest

from core.utils import safe_string_to_integers


@pytest.mark.parametrize(
    ("numbers_str", "expected_numbers"),
    [
        ("", []),
        ("1", [1]),
        ("text", []),
        ("1.1,2.2,3.3,4.4,5.5", []),
        ("1,2,3,4,5", [1, 2, 3, 4, 5]),
        ("-1,-2,-3,4,5", [-1, -2, -3, 4, 5]),
        ("1,2,3,4,5, text", [1, 2, 3, 4, 5]),
        ("text, 1,2,3,4,5, text", [1, 2, 3, 4, 5]),
        ("1  , 2  , 3 , 4 , 5  ", [1, 2, 3, 4, 5]),
    ],
)
def test_safe_string_to_numbers(numbers_str: str, expected_numbers: list[int]) -> None:
    numbers = safe_string_to_integers(numbers_str)
    assert numbers == expected_numbers
