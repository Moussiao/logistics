from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


class CustomerAddress(TimedMixin, models.Model):
    customer = models.ForeignKey(
        to="delivery.Customer",
        verbose_name=_("Заказчик"),
        on_delete=models.PROTECT,
        related_name="addresses",
    )

    postcode = models.CharField(_("почтовый индекс"), max_length=10, blank=True)
    country = models.ForeignKey(
        to="geo.Country",
        verbose_name=_("Страна"),
        on_delete=models.PROTECT,
        related_name="customer_addresses",
    )
    region = models.ForeignKey(
        to="geo.Region",
        verbose_name=_("Регион"),
        on_delete=models.PROTECT,
        related_name="customer_addresses",
    )
    city = models.ForeignKey(
        to="geo.City",
        verbose_name=_("Населенный пункт"),
        on_delete=models.PROTECT,
        related_name="customer_addresses",
    )
    street = models.CharField(_("Улица"), max_length=255)
    house_number = models.CharField(_("Номер дома"), max_length=50)
    flat_number = models.CharField(_("Номер квартиры"), max_length=10, blank=True)

    comment = models.CharField(_("Комментарий"), max_length=255, blank=True)

    class Meta(TypedModelMeta):
        verbose_name = _("Адрес заказчика")
        verbose_name_plural = _("Адреса заказчиков")

    def __str__(self) -> str:
        return f"{self.customer_id} -> {self.postcode}"
