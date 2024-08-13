from typing import final

from django.contrib import admin

from apps.delivery.models import Order


@final
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin[Order]):
    fields = (
        "external_id",
        "external_verbose",
        "status",
        "delivery_date",
        "expected_delivery_date",
        "customer",
        "customer_address",
        "products",
        "total_price",
        "partner",
        "comment",
    )
