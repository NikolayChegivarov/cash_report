# Generated by Django 5.0.7 on 2024-11-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashbox_app", "0008_alter_cashreport_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
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
                    "day_of_week",
                    models.CharField(
                        choices=[
                            ("monday", "Понедельник"),
                            ("tuesday", "Вторник"),
                            ("wednesday", "Среда"),
                            ("thursday", "Четверг"),
                            ("friday", "Пятница"),
                            ("saturday", "Суббота"),
                            ("sunday", "Воскресенье"),
                        ],
                        max_length=9,
                        verbose_name="День недели",
                    ),
                ),
                ("opening_time", models.TimeField(verbose_name="Время открытия")),
                ("closing_time", models.TimeField(verbose_name="Время закрытия")),
            ],
        ),
        migrations.AddField(
            model_name="address",
            name="schedules",
            field=models.ManyToManyField(
                related_name="addresses", to="cashbox_app.schedule"
            ),
        ),
    ]