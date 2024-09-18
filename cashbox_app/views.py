from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from cashbox_app.forms import CustomAuthenticationForm, AddressForm, CashReportForm, AddressSelectionForm
from cashbox_app.models import Address, CashReport

from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MultiCashReportForm

from django.views.generic.base import View


# Страница авторизации с переходом на страницу выбор адреса.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('address_selection')  # .html

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
        return super().form_valid(form)

    def get_success_url(self):
        # Переопределяем метод для получения URL перенаправления после успешного выбора адреса
        return self.success_url


# Заполнение отчета.
class CashReportFormView(LoginRequiredMixin, FormView):
    # Указывает имя шаблона для отображения формы
    template_name = 'cash_report_form.html'
    # Указывает класс формы, который будет использоваться
    form_class = MultiCashReportForm
    # URL, на который пользователь будет перенаправлен после успешной отправки формы
    success_url = reverse_lazy('report_submitted')

    def get_initial(self):
        # Получает начальные значения из родительского класса
        initial = super().get_initial()
        # Проверяет наличие ID выбранного адреса в сессии пользователя
        selected_address_id = self.request.session.get('selected_address_id')
        # Если ID адрес существует, устанавливает его как начальное значение поля id_address
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        # Устанавливает текущего пользователя как автора отчета
        initial['author'] = self.request.user
        # Возвращает словарь с начальными значениями
        return initial

    def get_form(self, form_class=None):
        """Конфигурирует форму, отключая поля, которые не должны быть изменены."""
        # Получает экземпляр формы из родительского класса
        form = super().get_form(form_class)
        # Ограничивает queryset поля id_address только одним выбранным адресом
        form.fields['id_address'].queryset = Address.objects.filter(id=self.request.session.get('selected_address_id'))
        # Удаляет пустую метку для поля id_address
        form.fields['id_address'].empty_label = None
        # Отключает поле id_address для редактирования
        form.fields['id_address'].disabled = True
        # Отключает поле author для редактирования
        form.fields['author'].disabled = True
        # Возвращает настроенную форму
        return form

    def form_valid(self, form):
        # Создайте новый экземпляр CashReport вручную.
        cash_report = CashReport.objects.create(
            author=self.request.user,
            id_address_id=self.request.session.get('selected_address_id')
        )

        # При необходимости вы можете сохранить здесь данные формы.

        return super().form_valid(form)


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


