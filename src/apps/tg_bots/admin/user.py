from typing import final

from django.contrib import admin

from src.apps.tg_bots.models import TgUser


@final
@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin[TgUser]):
    fields = (
        "external_id",
        "user",
        "username",
        "is_bot",
        "first_name",
        "last_name",
        "language_code",
    )
