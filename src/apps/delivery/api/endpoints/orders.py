from http import HTTPStatus
from typing import TYPE_CHECKING

from django.http import HttpRequest
from ninja import Query, Router, Schema
from ninja.errors import HttpError

from apps.delivery.api.schemas import (
    CreateOrderResponse,
    DetailOrderResponse,
    EditOrderRequest,
    OrderRequest,
    OrdersFilters,
    OrdersResponse,
)
from apps.delivery.services.orders.create_order import CreateOrder
from apps.delivery.services.orders.exceptions import CreateOrderError, OrderNotFoundError
from apps.delivery.services.orders.get_order import GetOrder
from apps.delivery.services.orders.get_orders import GetOrders
from apps.delivery.services.orders.state_machine_actions import (
    CancelOrder,
    CustomerPaid,
    DriveToCustomer,
    TakeOrderToJob,
)
from apps.delivery.services.orders.update_order import UpdateOrder
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
        order = GetOrder(user=request.user, order_id=order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc

    return order


@router.patch("/{order_id}")
def update_order(request: HttpRequest, order_id: int, payload: EditOrderRequest) -> None:
    try:
        UpdateOrder(user=request.user, order_id=order_id, payload=payload)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc


@router.post("/{order_id}/take-the-job")
def drive_to_customer(request: HttpRequest, order_id: int) -> None:
    try:
        TakeOrderToJob(user=request.user, order_id=order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc


@router.post("/{order_id}/drive-to-customer")
def go_to_the_customer(request: HttpRequest, order_id: int) -> None:
    try:
        DriveToCustomer(user=request.user, order_id=order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc


@router.post("/{order_id}/customer-paid")
def customer_paid(request: HttpRequest, order_id: int) -> None:
    try:
        CustomerPaid(user=request.user, order_id=order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc


@router.post("/{order_id}/cancel")
def cancel_order(request: HttpRequest, order_id: int) -> None:
    try:
        CancelOrder(user=request.user, order_id=order_id)()
    except OrderNotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, message="Order not exists") from exc
