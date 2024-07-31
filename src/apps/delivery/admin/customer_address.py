from django.contrib import admin

from apps.delivery.models.customer_address import CustomerAddress


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin[CustomerAddress]):
    fields = (
        "customer",
        "postcode",
        "country",
        "region",
        "city",
        "street",
        "house_number",
        "flat_number",
        "comment",
    )
