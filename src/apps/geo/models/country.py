from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Country(TimedMixin, models.Model):
    code = models.CharField(_("Код"), max_length=4, unique=True)
    name = models.CharField(_("Наименование"), max_length=200)

    class Meta(TypedModelMeta):
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")

    def __str__(self) -> str:
        return self.name
