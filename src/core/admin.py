from typing import Any


class TimeReadOnlyMixin:
    readonly_fields: Any = ("created_at", "updated_at")
