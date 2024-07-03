from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Region(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=200)

    country = models.ForeignKey(
        to="geo.Country",
        verbose_name=_("Страна"),
        on_delete=models.PROTECT,
        related_name="regions",
    )
    time_zone = models.ForeignKey(
        to="geo.TimeZone",
        verbose_name=_("Часовой пояс"),
        null=True,
        on_delete=models.PROTECT,
        related_name="regions",
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")

    def __str__(self) -> str:
        return self.name
