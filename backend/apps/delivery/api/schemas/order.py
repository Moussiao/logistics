from datetime import date, datetime
from decimal import Decimal

from ninja import Field, Schema

from backend.apps.delivery.api.schemas.customer import CustomerRequest, CustomerResponse
from backend.apps.delivery.api.schemas.customer_address import (
    CustomerAddressRequest,
    CustomerAddressResponse,
)
from backend.apps.delivery.api.schemas.product import OrderProductResponse, ProductRequest
from backend.apps.delivery.models import Order


class OrderRequest(Schema):
    external_id: int = Field(ge=0)
    external_verbose: str = Field(max_length=150)
    partner_id: int = Field(ge=0)
    expected_delivery_date: date
    comment: str = Field(max_length=255)
    customer: CustomerRequest
    customer_address: CustomerAddressRequest
    # Используем ограничения дабы максимальная сумма,
    # по всем заказам, не превышало валидное значение для Order.total_price
    products: list[ProductRequest] = Field(max_length=25)


class EditOrderRequest(Schema):
    comment: str | None = Field(None, max_length=255)


class OrderResponse(Schema):
    id: int = Field(ge=0)
    state: Order.State
    delivery_date: date | None
    expected_delivery_date: date
    total_price: Decimal


class DetailOrderResponse(Schema):
    id: int = Field(ge=0)
    external_id: int = Field(ge=0)
    external_verbose: str = Field(max_length=150)
    state: Order.State
    state_changed_at: datetime
    delivery_date: date | None
    expected_delivery_date: date
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    comment: str = Field(max_length=255)
    customer: CustomerResponse
    customer_address: CustomerAddressResponse
    products: list[OrderProductResponse]


class CreateOrderResponse(Schema):
    id: int


class OrdersResponse(Schema):
    items: list[OrderResponse]
    next_cursor: str | None = None
    previous_cursor: str | None = None


class OrdersFilters(Schema):
    cursor: str | None = None

    ids: str | None = None
    states: str | None = None
    partner_id: int | None = None
    delivery_date_start: date | None = None
    delivery_date_end: date | None = None
    expected_delivery_date_start: date | None = None
    expected_delivery_date_end: date | None = None
