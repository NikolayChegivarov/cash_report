# Generated by Django 5.0.7 on 2024-12-04 15:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("city", models.CharField(max_length=100, verbose_name="Город")),
                ("street", models.CharField(max_length=100, verbose_name="Улица")),
                ("home", models.CharField(max_length=10, verbose_name="Номер дома")),
            ],
            options={
                "ordering": ["city", "street", "home"],
            },
        ),
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
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        default="default_username",
                        max_length=100,
                        unique=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Фамилия"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Отчество"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
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
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address_schedules",
                        to="cashbox_app.address",
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
                (
                    "client",
                    models.CharField(
                        default="Новый клиент", max_length=50, verbose_name="Клиент"
                    ),
                ),
                (
                    "nomenclature",
                    models.CharField(max_length=50, verbose_name="Наименование"),
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
                        default="gold585",
                        max_length=15,
                        verbose_name="Проба",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена за грамм"
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
                        verbose_name="Статус скупки",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Сотрудник смены",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CashReport",
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
                    "cas_register",
                    models.CharField(
                        choices=[
                            ("BUYING_UP", "Скупка"),
                            ("PAWNSHOP", "Ломбард"),
                            ("TECHNIQUE", "Техника"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "cash_balance_beginning",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Остаток денежных средств в начале",
                    ),
                ),
                (
                    "introduced",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="Внесено в кассу",
                    ),
                ),
                (
                    "interest_return",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="Средства от процентов с залога, возврата выданных займов",
                    ),
                ),
                (
                    "loans_issued",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="Выдано займов",
                    ),
                ),
                (
                    "used_farming",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="На хоз. нужды, оплату труда",
                    ),
                ),
                (
                    "boss_took_it",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="Выемка денежных средств руководителем",
                    ),
                ),
                (
                    "cash_register_end",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Остаток на конец дня",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Дата изменения"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Открыто"),
                            ("CLOSED", "Закрыто"),
                            ("DRAFT", "Черновик"),
                        ],
                        default="OPEN",
                        max_length=10,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Сотрудник смены",
                    ),
                ),
                (
                    "id_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cashbox_app.address",
                        verbose_name="Адрес",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    (
                        "shift_date",
                        "id_address",
                        "cas_register",
                        "cash_balance_beginning",
                        "introduced",
                        "interest_return",
                        "loans_issued",
                        "used_farming",
                        "boss_took_it",
                        "cash_register_end",
                    )
                },
            },
        ),
    ]
