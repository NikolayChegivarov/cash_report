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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cas_register'].widget.attrs['onclick'] = 'this.checked=true;'

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

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем, что все обязательные поля заполнены
        required_fields = ['author', 'id_address', 'cas_register']
        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                raise forms.ValidationError(f"Обязательное поле '{field_name}' не заполнено.")

        # Остальная часть валидации...
        for field_name in self.fields.keys():
            if not cleaned_data.get(field_name):
                raise forms.ValidationError(f"Поле '{field_name}' не должно быть пустым.")

        return cleaned_data


def calculate_cash_register_end(self, cleaned_data, register_type):
    print(f'Используется функция подсчета остатка на конец дня: calculate_cash_register_end')
    print(f'cleaned_data_________{cleaned_data}')
    fields = [
        f'cash_balance_beginning_{register_type}',
        f'introduced_{register_type}',
        f'interest_return_{register_type}',
        f'loans_issued_{register_type}',
        f'used_farming_{register_type}',
        f'boss_took_it_{register_type}'
    ]

    total = sum(float(cleaned_data.get(field, 0)) for field in fields[:3])
    total -= sum(float(cleaned_data.get(field, 0)) for field in fields[3:])

    cleaned_data[f'cash_register_end_{register_type}'] = round(total, 2)


class MultiCashReportForm(forms.Form):
    print(f"MultiCashReportForm")

    author = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    id_address = forms.ModelChoiceField(queryset=Address.objects.all())

    # Формы для скупки.
    cas_register_buying_up = forms.ChoiceField(choices=CashRegisterChoices.choices, initial='BUYING_UP')
    cash_balance_beginning_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    introduced_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    interest_return_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    loans_issued_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    used_farming_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    boss_took_it_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    cash_register_end_buying_up = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Формы для ломбарда
    cas_register_pawnshop = forms.ChoiceField(choices=CashRegisterChoices.choices, initial='PAWNSHOP')
    cash_balance_beginning_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    introduced_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    interest_return_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    loans_issued_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    used_farming_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    boss_took_it_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
    cash_register_end_pawnshop = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Формы для техники.
    cas_register_technique = forms.ChoiceField(choices=CashRegisterChoices.choices, initial='TECHNIQUE')
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
        print(f"Начало сохранения данных. Дата: {shift_date}")
        try:
            # Buying Up report
            buying_up_report = CashReport(
                shift_date=shift_date,
                id_address=self.cleaned_data['id_address'],
                author=self.cleaned_data['author'],
                cas_register=self.cleaned_data['cas_register_buying_up'],
                cash_balance_beginning=self.cleaned_data['cash_balance_beginning_buying_up'],
                introduced=self.cleaned_data['introduced_buying_up'],
                interest_return=self.cleaned_data['interest_return_buying_up'],
                loans_issued=self.cleaned_data['loans_issued_buying_up'],
                used_farming=self.cleaned_data['used_farming_buying_up'],
                boss_took_it=self.cleaned_data['boss_took_it_buying_up'],
                cash_register_end=self.cleaned_data['cash_register_end_buying_up'],
                status=self.cleaned_data['status']
            )
            print(f"Buying Up report создан: {buying_up_report}")
            buying_up_report.save()
            print(f"Buying Up report сохранен")

            # Pawnshop report
            pawnshop_report = CashReport(
                shift_date=shift_date,
                id_address=self.cleaned_data['id_address'],
                author=self.cleaned_data['author'],
                cas_register=self.cleaned_data['cas_register_pawnshop'],
                cash_balance_beginning=self.cleaned_data['cash_balance_beginning_pawnshop'],
                introduced=self.cleaned_data['introduced_pawnshop'],
                interest_return=self.cleaned_data['interest_return_pawnshop'],
                loans_issued=self.cleaned_data['loans_issued_pawnshop'],
                used_farming=self.cleaned_data['used_farming_pawnshop'],
                boss_took_it=self.cleaned_data['boss_took_it_pawnshop'],
                cash_register_end=self.cleaned_data['cash_register_end_pawnshop'],
                status=self.cleaned_data['status']
            )
            print(f"Pawnshop report создан: {pawnshop_report}")
            pawnshop_report.save()
            print(f"Pawnshop report сохранен")

            # Technique report
            technique_report = CashReport(
                shift_date=shift_date,
                id_address=self.cleaned_data['id_address'],
                author=self.cleaned_data['author'],
                cas_register=self.cleaned_data['cas_register_technique'],
                cash_balance_beginning=self.cleaned_data['cash_balance_beginning_technique'],
                introduced=self.cleaned_data['introduced_technique'],
                interest_return=self.cleaned_data['interest_return_technique'],
                loans_issued=self.cleaned_data['loans_issued_technique'],
                used_farming=self.cleaned_data['used_farming_technique'],
                boss_took_it=self.cleaned_data['boss_took_it_technique'],
                cash_register_end=self.cleaned_data['cash_register_end_technique'],
                status=self.cleaned_data['status']
            )
            print(f"Technique report создан: {technique_report}")
            technique_report.save()
            print(f"Technique report сохранен")

            print("Все данные успешно сохранены")
            return True

        except Exception as e:
            print(f"Произошла ошибка при сохранении данных: {str(e)}")
            return False

    def clean(self):
        cleaned_data = super().clean()

        # Расчет для покупок
        calculate_cash_register_end(self, cleaned_data, 'buying_up')
        # Расчет для ломбарда
        calculate_cash_register_end(self, cleaned_data, 'pawnshop')
        # Расчет для техники
        calculate_cash_register_end(self, cleaned_data, 'technique')
        return cleaned_data


class ResultForm(forms.Form):

    today_date = forms.DateField()

    # ТП Адрес
    # Дата, cash_register, balance

    pass

