from typing import final

from django.contrib import admin

from backend.apps.delivery.models import Customer


@final
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin[Customer]):
    fields = ("name", "email", "phone", "gender")
