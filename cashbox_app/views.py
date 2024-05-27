from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from cashbox_app.forms import CustomAuthenticationForm, AddressForm, CashReportForm, AddressSelectionForm
from cashbox_app.models import Address


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
class CashReportFormView(FormView):
    template_name = 'cash_report_form.html'
    form_class = CashReportForm
    success_url = reverse_lazy('report_submitted')

    def get_initial(self):

        initial = super().get_initial()
        selected_address_id = self.request.session.get('selected_address_id')
        if selected_address_id:
            initial['id_address'] = Address.objects.get(id=selected_address_id)
        initial['author'] = self.request.user.username
        return initial

    def get_form(self, form_class=None):
        """Настраивает форму, отключая поля id_addressи author делая их доступными только для чтения."""
        form = super().get_form(form_class)
        form.fields['id_address'].queryset = Address.objects.filter(id=self.request.session.get('selected_address_id'))
        form.fields['id_address'].empty_label = None
        form.fields['id_address'].disabled = True
        form.fields['author'].disabled = True
        return form

    def form_valid(self, form):
        """Гарантирует, что выбранный адрес и вошедший в систему пользователь установлены правильно при отправке формы."""
        form.instance.id_address = Address.objects.get(id=self.request.session.get('selected_address_id'))
        form.instance.author = self.request.user
        return super().form_valid(form)
