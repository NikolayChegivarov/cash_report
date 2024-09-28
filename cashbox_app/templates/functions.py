

def current_balance(address_id):
    from cashbox_app.models import CashReport, CashRegisterChoices
    from django.db.models import Max
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

current_balance(2)