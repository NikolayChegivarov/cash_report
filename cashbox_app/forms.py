from django import forms
from django.contrib.auth.forms import AuthenticationForm
from cashbox_app.models import Address, CashReport, CustomUser


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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'home']


class CashReportForm(forms.ModelForm):
    class Meta:
        model = CashReport
        fields = [
            'id_address', 'cas_register', 'cash_balance_beginning',
            'introduced', 'interest_return', 'loans_issued', 'used_farming',
            'boss_took_it', 'cash_register_end', 'author', 'status'
        ]
