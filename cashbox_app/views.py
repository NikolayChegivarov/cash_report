from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from cashbox_app.forms import CustomAuthenticationForm, AddressForm, CashReportForm, AddressSelectionForm
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
    """Функция для получения текущего баланса кассы"""
    # Создаю словарь с балансами касс.
    BUYING_UP = CashRegisterChoices.BUYING_UP
    PAWNSHOP = CashRegisterChoices.PAWNSHOP
    TECHNIQUE = CashRegisterChoices.TECHNIQUE
    current_balance = {
        BUYING_UP: None,
        PAWNSHOP: None,
        TECHNIQUE: None
    }

    # Получаем все отчеты по скупке для указанного адреса
    buying_up_reports_BUYING_UP = CashReport.objects.filter(
        cas_register=CashRegisterChoices.BUYING_UP,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_BUYING_UP:
        # Если результат есть, добавляю его в словарь.
        current_balance[CashRegisterChoices.BUYING_UP] = buying_up_reports_BUYING_UP['cash_register_end']
        print(f'Текущий баланс BUYING_UP: {current_balance.get('BUYING_UP')}')
    else:
        # Если значения нет. Устанавливаю 0
        current_balance[CashRegisterChoices.BUYING_UP] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    # Получаем все отчеты по ломбарду для указанного адреса.
    buying_up_reports_PAWNSHOP = CashReport.objects.filter(
        cas_register=CashRegisterChoices.PAWNSHOP,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_PAWNSHOP:
        current_balance[CashRegisterChoices.PAWNSHOP] = buying_up_reports_PAWNSHOP['cash_register_end']
        print(f'Текущий баланс PAWNSHOP: {current_balance.get('PAWNSHOP')}')
    else:
        current_balance[CashRegisterChoices.BUYING_UP] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    # Получаем все отчеты по ломбарду для указанного адреса.
    buying_up_reports_TECHNIQUE = CashReport.objects.filter(
        cas_register=CashRegisterChoices.TECHNIQUE,
        id_address_id=address_id
    ).values('cash_register_end').annotate(
        last_updated=Max('updated_at')
    ).order_by('-last_updated').first()

    if buying_up_reports_TECHNIQUE:
        current_balance[CashRegisterChoices.TECHNIQUE] = buying_up_reports_TECHNIQUE['cash_register_end']
        print(f'Текущий баланс TECHNIQUE: {current_balance.get('TECHNIQUE')}')
    else:
        current_balance[CashRegisterChoices.TECHNIQUE] = 0
        print(f"Отчетов по скупке для адреса {address_id} не найдено")

    return current_balance


class CashReportFormView(LoginRequiredMixin, FormView):
    template_name = 'cash_report_form.html'
    form_class = MultiCashReportForm

    def get_initial(self):
        initial = super().get_initial()
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user
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

        # Устанавливаем начальные значения для полей кассовых регистров
        form.initial['cas_register_buying_up'] = CashRegisterChoices.BUYING_UP
        form.initial['cash_balance_beginning_buying_up'] = current_balance_[CashRegisterChoices.BUYING_UP]

        form.initial['cas_register_pawnshop'] = CashRegisterChoices.PAWNSHOP
        form.initial['cash_balance_beginning_pawnshop'] = current_balance_[CashRegisterChoices.PAWNSHOP]

        form.initial['cas_register_technique'] = CashRegisterChoices.TECHNIQUE
        form.initial['cash_balance_beginning_technique'] = current_balance_[CashRegisterChoices.TECHNIQUE]

        # Отключает поля кассовых регистров для редактирования
        form.fields['cas_register_buying_up'].disabled = True
        form.fields['cash_balance_beginning_buying_up'].disabled = True
        form.fields['cas_register_pawnshop'].disabled = True
        form.fields['cash_balance_beginning_pawnshop'].disabled = True
        form.fields['cas_register_technique'].disabled = True
        form.fields['cash_balance_beginning_technique'].disabled = True

        # Запрет на редактирование статуса.
        if hasattr(form, 'fields') and 'status' in form.fields:
            form.fields['status'].disabled = True

        print(f"Selected address ID: {selected_address_id}")
        print(f"Current balances: {current_balance_}")

        return form

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class ReportSubmittedView(FormView):
    # Указывает имя шаблона для отображения формы
    template_name = 'report_submitted.html'
    form_class = MultiCashReportForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')


    # URL, на который пользователь будет перенаправлен после успешной отправки формы
    # "Сменить пользователя"
    # success_url = reverse_lazy('login')
    # # "Сменить адрес"
    # success_url = reverse_lazy('address_selection.html')
    # # "Новый день"
    # success_url = reverse_lazy('cash_report_form.html')


