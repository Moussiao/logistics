# Generated by Django 5.1.1 on 2024-09-17 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0004_remove_order_status_order_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="state",
            field=models.CharField(
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
    ]
