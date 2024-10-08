# Generated by Django 5.0.7 on 2024-09-28 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashbox_app', '0007_alter_cashreport_author_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cashreport',
            unique_together={('shift_date', 'id_address', 'cas_register', 'cash_balance_beginning', 'introduced', 'interest_return', 'loans_issued', 'used_farming', 'boss_took_it', 'cash_register_end')},
        ),
    ]
