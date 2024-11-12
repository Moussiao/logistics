from typing import final

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from src.apps.delivery.models import Order, OrderProduct


class OrderProductInline(admin.StackedInline):
    extra = 1
    model = OrderProduct
    verbose_name = _("Заказ")
    verbose_name_plural = _("Заказы")


@final
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin[Order]):
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
