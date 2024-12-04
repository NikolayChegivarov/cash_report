# Generated by Django 5.0.7 on 2024-12-03 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashbox_app", "0010_alter_address_options_remove_address_schedules_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoldStandard",
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
                    "shift_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата смены"),
                ),
                (
                    "gold_standard",
                    models.CharField(
                        choices=[
                            ("750gold", "750gold"),
                            ("585goldN", "Не стандарт"),
                            ("585gold", "585gold"),
                            ("500gold", "500gold"),
                            ("375gold", "375gold"),
                            ("925silvers", "925silvers"),
                            ("875silvers", "875silvers"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "price_rubles",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена в рублях"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SecretRoom",
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
                    "shift_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата смены"),
                ),
                ("fio", models.CharField(max_length=50, verbose_name="ФИО")),
                ("nomenclature", models.CharField(max_length=50, verbose_name="ФИО")),
                (
                    "GoldStandard",
                    models.CharField(
                        choices=[
                            ("750gold", "750gold"),
                            ("585goldN", "Не стандарт"),
                            ("585gold", "585gold"),
                            ("500gold", "500gold"),
                            ("375gold", "375gold"),
                            ("925silvers", "925silvers"),
                            ("875silvers", "875silvers"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена за грамм."
                    ),
                ),
                (
                    "weight_clean",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Чистый вес"
                    ),
                ),
                (
                    "weight_fact",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Фактический вес"
                    ),
                ),
                (
                    "sum",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Выдано денег"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("LOCAL", "В ФИЛИАЛЕ"),
                            ("GATHER", "СОБРАНО"),
                            ("ISSUED", "ВЫДАНО"),
                        ],
                        default="LOCAL",
                        max_length=15,
                    ),
                ),
            ],
        ),
    ]