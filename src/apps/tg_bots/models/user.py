from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class TgUser(TimedMixin, models.Model):
    is_bot = models.BooleanField(_("Бот"), help_text=_("Является ли ботом"))
    external_id = models.PositiveBigIntegerField(_("TG ID"), db_index=True, unique=True)
    username = models.CharField(_("Имя пользователя"), max_length=32, unique=True, blank=True)

    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150, blank=True)
    language_code = models.CharField(_("Язык"), max_length=16, blank=True)

    user = models.OneToOneField(
        to="users.User",
        verbose_name=_("Пользователь"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tg_user",
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self) -> str:
        return f"{self.external_id} - {self.first_name} {self.last_name}"
