# Generated by Django 5.1.3 on 2024-11-14 18:52

import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0007_remove_order_products_orderproduct"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalOrder",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "external_verbose",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Внешнее наименование"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("new", "Новый заказ"),
                            ("processing", "Обработка"),
                            ("delivery", "Доставка"),
                            ("paid", "Оплачен"),
                            ("canceled", "Отменен"),
                        ],
                        default="new",
                        max_length=16,
                        verbose_name="Состояние",
                    ),
                ),
                (
                    "state_changed_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Дата изменения состояния"
                    ),
                ),
                (
                    "delivery_date",
                    models.DateField(
                        blank=True, db_index=True, null=True, verbose_name="Дата доставки"
                    ),
                ),
                (
                    "expected_delivery_date",
                    models.DateField(db_index=True, verbose_name="Ожидаемая дата доставки"),
                ),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Стоимость"),
                ),
                (
                    "comment",
                    models.CharField(blank=True, max_length=255, verbose_name="Комментарий"),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Заказ",
                "verbose_name_plural": "historical Заказы",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
