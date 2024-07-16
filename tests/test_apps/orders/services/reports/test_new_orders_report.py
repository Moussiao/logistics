from typing import TYPE_CHECKING

import pytest

from apps.orders.services.reports import (
    NotAvailableReportError,
    TodayNewOrders,
    TomorrowNewOrders,
)

if TYPE_CHECKING:
    from apps.geo.models import TimeZone
    from tests.plugins.apps.orders import PartnerFactory


pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time("2022-07-01 13:00")
def test_empty_today_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    today_report = TodayNewOrders(partner=partner)

    report_text = today_report.get_text()

    assert report_text == TodayNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 14:00")
def test_error_today_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    today_report = TodayNewOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        today_report.get_text()


@pytest.mark.freeze_time("2022-07-01 22:00")
def test_empty_tomorrow_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    tomorrow_report = TomorrowNewOrders(partner=partner)

    report_text = tomorrow_report.get_text()

    assert report_text == TomorrowNewOrders.EMPTY_ORDERS_TEXT


@pytest.mark.freeze_time("2022-07-01 23:00")
def test_error_tomorrow_report(
    utc_time_zone: "TimeZone",
    partner_factory: "PartnerFactory",
) -> None:
    partner = partner_factory(working_time_zone=utc_time_zone)
    tomorrow_report = TomorrowNewOrders(partner=partner)

    with pytest.raises(NotAvailableReportError):
        tomorrow_report.get_text()
