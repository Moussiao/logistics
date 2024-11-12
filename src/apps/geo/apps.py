from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "src.apps.geo"
    verbose_name = _("География")
