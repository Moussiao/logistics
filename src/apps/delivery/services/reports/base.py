from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.utils.timezone import is_naive, localtime, make_aware, now

from apps.delivery.services.reports.exceptions import NotAvailableReportError, SenderError

if TYPE_CHECKING:
    from apps.delivery.models import Order, Partner
    from apps.delivery.services.reports.types import ReportType


class OrdersReport(ABC):
    report_type: Optional["ReportType"] = None

    # Поля экземпляра
    _partner: "Partner"
    _partner_current_time: datetime
    _partner_current_date: date

    def __init__(
        self,
        partner: "Partner",
        current_time: datetime | None = None,
    ) -> None:
        self._partner = partner

        if current_time is None:
            current_time = now()
        elif is_naive(current_time):
            current_time = make_aware(current_time)
        partner_timezone = partner.working_time_zone.get_zone_info()
        self._partner_current_time = localtime(current_time, timezone=partner_timezone)
        self._partner_current_date = self._partner_current_time.date()

    def get_text(self) -> str:
        if not self._is_report_allowed():
            raise NotAvailableReportError(
                f"Отчет не доступен для {self._partner} в {self._partner_current_time}"
            )

        orders = self._get_orders_to_report()
        return self._prepare_orders_report(orders)

    async def aget_text(self) -> str:
        return await sync_to_async(self.get_text)()

    def _is_report_allowed(self) -> bool:
        return True

    @abstractmethod
    def _get_orders_to_report(self) -> Sequence["Order"]:
        pass

    @abstractmethod
    def _prepare_orders_report(self, orders: Sequence["Order"]) -> str:
        pass


class OrdersReportSender(ABC):
    async def send(self, text: str, partner: "Partner") -> None:
        try:
            await self._send(text=text, partner=partner)
        except SenderError:
            raise
        except Exception as exc:
            raise SenderError(str(exc)) from exc

    @classmethod
    @abstractmethod
    def get_valid_partners_qs(cls) -> QuerySet["Partner"]:
        pass

    @abstractmethod
    async def _send(self, text: str, partner: "Partner") -> None:
        pass
