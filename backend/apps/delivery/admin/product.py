from typing import final

from django.contrib import admin

from backend.apps.delivery.models import Product


@final
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    fields = ("name", "price")
