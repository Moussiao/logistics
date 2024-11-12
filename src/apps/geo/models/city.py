from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.core.models import TimedMixin


@final
class City(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=200)
    region = models.ForeignKey(
        to="geo.Region",
        verbose_name=_("Регион"),
        on_delete=models.PROTECT,
        related_name="cities",
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Город")
        verbose_name_plural = _("Города")

    def __str__(self) -> str:
        return self.name
