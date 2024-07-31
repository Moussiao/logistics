from decimal import Decimal

from ninja import Field, ModelSchema

from apps.delivery.models import Product

MIN_PRICE = 0
MAX_PRICE = 150000


class ProductRequest(ModelSchema):
    # Используем ограничения дабы максимальная сумма,
    # по всем заказам, не могла привысить валидное значение для Order.total_price
    amount: int = Field(gt=0, le=25)
    price: Decimal = Field(max_digits=8, decimal_places=2, ge=MIN_PRICE, le=MAX_PRICE)

    class Meta:
        model = Product
        fields = ("name",)


class ProductResponse(ModelSchema):
    class Meta:
        model = Product
        fields = ("id", "name", "price")
