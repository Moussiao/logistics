from ninja import Field, ModelSchema, Schema
from pydantic import constr

from apps.orders.api.schemas.customer import CustomerInput
from apps.orders.api.schemas.customer_address import CustomerAddressInput
from apps.orders.api.schemas.product import ProductInput
from apps.orders.models import Order


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
        fields = (
            "external_verbose",
            "expected_delivery_date",
            "comment",
        )


class OrderOutput(Schema):
    id: int


class OrderErrorEntity(Schema):
    msg: str
    type: str
    field: str | None = None
    loc: list[str] | None = None
    ctx: dict[str, str] | None = None


class OrderErrorOutput(Schema):
    detail: list[OrderErrorEntity]
