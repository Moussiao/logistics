from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from backend.core.models import TimedMixin


@final
class TgChat(TimedMixin, models.Model):
    class Type(models.TextChoices):
        CHANNEL = "channel", _("Канал")
        PRIVATE = "private", _("Приватный")
        GROUP = "group", _("Группа")
        SUPERGROUP = "supergroup", _("Супер-группа")

    type = models.CharField(_("Тип"), max_length=16, choices=Type.choices)
    external_id = models.PositiveBigIntegerField(_("TG ID"), db_index=True, unique=True)

    title = models.CharField(_("Название"), max_length=128, db_index=True, blank=True)
    description = models.CharField(_("Описание"), max_length=255, blank=True)
    username = models.CharField(_("Текстовый идентификатор"), max_length=32, blank=True)
    invite_link = models.CharField(_("Ссылка - приглашение"), max_length=64, blank=True)

    class Meta(TypedModelMeta):
        verbose_name = _("Чат")
        verbose_name_plural = _("Чаты")

    def __str__(self) -> str:
        return f"{self.external_id} - {self.title} ({self.type})"
