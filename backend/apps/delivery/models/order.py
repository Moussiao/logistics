from typing import final

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta
from simple_history.models import HistoricalRecords  # type: ignore[import-untyped]

from backend.core.models import TimedMixin


@final
class Order(TimedMixin, models.Model):
    class State(models.TextChoices):
        NEW = "new", _("Новый заказ")
        PROCESSING = "processing", _("Обработка")
        DELIVERY = "delivery", _("Доставка")
        PAID = "paid", _("Оплачен")
        CANCELED = "canceled", _("Отменен")

    external_id = models.PositiveIntegerField(_("Внешний ID"), db_index=True)
    external_verbose = models.CharField(_("Внешнее наименование"), max_length=150, blank=True)
    state = models.CharField(
        _("Состояние"), max_length=16, default=State.NEW, choices=State.choices
    )
    state_changed_at = models.DateTimeField(_("Дата изменения состояния"), default=now)
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

    history = HistoricalRecords(
        excluded_fields=[
            "external_id",
            "partner",
            "customer",
            "customer_address",
            "created_at",
            "updated_at",
        ],
        cascade_delete_history=True,
    )

    class Meta(TypedModelMeta):
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self) -> str:
        return f"{self.external_id} - {self.state}"
