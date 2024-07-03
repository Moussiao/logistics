from typing import TYPE_CHECKING, final

import attr
from telegram.ext import ExtBot as TelegramBot

from core.settings.environ import env

if TYPE_CHECKING:
    from apps.tg_bots.models import TgChat


@final
@attr.dataclass(slots=True, frozen=True)
class TgSendMessage:
    BOT_TOKEN = env("BOT_TOKEN", cast=str)

    _text: str
    _chat: "TgChat"

    async def __call__(self) -> None:
        bot = TelegramBot(token=self.BOT_TOKEN)
        await bot.send_message(chat_id=self._chat.external_id * -1, text=self._text)
