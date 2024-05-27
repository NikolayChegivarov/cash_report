from rest_framework import serializers
from .models import Address, CustomUser, CashReport


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CashReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReport
        fields = '__all__'
        depth = 1  # Это будет включать связанные поля в сериализованный вывод.
