from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Product(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=150, unique=True)
    price = models.DecimalField(_("Стоимость"), max_digits=10, decimal_places=2)

    class Meta(TypedModelMeta):
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return self.name
