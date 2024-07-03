from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Customer(TimedMixin, models.Model):
    phone = models.CharField(
        _("Номер телефона"), max_length=16, unique=True, db_index=True
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Заказчик")
        verbose_name_plural = _("Заказчики")

    def __str__(self) -> str:
        return self.phone
