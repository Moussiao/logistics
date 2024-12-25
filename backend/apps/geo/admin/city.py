from typing import final

from django.contrib import admin

from backend.apps.geo.models import City


@final
@admin.register(City)
class CityAdmin(admin.ModelAdmin[City]):
    fields = ("name", "region")
