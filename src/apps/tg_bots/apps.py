from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TgBotsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.tg_bots"
    verbose_name = _("Telegram")
