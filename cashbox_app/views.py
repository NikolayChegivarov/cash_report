from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Max
from django.utils.timezone import now
from django.shortcuts import redirect
from cashbox_app.forms import CustomAuthenticationForm, AddressSelectionForm
from cashbox_app.models import Address, CashReport, CashRegisterChoices
from .forms import MultiCashReportForm


class CustomLoginView(LoginView):
    """Представление для авторизации."""
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('address_selection')  # .html

    def form_valid(self, form):
        """
        Проверяет валидность формы и выполняет действия при успешной валидации.

        Этот метод вызывается после того, как форма была успешно валидирана.
        Он проверяет данные формы, выводит имя пользователя и затем передает управление родительскому классу.

        :param form: Объект формы Django, содержащий очищенные данные
        :return: True, если форма валидна, False в противном случае
        """
        user = form.cleaned_data.get('username')
        print(f'Вошел пользователь: {user}')
        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает URL успешного завершения для текущего представления."""
        return self.success_url


class AddressSelectionView(FormView):
    """Представление для выбора адреса."""
    template_name = 'address_selection.html'
    form_class = AddressSelectionForm
    success_url = reverse_lazy('cash_report_form')

    def form_valid(self, form):
        selected_address = form.cleaned_data['addresses']
        self.request.session['selected_address_id'] = selected_address.id

        # Получаем текущего пользователя
        current_user = self.request.user

        print(f'Пользователь {current_user} выбрал адрес {selected_address}')

        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает URL успешного завершения для текущего представления."""
        return self.success_url


def current_balance(address_id):
    """Функция для получения текущего баланса кассы"""
    # Создаю словарь с балансами касс.
    balance = {'buying_up': None, 'pawnshop': None, 'technique': None}

    # BUYING_UP
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

    # PAWNSHOP
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

    # TECHNIQUE
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
    """Представление для внесения изменений в кассовых балансах."""

    template_name = 'cash_report_form.html'
    form_class = MultiCashReportForm

    def get_initial(self):
        """
        Функция для получения начальных значений данных формы.

        Возвращает словарь с начальными значениями полей формы,
        включая выбранный адрес и автора (текущего пользователя).
        """
        initial = {}
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user

        # # Распечатка содержимого request
        # print("-" * 50)
        # print("Содержимое request:")
        # for attr_name in dir(self.request):
        #     if not attr_name.startswith('__'):
        #         try:
        #             value = getattr(self.request, attr_name)
        #             print(f"{attr_name}: {value}")
        #         except Exception as e:
        #             print(f"Ошибка при доступе к {attr_name}: {str(e)}")
        # print("-" * 50)

        return initial

    def post(self, request, *args, **kwargs):
        """
        Этот метод обрабатывает отправку формы на сервер.
        Он проверяет валидность формы, если форма валидна, то сохраняет данные и возвращает успешный ответ.
        Если форма невалидна, то выводит ошибки и возвращает ответ о некорректности данных.
        """
        form = self.get_form()
        if form.is_valid():
            result = form.save()
            print(f"Результат сохранения: {result}")
            return self.form_valid(form)
        else:
            print("Форма невалидна:", form.errors)
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        """
        Конфигурирует форму, отключая поля, которые не должны быть изменены.
        """
        # Получает экземпляр формы из родительского класса
        form = super().get_form(form_class)

        # Ограничивает queryset поля id_address только одним выбранным адресом
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            form.fields['id_address'].queryset = Address.objects.filter(id=selected_address_id)
        else:
            form.fields['id_address'].queryset = Address.objects.all()[:1]

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
        form.fields['id_address'].disabled = True
        form.fields['author'].disabled = True
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
        """Возвращает URL успешного завершения для текущего представления."""
        return reverse_lazy('report_submitted')


