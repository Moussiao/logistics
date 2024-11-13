from decimal import Decimal

from ninja import Field, Schema


class ProductRequest(Schema):
    name: str = Field(max_length=150)
    # Используем ограничения дабы максимальная сумма,
    # по всем заказам, не могла привысить валидное значение для Order.total_price
    quantity: int = Field(gt=0, le=25)
    price: Decimal = Field(max_digits=8, decimal_places=2, ge=0, le=150_000)


class OrderProductResponse(Schema):
    product_id: int = Field(alias="product.id")
    product_name: str = Field(alias="product.name")
    quantity: int = Field(ge=0)
    total_price: Decimal
