from typing import TYPE_CHECKING

import pytest

from apps.delivery.services.reports import (
    NotAvailableReportError,
    PreviousDayBuyoutedOrders,
    PreviousMonthBuyoutedOrders,
)

if TYPE_CHECKING:
    from apps.delivery.models import Partner
    from apps.geo.models import TimeZone
    from tests.plugins.apps.delivery import PartnerFactory


pytestmark = [pytest.mark.django_db]


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
