from typing import final

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


@final
class User(AbstractUser):
    class Role(models.TextChoices):
        LOGISTICIAN = "logistician", _("Логист")
        DELIVERY_PARTNER = "partner", _("Партнер")
        UNKNOWN = "", _("Не указана")

    role = models.CharField(_("Роль"), max_length=16, choices=Role.choices, blank=True)

    updated_at = models.DateTimeField(_("Дата последнего изменения"), auto_now=True)

    class Meta(AbstractUser.Meta):
        abstract = False
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
