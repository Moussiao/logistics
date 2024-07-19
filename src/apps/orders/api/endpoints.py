from http import HTTPStatus
from typing import TYPE_CHECKING

from django.http import HttpRequest
from ninja import Query, Router, Schema
from ninja.errors import HttpError

from apps.orders.api.schemas import (
    CreateOrderOutput,
    DetailOrderOutput,
    OrderInput,
    OrdersFilters,
    OrdersOutput,
    PartnersFilters,
    PartnersOutput,
)
from apps.orders.services.create_order import CreateOrder
from apps.orders.services.exceptions import CreateOrderError, OrderNotFoundError
from apps.orders.services.list_orders import ListOrders
from apps.orders.services.list_partners import ListPartners
from apps.orders.services.retrieve_order import RetrieveOrder
from core.schemas import ErrorEntity, ErrorOutput

if TYPE_CHECKING:
    from apps.orders.models import Order

router = Router()


@router.post(
    "/orders",
    response={
        HTTPStatus.CREATED: CreateOrderOutput,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorOutput,
    },
)
def create_order(request: HttpRequest, data: OrderInput) -> tuple[HTTPStatus, Schema]:
    try:
        order = CreateOrder(data)()
    except CreateOrderError as exc:
        order_error = ErrorEntity(
            msg=exc.msg, type=exc.error_type.value, field=exc.field
        )
        return HTTPStatus.UNPROCESSABLE_ENTITY, ErrorOutput(detail=[order_error])

    return HTTPStatus.CREATED, CreateOrderOutput(id=order.pk)


@router.get("/orders", response=OrdersOutput)
def list_orders(request: HttpRequest, filters: Query[OrdersFilters]) -> OrdersOutput:
    return ListOrders(user=request.user, filters=filters)()


@router.get("/orders/{order_id}", response=DetailOrderOutput)
def retrieve_order(request: HttpRequest, order_id: int) -> "Order":
    try:
        order = RetrieveOrder(order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc

    return order


@router.get("/partners", response=PartnersOutput)
def list_partners(
    request: HttpRequest,
    filters: Query[PartnersFilters],
) -> PartnersOutput:
    return ListPartners(filters)()
