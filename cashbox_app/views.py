from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from cashbox_app.forms import CustomAuthenticationForm, AddressForm, CashReportForm, AddressSelectionForm, ResultForm
from cashbox_app.models import Address, CashReport, CashRegisterChoices

from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MultiCashReportForm
# from django.db.models import Q
from django.db.models import F
from django.db.models import Max
from django.utils import timezone
from django.views.generic.base import View
from django.utils.timezone import now
from datetime import datetime



# Страница авторизации с переходом на страницу выбор адреса.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('address_selection')  # .html

    def form_valid(self, form):
        """Функция только для вывода пользователя в консоль."""
        user = form.cleaned_data.get('username')
        print(f'Вошел пользователь: {user}')
        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем метод для получения URL перенаправления после успешного входа
        return self.success_url


# Выбор адреса с переходом на страницу заполнения отчета.
class AddressSelectionView(FormView):
    template_name = 'address_selection.html'
    form_class = AddressSelectionForm
    success_url = reverse_lazy('cash_report_form')  # .html

    def form_valid(self, form):
        selected_address = form.cleaned_data['addresses']
        self.request.session['selected_address_id'] = selected_address.id

        # Получаем текущего пользователя
        current_user = self.request.user

        # Распечатываем сообщение
        print(f'Пользователь {current_user} выбрал адрес {selected_address}')

        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем метод для получения URL перенаправления после успешного выбора адреса
        return self.success_url


