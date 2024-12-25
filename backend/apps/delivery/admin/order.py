from typing import final

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin  # type: ignore[import-untyped]

from backend.apps.delivery.models import Order, OrderProduct


@final
class OrderProductInline(admin.StackedInline[OrderProduct, Order]):
    extra = 1
    model = OrderProduct
    verbose_name = _("Продукт")
    verbose_name_plural = _("Продукты")


@final
@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):  # type: ignore[misc]
    fields = (
        "external_id",
        "external_verbose",
        "state",
        "delivery_date",
        "expected_delivery_date",
        "customer",
        "customer_address",
        "total_price",
        "partner",
        "comment",
    )
    inlines = (OrderProductInline,)
