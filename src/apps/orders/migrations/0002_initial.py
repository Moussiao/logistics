# Generated by Django 5.0.6 on 2024-07-12 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("geo", "0001_initial"),
        ("orders", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="partner",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="partner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="partner",
            name="working_time_zone",
            field=models.ForeignKey(
                help_text="Часовой пояс на который будет завязана логика работы с партнером",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="geo.timezone",
                verbose_name="Рабочий часовой пояс",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="partner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="orders.partner",
                verbose_name="Партнер",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                related_name="orders", to="orders.product", verbose_name="Продукты"
            ),
        ),
    ]
