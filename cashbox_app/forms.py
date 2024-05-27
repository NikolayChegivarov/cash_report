from django import forms
from django.contrib.auth.forms import AuthenticationForm
from cashbox_app.models import Address, CashReport, CustomUser


# Форма для страницы авторизации.
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        to_field_name='username',
        label='Имя пользователя',
        empty_label=None
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


# Для создания адреса или редактирования существующего.
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'home']


# Форма выбора адреса.
class AddressSelectionForm(forms.Form):
    addresses = forms.ModelChoiceField(queryset=Address.objects.all(), empty_label="Выберите адрес")


# Форма редактирования кассового отчета.
class CashReportForm(forms.ModelForm):
    class Meta:
        model = CashReport
        fields = [
            'id_address', 'cas_register', 'cash_balance_beginning',
            'introduced', 'interest_return', 'loans_issued', 'used_farming',
            'boss_took_it', 'cash_register_end', 'author', 'status'
        ]
        widgets = {  # Эти поля доступны только для чтения.
            'id_address': forms.Select(attrs={'readonly': 'readonly'}),
            'author': forms.TextInput(attrs={'readonly': 'readonly'})
        }
