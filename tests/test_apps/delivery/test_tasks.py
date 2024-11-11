import pytest
from pytest_mock import MockerFixture, MockType

from apps.delivery.tasks import notify_of_buyout_orders, notify_of_new_orders

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def mock_try_send_reports(mocker: MockerFixture) -> MockType:
    return mocker.patch("apps.delivery.services.reports.TrySendReports.send_to_active_partners")


def test_notify_of_buyout_orders(mock_try_send_reports: "MockType") -> None:
    notify_of_buyout_orders()
    mock_try_send_reports.assert_called_once()


def test_notify_of_new_orders(mock_try_send_reports: "MockType") -> None:
    notify_of_new_orders()
    mock_try_send_reports.assert_called_once()
