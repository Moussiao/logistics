from typing import TYPE_CHECKING

import pytest
from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from pytest_mock import MockerFixture, MockType

from backend.apps.delivery.models import Partner
from backend.apps.delivery.services.reports import (
    NotAvailableReportError,
    ReportType,
    TrySendReports,
)
from backend.apps.delivery.services.reports.base import OrdersReportSender

if TYPE_CHECKING:
    from backend.apps.delivery.tests.fixtures import PartnersFactory

# transaction=True для верной работы sync_to_async.
# Без него тест падает по таймауту, а также изменения в базе не откатываются.
pytestmark = [pytest.mark.django_db(transaction=True)]


class TestSender(OrdersReportSender):
    @classmethod
    def get_valid_partners_qs(cls) -> QuerySet[Partner]:
        return Partner.objects.all()

    async def _send(self, text: str, partner: Partner) -> None:
        assert isinstance(text, str)
        assert isinstance(partner, Partner)


@pytest.fixture
def mock_send_report(mocker: MockerFixture) -> MockType:
    return mocker.patch.object(
        target=TrySendReports,
        attribute="_send_report",
        side_effect=NotAvailableReportError(),
    )


@pytest.fixture
def mock_send_to_partner(mocker: MockerFixture) -> MockType:
    return mocker.patch.object(
        target=TrySendReports,
        attribute="send_to_partner",
        return_value=None,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("report_type", [ReportType.NEW_ORDERS, ReportType.BYUYOUT_ORDERS])
async def test_send_to_active_partners(
    report_type: ReportType, mock_send_report: MockType, partners_factory: "PartnersFactory"
) -> None:
    partners_count = 10
    await sync_to_async(partners_factory)(partners_count, active=True)
    sender = TrySendReports(report_type=report_type, sender=TestSender())

    await sender.send_to_active_partners()

    assert mock_send_report.call_count == partners_count * sender.get_reports_count()


@pytest.mark.asyncio
@pytest.mark.parametrize("report_type", [ReportType.NEW_ORDERS, ReportType.BYUYOUT_ORDERS])
async def test_empty_send_to_active_partners(
    report_type: ReportType, mock_send_to_partner: MockType
) -> None:
    sender = TrySendReports(report_type=report_type, sender=TestSender())

    await sender.send_to_active_partners()

    mock_send_to_partner.assert_not_called()
