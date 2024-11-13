from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.management import BaseCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes


class Command(BaseCommand):
    """Команда запускает telegram чат бота."""

    help = __doc__

    def handle(self, **options: Any) -> None:
        application = ApplicationBuilder().token(settings.BOT_TOKEN).build()  # type: ignore[misc]

        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        application.run_polling()

    @staticmethod
    async def start_command(
        update: "Update",
        context: "ContextTypes.DEFAULT_TYPE",
    ) -> None:
        if update.effective_chat is None:
            return

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello world {update.effective_chat.id}",
        )

    @staticmethod
    async def help_command(
        update: "Update",
        context: "ContextTypes.DEFAULT_TYPE",
    ) -> None:
        if update.message is None:
            return

        await update.message.reply_text("Help me")

    @staticmethod
    async def echo(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
        if update.message is None:
            return

        await update.message.reply_text(update.message.text or "")
