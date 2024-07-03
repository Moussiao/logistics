from typing import final

from django.contrib import admin

from apps.tg_bots.models import TgChat


@final
@admin.register(TgChat)
class TgChatAdmin(admin.ModelAdmin[TgChat]):
    fields = ("external_id", "type", "title", "description", "username", "invite_link")