class ReportSubmittedView(FormView):
    """
    Форма с результатом сохранения изменений в балансах касс.
    """
    template_name = 'report_submitted.html'
    form_class = MultiCashReportForm

    def get_initial(self):
        initial = {}
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user

        return initial

    def get_form(self, form_class=None):
        """
        Конфигурирует форму, отключая поля, которые не должны быть изменены.
        """
        form = super().get_form(form_class)

        # Ограничивает queryset поля id_address только одним выбранным адресом
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            form.fields['id_address'].queryset = Address.objects.filter(id=selected_address_id)
        else:
            form.fields['id_address'].queryset = Address.objects.all()[:1]

        address_id = selected_address_id

        # ПОЛУЧАЮ ДАННЫЕ ИЗ БД.
        # BUYING_UP.
        buying_up_reports_BUYING_UP = CashReport.objects.filter(
            cas_register=CashRegisterChoices.BUYING_UP,
            id_address_id=address_id
        ).annotate(
            last_updated=Max('updated_at')
        ).order_by('-last_updated').first()
        # PAWNSHOP.
        buying_up_reports_PAWNSHOP = CashReport.objects.filter(
            cas_register=CashRegisterChoices.PAWNSHOP,
            id_address_id=address_id
        ).annotate(
            last_updated=Max('updated_at')
        ).order_by('-last_updated').first()
        # TECHNIQUE.
        buying_up_reports_TECHNIQUE = CashReport.objects.filter(
            cas_register=CashRegisterChoices.TECHNIQUE,
            id_address_id=address_id
        ).annotate(
            last_updated=Max('updated_at')
        ).order_by('-last_updated').first()

        print(f'тест:{buying_up_reports_BUYING_UP}')

        # Устанавливаю значения для полей.
        # Общее
        form.initial['data'] = now().strftime('%Y-%m-%d')
        # BUYING_UP.
        form.initial['cas_register_buying_up'] = buying_up_reports_BUYING_UP.cas_register
        form.initial['cash_balance_beginning_buying_up'] = buying_up_reports_BUYING_UP.cash_balance_beginning
        form.initial['introduced_buying_up'] = buying_up_reports_BUYING_UP.introduced
        form.initial['interest_return_buying_up'] = buying_up_reports_BUYING_UP.interest_return
        form.initial['loans_issued_buying_up'] = buying_up_reports_BUYING_UP.loans_issued
        form.initial['used_farming_buying_up'] = buying_up_reports_BUYING_UP.used_farming
        form.initial['boss_took_it_buying_up'] = buying_up_reports_BUYING_UP.boss_took_it
        form.initial['cash_register_end_buying_up'] = buying_up_reports_BUYING_UP.cash_register_end
        # PAWNSHOP.
        form.initial['cas_register_pawnshop'] = buying_up_reports_PAWNSHOP.cas_register
        form.initial['cash_balance_beginning_pawnshop'] = buying_up_reports_PAWNSHOP.cash_balance_beginning
        form.initial['introduced_pawnshop'] = buying_up_reports_PAWNSHOP.introduced
        form.initial['interest_return_pawnshop'] = buying_up_reports_PAWNSHOP.interest_return
        form.initial['loans_issued_pawnshop'] = buying_up_reports_PAWNSHOP.loans_issued
        form.initial['used_farming_pawnshop'] = buying_up_reports_PAWNSHOP.used_farming
        form.initial['boss_took_it_pawnshop'] = buying_up_reports_PAWNSHOP.boss_took_it
        form.initial['cash_register_end_pawnshop'] = buying_up_reports_PAWNSHOP.cash_register_end
        # TECHNIQUE.
        form.initial['cas_register_technique'] = buying_up_reports_TECHNIQUE.cas_register
        form.initial['cash_balance_beginning_technique'] = buying_up_reports_TECHNIQUE.cash_balance_beginning
        form.initial['introduced_technique'] = buying_up_reports_TECHNIQUE.introduced
        form.initial['interest_return_technique'] = buying_up_reports_TECHNIQUE.interest_return
        form.initial['loans_issued_technique'] = buying_up_reports_TECHNIQUE.loans_issued
        form.initial['used_farming_technique'] = buying_up_reports_TECHNIQUE.used_farming
        form.initial['boss_took_it_technique'] = buying_up_reports_TECHNIQUE.boss_took_it
        form.initial['cash_register_end_technique'] = buying_up_reports_TECHNIQUE.cash_register_end

        # ОТКЛЮЧАЮ ПОЛЯ ДЛЯ РЕДАКТИРОВАНИЯ.
        form.fields['author'].disabled = True
        form.fields['id_address'].disabled = True
        form.fields['data'].disabled = True
        # BUYING_UP.
        form.fields['cas_register_buying_up'].disabled = True
        form.fields['cash_balance_beginning_buying_up'].disabled = True
        form.fields['introduced_buying_up'].disabled = True
        form.fields['interest_return_buying_up'].disabled = True
        form.fields['loans_issued_buying_up'].disabled = True
        form.fields['used_farming_buying_up'].disabled = True
        form.fields['boss_took_it_buying_up'].disabled = True
        form.fields['cash_register_end_buying_up'].disabled = True
        # PAWNSHOP.
        form.fields['cas_register_pawnshop'].disabled = True
        form.fields['cash_balance_beginning_pawnshop'].disabled = True
        form.fields['introduced_pawnshop'].disabled = True
        form.fields['interest_return_pawnshop'].disabled = True
        form.fields['loans_issued_pawnshop'].disabled = True
        form.fields['used_farming_pawnshop'].disabled = True
        form.fields['boss_took_it_pawnshop'].disabled = True
        form.fields['cash_register_end_pawnshop'].disabled = True
        # TECHNIQUE.
        form.fields['cas_register_technique'].disabled = True
        form.fields['cash_balance_beginning_technique'].disabled = True
        form.fields['introduced_technique'].disabled = True
        form.fields['interest_return_technique'].disabled = True
        form.fields['loans_issued_technique'].disabled = True
        form.fields['used_farming_technique'].disabled = True
        form.fields['boss_took_it_technique'].disabled = True
        form.fields['cash_register_end_technique'].disabled = True

        # Запрет на редактирование статуса.
        if hasattr(form, 'fields') and 'status' in form.fields:
            form.fields['status'].disabled = True

        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            submit_button = request.POST.get('submit_button')
            if submit_button == 'Сменить пользователя':
                return redirect(reverse_lazy('login'))
            elif submit_button == 'Сменить адрес':
                return redirect(reverse_lazy('address_selection'))
            elif submit_button == 'Новый день':
                return redirect(reverse_lazy('cash_report_form'))

        return self.render_to_response(self.get_context_data(form=form))