def current_balance(address_id):
    """Получение текущего баланса кассы"""
    # Создаю словарь с балансами касс.
    balance = {'buying_up': None, 'pawnshop': None, 'technique': None}

    # Получаем все отчеты по скупке для указанного адреса
    buying_up_reports_BUYING_UP = CashReport.objects.filter(
        cas_register=CashRegisterChoices.BUYING_UP,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_BUYING_UP:
        # Если результат есть, добавляю его в словарь.
        balance['buying_up'] = buying_up_reports_BUYING_UP['cash_register_end']
        print(f'Текущий баланс BUYING_UP: {balance.get('buying_up')}')
    else:
        # Если значения нет. Устанавливаю 0
        balance['buying_up'] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    # Получаем все отчеты по ломбарду для указанного адреса.
    buying_up_reports_PAWNSHOP = CashReport.objects.filter(
        cas_register=CashRegisterChoices.PAWNSHOP,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_PAWNSHOP:
        balance['pawnshop'] = buying_up_reports_PAWNSHOP['cash_register_end']
        print(f'Текущий баланс PAWNSHOP: {balance.get('pawnshop')}')
    else:
        balance['pawnshop'] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    # Получаем все отчеты по ломбарду для указанного адреса.
    buying_up_reports_TECHNIQUE = CashReport.objects.filter(
        cas_register=CashRegisterChoices.TECHNIQUE,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_TECHNIQUE:
        balance['technique'] = buying_up_reports_TECHNIQUE['cash_register_end']
        print(f'Текущий баланс TECHNIQUE: {balance.get('technique')}')
    else:
        balance['technique'] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    return balance


class CashReportFormView(LoginRequiredMixin, FormView):
    template_name = 'cash_report_form.html'
    form_class = MultiCashReportForm

    def get_initial(self):
        initial = {}
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user

        # Распечатка содержимого request
        print("-" * 50)
        print("Содержимое request:")
        for attr_name in dir(self.request):
            if not attr_name.startswith('__'):
                try:
                    value = getattr(self.request, attr_name)
                    print(f"{attr_name}: {value}")
                except Exception as e:
                    print(f"Ошибка при доступе к {attr_name}: {str(e)}")
        print("-" * 50)

        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            result = form.save()
            print(f"Результат сохранения: {result}")
            return self.form_valid(form)
        else:
            print("Форма невалидна:", form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('report_submitted')

    def get_form(self, form_class=None):
        """Конфигурирует форму, отключая поля, которые не должны быть изменены."""
        # Получает экземпляр формы из родительского класса
        form = super().get_form(form_class)

        # Ограничивает queryset поля id_address только одним выбранным адресом
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            form.fields['id_address'].queryset = Address.objects.filter(id=selected_address_id)
        else:
            form.fields['id_address'].queryset = Address.objects.all()[:1]

        # Отключает поле id_address для редактирования
        form.fields['id_address'].disabled = True

        # Отключает поле author для редактирования
        form.fields['author'].disabled = True

        # Получаем актуальные балансы касс
        current_balance_ = current_balance(selected_address_id)

        # Устанавливаю значения для полей.
        form.initial['data'] = now().strftime('%Y-%m-%d')

        form.initial['cas_register_buying_up'] = CashRegisterChoices.BUYING_UP
        form.initial['cash_balance_beginning_buying_up'] = current_balance_['buying_up']

        form.initial['cas_register_pawnshop'] = CashRegisterChoices.PAWNSHOP
        form.initial['cash_balance_beginning_pawnshop'] = current_balance_['pawnshop']

        form.initial['cas_register_technique'] = CashRegisterChoices.TECHNIQUE
        form.initial['cash_balance_beginning_technique'] = current_balance_['technique']

        # Отключаю поля для редактирования
        form.fields['cas_register_buying_up'].disabled = True
        form.fields['cash_balance_beginning_buying_up'].disabled = True
        form.fields['cas_register_pawnshop'].disabled = True
        form.fields['cash_balance_beginning_pawnshop'].disabled = True
        form.fields['cas_register_technique'].disabled = True
        form.fields['cash_balance_beginning_technique'].disabled = True
        form.fields['cash_register_end_buying_up'].disabled = True
        form.fields['cash_register_end_pawnshop'].disabled = True
        form.fields['cash_register_end_technique'].disabled = True

        # Запрет на редактирование статуса.
        if hasattr(form, 'fields') and 'status' in form.fields:
            form.fields['status'].disabled = True

        print(f"Selected address ID: {selected_address_id}")
        print(f"Current balances: {current_balance_}")

        return form


class ReportSubmittedView(FormView):
    # Указывает имя шаблона для отображения формы
    template_name = 'report_submitted.html'
    # form_class = ResultForm
    form_class = MultiCashReportForm

    def get_initial(self):
        initial = {}
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user

        return initial

    def get_form(self, form_class=None):
        """Конфигурирует форму, отключая поля, которые не должны быть изменены."""
        # Получает экземпляр формы из родительского класса
        form = super().get_form(form_class)

        # Ограничивает queryset поля id_address только одним выбранным адресом
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            form.fields['id_address'].queryset = Address.objects.filter(id=selected_address_id)
        else:
            form.fields['id_address'].queryset = Address.objects.all()[:1]

        # Отключает поле id_address для редактирования
        form.fields['id_address'].disabled = True

        # Отключает поле author для редактирования
        form.fields['author'].disabled = True

        # Получаем актуальные балансы касс.
        current_balance_ = current_balance(selected_address_id)

        # получаю данные из бд.


        # Устанавливаю значения для полей.
        form.initial['data'] = now().strftime('%Y-%m-%d')

        form.initial['cas_register_buying_up'] = CashRegisterChoices.BUYING_UP
        # form.initial[''] =
        form.initial['cash_register_end_buying_up'] = current_balance_['buying_up']


        form.initial['cas_register_pawnshop'] = CashRegisterChoices.PAWNSHOP
        form.initial['cash_register_end_pawnshop'] = current_balance_['pawnshop']

        form.initial['cas_register_technique'] = CashRegisterChoices.TECHNIQUE
        form.initial['cash_register_end_technique'] = current_balance_['technique']

        # Отключаю поля для редактирования.
        form.fields['cas_register_buying_up'].disabled = True
        form.fields['cash_balance_beginning_buying_up'].disabled = True
        form.fields['cas_register_pawnshop'].disabled = True
        form.fields['cash_balance_beginning_pawnshop'].disabled = True
        form.fields['cas_register_technique'].disabled = True
        form.fields['cash_balance_beginning_technique'].disabled = True
        form.fields['cash_register_end_buying_up'].disabled = True
        form.fields['cash_register_end_pawnshop'].disabled = True
        form.fields['cash_register_end_technique'].disabled = True

        # Запрет на редактирование статуса.
        if hasattr(form, 'fields') and 'status' in form.fields:
            form.fields['status'].disabled = True

        print(f"Selected address ID: {selected_address_id}")
        print(f"Current balances: {current_balance_}")

        return form

    def get_success_url(self):
        return reverse_lazy('login')


    # URL, на который пользователь будет перенаправлен после успешной отправки формы
    # "Сменить пользователя"
    # success_url = reverse_lazy('login')
    # # "Сменить адрес"
    # success_url = reverse_lazy('address_selection.html')
    # # "Новый день"
    # success_url = reverse_lazy('cash_report_form.html')


