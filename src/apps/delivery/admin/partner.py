from typing import final

from django.contrib import admin

from apps.delivery.models import Partner


@final
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin[Partner]):
    fields = ("name", "user", "tg_chat", "working_time_zone", "regions")
