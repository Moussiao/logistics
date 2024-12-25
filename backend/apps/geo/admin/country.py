from typing import final

from django.contrib import admin

from backend.apps.geo.models import Country


@final
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin[Country]):
    readonly_fields = ("created_at", "updated_at")
    fields = ("code", "name", "created_at", "updated_at")
