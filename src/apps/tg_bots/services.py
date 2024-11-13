from typing import TYPE_CHECKING, final

import attr
from django.conf import settings
from telegram.ext import ExtBot as TelegramBot

if TYPE_CHECKING:
    from src.apps.tg_bots.models import TgChat


@final
@attr.dataclass(slots=True, frozen=True)
class TgSendMessage:
    _text: str
    _chat: "TgChat"

    async def __call__(self) -> None:
        bot = TelegramBot(token=settings.BOT_TOKEN)  # type: ignore[misc]
        await bot.send_message(chat_id=self._chat.external_id * -1, text=self._text)
