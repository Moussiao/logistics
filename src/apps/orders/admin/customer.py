from typing import final

from django.contrib import admin

from apps.orders.models import Customer


@final
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin[Customer]):
    fields = ("phone",)
