from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router, Schema

from apps.orders.api.schemas import (
    OrderErrorEntity,
    OrderErrorOutput,
    OrderInput,
    OrderOutput,
)
from apps.orders.services.create_order import CreateOrder
from apps.orders.services.exceptions import CreateOrderError

router = Router()


type ApiResponse = tuple[HTTPStatus, Schema]


@router.post(
    "/orders",
    response={
        HTTPStatus.CREATED: OrderOutput,
        HTTPStatus.UNPROCESSABLE_ENTITY: OrderErrorOutput,
    },
)
def create_order(request: HttpRequest, data: OrderInput) -> ApiResponse:
    try:
        order = CreateOrder(data)()
    except CreateOrderError as exc:
        order_error = OrderErrorEntity(
            msg=exc.msg, type=exc.error_type.value, field=exc.field
        )
        return HTTPStatus.UNPROCESSABLE_ENTITY, OrderErrorOutput(detail=[order_error])

    return HTTPStatus.CREATED, OrderOutput(id=order.pk)
