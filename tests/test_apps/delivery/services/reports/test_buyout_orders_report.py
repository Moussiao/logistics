from datetime import UTC, timedelta
from typing import TYPE_CHECKING

import pytest
from dateutil.relativedelta import relativedelta
from django.utils.timezone import localdate

from apps.delivery.models import Order, Partner
from apps.delivery.services.reports import (
    NotAvailableReportError,
    PreviousDayBuyoutedOrders,
    PreviousMonthBuyoutedOrders,
)

if TYPE_CHECKING:
    from apps.geo.models import TimeZone
    from tests.plugins.apps.delivery import OrderFactory, PartnerFactory


pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_previous_day_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
    order_factory: "OrderFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    previous_date = localdate(timezone=UTC) - timedelta(days=1)
    previous_day_report = PreviousDayBuyoutedOrders(partner=partner)
    order_factory(partner=partner, status=Order.Status.PAID, delivery_date=previous_date)

    report_text = previous_day_report.get_text()

    assert report_text
    assert report_text != PreviousDayBuyoutedOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_empty_previous_day_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    previous_day_report = PreviousDayBuyoutedOrders(partner=partner)

    report_text = previous_day_report.get_text()

    assert report_text == PreviousDayBuyoutedOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 13:00")
def test_error_previous_day_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    previous_day_report = PreviousDayBuyoutedOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        previous_day_report.get_text()


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_previous_month_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
    order_factory: "OrderFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    previous_month_first_date = localdate(timezone=UTC) - relativedelta(months=1)
    previous_day_report = PreviousMonthBuyoutedOrders(partner=partner)
    order_factory(
        partner=partner,
        status=Order.Status.PAID,
        delivery_date=previous_month_first_date,
    )

    report_text = previous_day_report.get_text()

    assert report_text
    assert report_text != PreviousDayBuyoutedOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_empty_previous_month_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    previous_month_report = PreviousMonthBuyoutedOrders(partner=partner)

    report_text = previous_month_report.get_text()

    assert report_text == PreviousMonthBuyoutedOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-15 13:00")
def test_error_previous_month_report(partner: "Partner") -> None:
    previous_month_report = PreviousMonthBuyoutedOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        previous_month_report.get_text()
