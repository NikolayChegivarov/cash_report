# import datetime
from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from cashbox_app.models import Address, CashReport, CustomUser, CashReportStatusChoices, CashRegisterChoices


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


class CashReportForm(forms.ModelForm):
    class Meta:
        model = CashReport
        fields = [
            'author', 'id_address', 'cas_register', 'cash_balance_beginning',
            'introduced', 'interest_return', 'loans_issued', 'used_farming',
            'boss_took_it', 'cash_register_end', 'status'
        ]
        widgets = {
            'id_address': forms.Select(attrs={'readonly': 'readonly'}),
            'author': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class MultiCashReportForm(forms.Form):
    author = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    id_address = forms.ModelChoiceField(queryset=Address.objects.all())

    # Формы для скупки.
    cash_balance_beginning_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    introduced_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    interest_return_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    loans_issued_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    used_farming_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    boss_took_it_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    cash_register_end_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Формы для ломбарда
    cash_balance_beginning_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    introduced_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    interest_return_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    loans_issued_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    used_farming_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    boss_took_it_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    cash_register_end_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Формы для техники.
    cash_balance_beginning_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    introduced_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    interest_return_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    loans_issued_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    used_farming_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    boss_took_it_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    cash_register_end_technique = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    status = forms.ChoiceField(choices=CashReportStatusChoices.choices, initial=CashReportStatusChoices.OPEN)

    def save(self):
        shift_date = datetime.now()

        buying_up_report = CashReport(
            shift_date=shift_date,
            id_address=self.cleaned_data['id_address'],
            author=self.cleaned_data['author'],
            cas_register=CashRegisterChoices.BUYING_UP,
            cash_balance_beginning=self.cleaned_data['cash_balance_beginning_buying_up'],
            introduced=self.cleaned_data['introduced_buying_up'],
            interest_return=self.cleaned_data['interest_return_buying_up'],
            loans_issued=self.cleaned_data['loans_issued_buying_up'],
            used_farming=self.cleaned_data['used_farming_buying_up'],
            boss_took_it=self.cleaned_data['boss_took_it_buying_up'],
            cash_register_end=self.cleaned_data['cash_register_end_buying_up'],
            status=self.cleaned_data['status']
        )
        buying_up_report.save()

        pawnshop_report = CashReport(
            shift_date=shift_date,
            id_address=self.cleaned_data['id_address'],
            author=self.cleaned_data['author'],
            cas_register=CashRegisterChoices.PAWNSHOP,
            cash_balance_beginning=self.cleaned_data['cash_balance_beginning_pawnshop'],
            introduced=self.cleaned_data['introduced_pawnshop'],
            interest_return=self.cleaned_data['interest_return_pawnshop'],
            loans_issued=self.cleaned_data['loans_issued_pawnshop'],
            used_farming=self.cleaned_data['used_farming_pawnshop'],
            boss_took_it=self.cleaned_data['boss_took_it_pawnshop'],
            cash_register_end=self.cleaned_data['cash_register_end_pawnshop'],
            status=self.cleaned_data['status']
        )
        pawnshop_report.save()

        technique_report = CashReport(
            shift_date=shift_date,
            id_address=self.cleaned_data['id_address'],
            author=self.cleaned_data['author'],
            cas_register=CashRegisterChoices.TECHNIQUE,
            cash_balance_beginning=self.cleaned_data['cash_balance_beginning_technique'],
            introduced=self.cleaned_data['introduced_technique'],
            interest_return=self.cleaned_data['interest_return_technique'],
            loans_issued=self.cleaned_data['loans_issued_technique'],
            used_farming=self.cleaned_data['used_farming_technique'],
            boss_took_it=self.cleaned_data['boss_took_it_technique'],
            cash_register_end=self.cleaned_data['cash_register_end_technique'],
            status=self.cleaned_data['status']
        )
        technique_report.save()

