from datetime import date

from ninja import Field, ModelSchema, Schema
from pydantic import constr

from apps.delivery.api.schemas.customer import CustomerRequest, CustomerResponse
from apps.delivery.api.schemas.customer_address import (
    CustomerAddressRequest,
    CustomerAddressResponse,
)
from apps.delivery.api.schemas.product import ProductRequest, ProductResponse
from apps.delivery.models import Order
from core.types import SortDirecition


class OrderRequest(ModelSchema):
    external_id: int = Field(ge=0)
    partner: constr(to_lower=True)
    customer: CustomerRequest
    customer_address: CustomerAddressRequest
    # Используем ограничения дабы максимальная сумма,
    # по всем заказам, не превышало валидное значение для Order.total_price
    products: list[ProductRequest] = Field(max_length=25)

    class Meta:
        model = Order
        fields = ("external_verbose", "expected_delivery_date", "comment")


class OrderResponse(ModelSchema):
    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "delivery_date",
            "expected_delivery_date",
            "total_price",
        )


class DetailOrderResponse(ModelSchema):
    customer: CustomerResponse
    customer_address: CustomerAddressResponse
    products: list[ProductResponse]

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


class CreateOrderResponse(Schema):
    id: int


class OrdersResponse(Schema):
    items: list[OrderResponse]

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
