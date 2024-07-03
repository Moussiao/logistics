from typing import final
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class TimeZone(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=100, unique=True)
    minutes_offset_from_utc = models.SmallIntegerField(_("Смещение от UTC в минутах"))

    is_canonical = models.BooleanField(
        _("Каноничный"),
        help_text=_(
            "Является ли основным, предпочительным наименованием часовой зоны. "
            "Именно каноничные будут использоваться в системе, а другие скрыты."
        ),
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Часовой пояс")
        verbose_name_plural = _("Часовые пояса")

    def __str__(self) -> str:
        return self.name

    def get_zone_info(self) -> ZoneInfo | None:
        try:
            zone_info = ZoneInfo(self.name)
        except ZoneInfoNotFoundError:
            zone_info = None

        return zone_info
