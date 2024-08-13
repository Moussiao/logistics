def safe_string_to_numbers(string: str) -> list[int]:
    numbers = []
    for number in string.replace(" ", "").split(","):
        try:
            numbers.append(int(number))
        except (KeyError, ValueError):
            continue

    return numbers
