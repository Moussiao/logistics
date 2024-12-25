from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from backend.core.models import TimedMixin


@final
class Country(TimedMixin, models.Model):
    # max_length=16 для ситуации при генирации рандомных стран, дабы уменьшить шанс коллизий.
    # Для нынешних СУБД, разницы особо нет, ограничиваемым ли мы длину для CharField или нет.
    code = models.CharField(_("Код"), help_text="alpha_2", max_length=16, unique=True)
    name = models.CharField(_("Наименование"), max_length=200)

    class Meta(TypedModelMeta):
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")

    def __str__(self) -> str:
        return self.name
