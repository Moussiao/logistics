from typing import final

from django.db.models import QuerySet

from backend.apps.delivery.models import Partner
from backend.apps.delivery.services.reports.base import OrdersReportSender
from backend.apps.delivery.services.reports.exceptions import SenderError
from backend.apps.tg_bots.services import TgSendMessage


class PartnerWithoutTgChatError(SenderError):
    pass


@final
class TelegramSender(OrdersReportSender):
    @classmethod
    def get_valid_partners_qs(cls) -> QuerySet[Partner]:
        return Partner.objects.filter(tg_chat__isnull=False).select_related("tg_chat")

    async def _send(self, text: str, partner: "Partner") -> None:
        if partner.tg_chat is None:
            raise PartnerWithoutTgChatError(f"{partner} is unrelated to tg_chat")

        tg_message_sender = TgSendMessage(text=text, chat=partner.tg_chat)
        await tg_message_sender()
