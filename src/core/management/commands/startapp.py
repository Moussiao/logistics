from typing import Any

from django.conf import settings
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    def handle(self, **options: Any) -> None:  # type: ignore[override]
        directory = settings.BASE_DIR.parent / "apps" / options["name"]  # type: ignore[misc]
        directory.mkdir()

        options.update(directory=str(directory))

        super().handle(**options)
