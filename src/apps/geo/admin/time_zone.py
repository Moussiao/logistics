from typing import final

from django.contrib import admin

from apps.geo.models import TimeZone


@final
@admin.register(TimeZone)
class TimeZoneAdmin(admin.ModelAdmin[TimeZone]):
    fields = ("name", "minutes_offset_from_utc", "is_canonical")
