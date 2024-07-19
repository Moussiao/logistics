from datetime import date

from ninja import Field, ModelSchema, Schema
from pydantic import constr

from apps.orders.api.schemas.customer import CustomerInput, CustomerOutput
from apps.orders.api.schemas.customer_address import (
    CustomerAddressInput,
    CustomerAddressOutput,
)
from apps.orders.api.schemas.product import ProductInput, ProductOutput
from apps.orders.models import Order
from core.types import SortDirecition


class OrderInput(ModelSchema):
    external_id: int = Field(ge=0)
    partner: constr(to_lower=True)
    customer: CustomerInput
    customer_address: CustomerAddressInput
    # Используем ограничения дабы максимальная сумма,
    # по всем заказам, не превышало валидное значение для Order.total_price
    products: list[ProductInput] = Field(max_length=25)

    class Meta:
        model = Order
        fields = ("external_verbose", "expected_delivery_date", "comment")


class OrderOutput(ModelSchema):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "delivery_date",
            "expected_delivery_date",
            "total_price",
        )


class DetailOrderOutput(ModelSchema):
    customer: CustomerOutput
    customer_address: CustomerAddressOutput
    products: list[ProductOutput]

    class Meta:
        model = Order
        fields = (
            "id",
            "external_id",
            "external_verbose",
            "status",
            "delivery_date",
            "expected_delivery_date",
            "total_price",
            "created_at",
            "updated_at",
            "comment",
        )


class CreateOrderOutput(Schema):
    id: int


class OrdersOutput(Schema):
    items: list[OrderOutput]

    page: int
    has_next_page: bool


class OrdersFilters(Schema):
    page: int = Field(1, gt=0)

    status: Order.Status | None = None
    partner_id: int | None = None
    delivery_date_start: date | None = None
    delivery_date_end: date | None = None
    expected_delivery_date_start: date | None = None
    expected_delivery_date_end: date | None = None

    expected_delivery_date_sort: SortDirecition | None = None
