from typing import final

from django.contrib import admin

from src.apps.geo.models import City


@final
@admin.register(City)
class CityAdmin(admin.ModelAdmin[City]):
    fields = ("name", "region")
