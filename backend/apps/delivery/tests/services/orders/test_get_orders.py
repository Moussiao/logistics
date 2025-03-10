from typing import TYPE_CHECKING

import pytest
from django.utils.timezone import localdate

from backend.apps.delivery.api.schemas import OrdersFilters
from backend.apps.delivery.models import Order, Partner
from backend.apps.delivery.services.orders.get_orders import GetOrders

if TYPE_CHECKING:
    from backend.apps.delivery.tests.fixtures import OrdersFactory, PartnerFactory
    from backend.apps.users.models import User

pytestmark = [pytest.mark.django_db]


def test_logistician_get_orders(logistician_user: "User", orders_factory: "OrdersFactory") -> None:
    orders_factory(GetOrders.PAGE_SIZE)

    result = GetOrders(logistician_user, OrdersFilters())()

    assert len(result.items) == GetOrders.PAGE_SIZE
    assert result.next_cursor is None
    assert result.previous_cursor is None


def test_partner_get_orders(
    partner_user: "User",
    orders_factory: "OrdersFactory",
    partner_factory: "PartnerFactory",
    another_partner: Partner,
) -> None:
    partner = partner_factory(user=partner_user)
    orders_factory(GetOrders.PAGE_SIZE, partner=partner)
    orders_factory(GetOrders.PAGE_SIZE, partner=another_partner)

    result = GetOrders(partner_user, OrdersFilters())()

    assert len(result.items) == GetOrders.PAGE_SIZE
    assert result.next_cursor is None
    assert result.previous_cursor is None


def test_unknown_user_get_orders(
    unknown_user: "User",
    orders_factory: "OrdersFactory",
    partner_factory: "PartnerFactory",
    another_partner: Partner,
) -> None:
    partner = partner_factory(user=unknown_user)
    orders_factory(GetOrders.PAGE_SIZE, partner=partner)
    orders_factory(GetOrders.PAGE_SIZE, partner=another_partner)

    result = GetOrders(unknown_user, OrdersFilters())()

    assert len(result.items) == 0
    assert result.next_cursor is None
    assert result.previous_cursor is None


def test_filters(
    logistician_user: "User", orders_factory: "OrdersFactory", partner: Partner
) -> None:
    orders_factory(GetOrders.PAGE_SIZE * 2)
    now_date = localdate()
    orders_to_filters = orders_factory(
        GetOrders.PAGE_SIZE,
        partner=partner,
        state=Order.State.NEW,
        delivery_date=now_date,
        expected_delivery_date=now_date,
    )
    filters = OrdersFilters(
        ids=",".join(str(x.pk) for x in orders_to_filters),
        partner_id=partner.pk,
        states=str(Order.State.NEW),
        delivery_date_start=now_date,
        delivery_date_end=now_date,
        expected_delivery_date_start=now_date,
        expected_delivery_date_end=now_date,
    )

    result = GetOrders(logistician_user, filters)()

    assert len(result.items) == GetOrders.PAGE_SIZE
    assert result.next_cursor is None
    assert result.previous_cursor is None
