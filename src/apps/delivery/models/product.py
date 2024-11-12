from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from src.core.models import TimedMixin


@final
class Product(TimedMixin, models.Model):
    name = models.CharField(_("Наименование"), max_length=150, unique=True)
    price = models.DecimalField(_("Стоимость"), max_digits=10, decimal_places=2)

    class Meta(TypedModelMeta):
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return self.name


@final
class OrderProduct(TimedMixin, models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name=_("Товар"),
        related_name="orders",
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        to="delivery.Order",
        verbose_name=_("Заказ"),
        on_delete=models.CASCADE,
        related_name="products",
    )

    quantity = models.PositiveSmallIntegerField(_("Количество"))
    total_price = models.DecimalField(_("Общая стоимость"), max_digits=10, decimal_places=2)

    class Meta(TypedModelMeta):
        verbose_name = _("Товар заказа")
        verbose_name_plural = _("Товары заказов")

    def __str__(self) -> str:
        return f"{self.quantity} ({self.total_price})"
