from typing import TYPE_CHECKING

import pytest
from asgiref.sync import sync_to_async
from django.db.models import aprefetch_related_objects

from backend.apps.delivery.services.reports.senders import PartnerWithoutTgChatError, TelegramSender

if TYPE_CHECKING:
    from pytest_mock import MockerFixture, MockType

    from backend.apps.delivery.tests.fixtures import PartnerFactory
    from backend.apps.tg_bots.models import TgChat

# transaction=True для верной работы sync_to_async.
# Без него тест падает по таймауту, а также изменения в базе не откатываются.
pytestmark = [pytest.mark.django_db(transaction=True)]


@pytest.fixture
def mock_tg_send_message(mocker: "MockerFixture") -> "MockType":
    return mocker.patch("telegram.ext.ExtBot.send_message")


@pytest.mark.asyncio
async def test_telegram_sender(
    tg_chat: "TgChat", partner_factory: "PartnerFactory", mock_tg_send_message: "MockType"
) -> None:
    partner = await sync_to_async(partner_factory)(tg_chat=tg_chat)
    # Необходимо, так как в TelegramSender идет обращение к данному полю.
    # А если поле не подгружено, то в асинхронной функции будет поднята ошибка.
    await aprefetch_related_objects([partner], "tg_chat")

    telegram_sender = TelegramSender()

    await telegram_sender.send(text="text", partner=partner)

    mock_tg_send_message.assert_called_once_with(chat_id=tg_chat.external_id * -1, text="text")


@pytest.mark.asyncio
async def test_error_telegram_sender(
    partner_factory: "PartnerFactory", mock_tg_send_message: "MockType"
) -> None:
    partner = await sync_to_async(partner_factory)(tg_chat=None)
    telegram_sender = TelegramSender()

    with pytest.raises(PartnerWithoutTgChatError):
        await telegram_sender.send(text="text", partner=partner)

    mock_tg_send_message.assert_not_called()
