from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class Address(models.Model):
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    home = models.CharField(max_length=10, verbose_name='Номер дома')

    def __str__(self):
        return f"{self.city}, {self.street}, {self.home}"


class CustomUserManager(BaseUserManager):  # Переопределяю методы для CustomUser

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, username, password=None, **extra_fields):
        # Указываем, какие поля должны быть включены в форму админки.
        fields = (
        'username', 'email', 'last_name', 'first_name', 'patronymic', 'is_active', 'is_staff', 'is_superuser', 'groups',
        'user_permissions')
        # Проверка наличия username, если его нет, выбрасывается исключение
        if not username:
            raise ValueError('Поле Имя пользователя должно быть установлено')
        # Создание экземпляра пользователя с заданными параметрами.
        user = self.model(username=username, **extra_fields)
        # Установка пароля для пользователя
        user.set_password(password)
        # Сохранение пользователя в базе данных
        user.save(using=self._db)
        # Возвращение созданного пользователя
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Установка полей is_staff и is_superuser в True по умолчанию
        extra_fields.setdefault('is_staff', True)  # по умолчанию не имеет доступа к административной панели Django.
        extra_fields.setdefault('is_superuser', True)  # по умолчанию пользователь не является суперпользователем.
        # Вызов метода create_user для создания суперпользователя с заданными параметрами
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):   # Пользователь.
    username = models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя', default='default_username')
    email = models.EmailField(unique=True, verbose_name='Email', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя', blank=True, null=True)
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Если не активен, то не сможет авторизоваться на сайте.
    is_staff = models.BooleanField(default=False)  # Может ли войти в "админку".

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Изменено на 'username'
    # REQUIRED_FIELDS = ['patronymic']  # 'email', 'last_name', 'first_name',   # Обязательные поля.

    def __str__(self):
        return self.username


class CashRegisterChoices(models.TextChoices):  # Разновидность кассы.
    BUYING_UP = "BUYING_UP", "Скупка"
    PAWNSHOP = "PAWNSHOP", "Ломбард"
    TECHNIQUE = "TECHNIQUE", "Техника"


class CashReportStatusChoices(models.TextChoices):  # Статусы отчета.
    """Статусы кассового отчета. Определяет набор допустимых
    значений для поля status с помощью атрибута choices
    в классе Advertisement."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class CashReport(models.Model):  # Кассовый отчет.
    shift_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата смены')
    id_address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес')
    cas_register = models.CharField(
        max_length=10,
        choices=CashRegisterChoices.choices,
    )
    cash_balance_beginning = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Остаток денежных средств в начале', blank=False, null=False)
    introduced = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Внесено в кассу', blank=False, null=False, default=0.00)
    interest_return = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Средства от процентов с залога, возврата выданных займов',
        blank=False, null=False, default=0.00)
    loans_issued = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Выдано займов', blank=False, null=False, default=0.00)
    used_farming = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='На хоз. нужды, оплату труда', blank=False, null=False,
        default=0.00)
    boss_took_it = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Выемка денежных средств руководителем', blank=False,
        null=False, default=0.00)
    cash_register_end = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Остаток на конец дня', blank=False, null=False)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Сотрудник смены', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=False, null=False)
    status = models.CharField(
        max_length=10,
        choices=CashReportStatusChoices.choices,
        default=CashReportStatusChoices.OPEN
    )

    class Meta:
        unique_together = ('shift_date', 'id_address',)  # Комбинация уникальна как primary_key.

    def __str__(self):
        return f"{self.shift_date} - {self.id_address}"

