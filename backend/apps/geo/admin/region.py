from typing import final

from django.contrib import admin

from backend.apps.geo.models import Region


@final
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin[Region]):
    fields = ("name", "country", "time_zone")
