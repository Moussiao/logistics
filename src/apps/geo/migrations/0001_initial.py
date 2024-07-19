# Generated by Django 5.0.7 on 2024-07-18 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        help_text="alpha_2",
                        max_length=4,
                        unique=True,
                        verbose_name="Код",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
            },
        ),
        migrations.CreateModel(
            name="TimeZone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Наименование"
                    ),
                ),
                (
                    "minutes_offset_from_utc",
                    models.SmallIntegerField(verbose_name="Смещение от UTC в минутах"),
                ),
                (
                    "is_canonical",
                    models.BooleanField(
                        help_text="Является ли основным, предпочительным наименованием часовой зоны. Именно каноничные будут использоваться в системе, а другие скрыты.",
                        verbose_name="Каноничный",
                    ),
                ),
            ],
            options={
                "verbose_name": "Часовой пояс",
                "verbose_name_plural": "Часовые пояса",
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="regions",
                        to="geo.country",
                        verbose_name="Страна",
                    ),
                ),
                (
                    "time_zone",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="regions",
                        to="geo.timezone",
                        verbose_name="Часовой пояс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Регион",
                "verbose_name_plural": "Регионы",
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Наименование")),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cities",
                        to="geo.region",
                        verbose_name="Регион",
                    ),
                ),
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
            },
        ),
    ]
