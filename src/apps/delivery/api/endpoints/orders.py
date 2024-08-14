from http import HTTPStatus
from typing import TYPE_CHECKING

from django.http import HttpRequest
from ninja import Query, Router, Schema
from ninja.errors import HttpError

from apps.delivery.api.schemas import (
    CreateOrderResponse,
    DetailOrderResponse,
    OrderRequest,
    OrdersFilters,
    OrdersResponse,
)
from apps.delivery.services.orders.create_order import CreateOrder
from apps.delivery.services.orders.exceptions import CreateOrderError, OrderNotFoundError
from apps.delivery.services.orders.get_order import GetOrder
from apps.delivery.services.orders.get_orders import GetOrders
from core.schemas import ErrorEntity, ErrorResponse

if TYPE_CHECKING:
    from apps.delivery.models import Order

router = Router()


@router.post(
    "",
    response={
        HTTPStatus.CREATED: CreateOrderResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
def create_order(request: HttpRequest, data: OrderRequest) -> tuple[HTTPStatus, Schema]:
    try:
        order = CreateOrder(data)()
    except CreateOrderError as exc:
        order_error = ErrorEntity(msg=exc.msg, type=exc.error_type.value, field=exc.field)
        return HTTPStatus.UNPROCESSABLE_ENTITY, ErrorResponse(detail=[order_error])

    return HTTPStatus.CREATED, CreateOrderResponse(id=order.pk)


@router.get("", response=OrdersResponse)
def get_orders(request: HttpRequest, filters: Query[OrdersFilters]) -> OrdersResponse:
    return GetOrders(user=request.user, filters=filters)()


@router.get("/{order_id}", response=DetailOrderResponse)
def get_order(request: HttpRequest, order_id: int) -> "Order":
    try:
        order = GetOrder(order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc

    return order
