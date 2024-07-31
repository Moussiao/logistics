from typing import Any, final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Customer(TimedMixin, models.Model):
    class Gender(models.TextChoices):
        MALE = "male", _("Мужчина")
        FEMALE = "female", _("Женшина")
        UNKNOWN = "unknown", _("Неизветсно")

    name = models.CharField(_("ФИО"), max_length=200)
    email = models.EmailField(_("Email"), blank=True)

    phone = models.CharField(_("Номер телефона"), max_length=32, unique=True, db_index=True)
    gender = models.CharField(
        _("Пол"), max_length=8, default=Gender.UNKNOWN, choices=Gender.choices
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Заказчик")
        verbose_name_plural = _("Заказчики")

    def __str__(self) -> str:
        return self.phone

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.email = self.email.lower()
        super().save(*args, **kwargs)
