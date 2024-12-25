from datetime import UTC, timedelta
from typing import TYPE_CHECKING

import pytest
from django.utils.timezone import localdate

from backend.apps.delivery.models import Order
from backend.apps.delivery.services.reports import (
    NotAvailableReportError,
    TodayNewOrders,
    TomorrowNewOrders,
)

if TYPE_CHECKING:
    from backend.apps.delivery.tests.fixtures import OrderFactory, PartnerFactory
    from backend.apps.geo.models import TimeZone


pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time("2022-07-01 13:00")
def test_today(
    utc_time_zone: "TimeZone", partner_factory: "PartnerFactory", order_factory: "OrderFactory"
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    yesterday_date = localdate(timezone=UTC) - timedelta(days=1)
    order_factory(partner=partner, state=Order.State.NEW, expected_delivery_date=yesterday_date)
    today_report = TodayNewOrders(partner=partner)

    report_text = today_report.get_text()

    assert report_text
    assert report_text != TodayNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 13:00")
def test_empty_today(utc_time_zone: "TimeZone", partner_factory: "PartnerFactory") -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    today_report = TodayNewOrders(partner=partner)

    report_text = today_report.get_text()

    assert report_text == TodayNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_error_today(utc_time_zone: "TimeZone", partner_factory: "PartnerFactory") -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    today_report = TodayNewOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        today_report.get_text()


@pytest.mark.freeze_time("2022-07-01 22:00")
def test_tomorrow(
    utc_time_zone: "TimeZone", partner_factory: "PartnerFactory", order_factory: "OrderFactory"
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    tomorrow_date = localdate(timezone=UTC) + timedelta(days=1)
    order_factory(partner=partner, state=Order.State.NEW, expected_delivery_date=tomorrow_date)
    tomorrow_report = TomorrowNewOrders(partner=partner)

    report_text = tomorrow_report.get_text()

    assert report_text
    assert report_text != TomorrowNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 22:00")
def test_empty_tomorrow(utc_time_zone: "TimeZone", partner_factory: "PartnerFactory") -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    tomorrow_report = TomorrowNewOrders(partner=partner)

    report_text = tomorrow_report.get_text()

    assert report_text == TomorrowNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 23:00")
def test_error_tomorrow(utc_time_zone: "TimeZone", partner_factory: "PartnerFactory") -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    tomorrow_report = TomorrowNewOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        tomorrow_report.get_text()
