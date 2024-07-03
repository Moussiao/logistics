from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Partner(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=150)
    is_active = models.BooleanField(
        _("Активен"), help_text=_("Является ли активным партнером"), default=True
    )

    user = models.OneToOneField(
        to="users.User",
        verbose_name=_("Пользователь"),
        on_delete=models.PROTECT,
        related_name="partner",
    )
    tg_chat = models.OneToOneField(
        to="tg_bots.TgChat",
        verbose_name=_("Чат в Telegram"),
        on_delete=models.PROTECT,
        related_name="partner",
        null=True,
    )
    working_time_zone = models.ForeignKey(
        to="geo.TimeZone",
        verbose_name=_("Рабочий часовой пояс"),
        help_text=_("Часовой пояс на который будет завязана логика работы с партнером"),
        on_delete=models.PROTECT,
        related_name="+",
    )
    regions = models.ManyToManyField(to="geo.Region", related_name="+")

    class Meta(TypedModelMeta):
        verbose_name = _("Партнер")
        verbose_name_plural = _("Партнеры")

    def __str__(self) -> str:
        return self.name
