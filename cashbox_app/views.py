from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from cashbox_app.forms import CustomAuthenticationForm, AddressForm, CashReportForm


# Страница авторизации с переходом на страницу выбор адреса.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('address_selection')


# Выбор адреса с переходом на страницу заполнения отчета.
class AddressSelectionView(TemplateView):
    template_name = 'address_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте здесь любые дополнительные данные, которые вы хотите передать в шаблон
        return context


# Заполнение отчета.
class CashReportFormView(FormView):
    template_name = 'cash_report_form.html'
    form_class = CashReportForm
    success_url = reverse_lazy('report_submitted')

    def form_valid(self, form):
        # Обработайте данные формы здесь
        return super().form_valid(form)
