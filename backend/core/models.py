from django.db import models
from django.utils.translation import gettext_lazy as _


class TimedMixin(models.Model):
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата последнего изменения"), auto_now=True)

    class Meta:
        abstract = True
