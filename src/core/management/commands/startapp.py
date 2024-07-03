from typing import Any

from django.conf import settings
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    def handle(self, **options: Any) -> None:
        directory = settings.BASE_DIR.parent / "apps" / options["name"]
        directory.mkdir()

        options.update(directory=str(directory))

        super().handle(**options)
