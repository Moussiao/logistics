from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from core.models import TimedMixin


@final
class Order(TimedMixin, models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("Новый заказ")
        DELIVERY = "delivery", _("Доставка")
        PAID = "paid", _("Оплачен")
        RETURN = "return", _("Возврат")

    external_id = models.PositiveIntegerField(_("Внешний ID"), db_index=True)
    external_verbose = models.CharField(_("Внешнее наименование"), max_length=150, blank=True)
    status = models.CharField(
        _("Статус"), max_length=16, default=Status.NEW, choices=Status.choices
    )
    delivery_date = models.DateField(_("Дата доставки"), db_index=True, null=True, blank=True)
    expected_delivery_date = models.DateField(_("Ожидаемая дата доставки"), db_index=True)
    total_price = models.DecimalField(_("Стоимость"), max_digits=10, decimal_places=2)
    comment = models.CharField(_("Комментарий"), max_length=255, blank=True)

    partner = models.ForeignKey(
        to="delivery.Partner",
        verbose_name=_("Партнер"),
        on_delete=models.PROTECT,
        related_name="orders",
    )
    customer = models.ForeignKey(
        to="delivery.Customer",
        verbose_name=_("Заказчик"),
        on_delete=models.PROTECT,
        related_name="orders",
    )
    customer_address = models.ForeignKey(
        to="delivery.CustomerAddress",
        verbose_name=_("Адрес заказчика"),
        on_delete=models.PROTECT,
        related_name="orders",
    )
    products = models.ManyToManyField(
        to="delivery.Product", verbose_name=_("Продукты"), related_name="orders"
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self) -> str:
        return f"{self.external_id} - {self.status}"
