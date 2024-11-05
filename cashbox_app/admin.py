from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Address, Schedule


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "get_address_schedules")
    search_fields = ["city", "street", "home"]
    list_filter = ["city"]

    def get_address_schedules(self, obj):
        schedules = obj.address_schedules.all()
        return "\n".join(
            [
                f"{schedule.day_of_week}: {schedule.opening_time} - {schedule.closing_time}"
                for schedule in schedules
            ]
        )

    get_address_schedules.short_description = "Расписание"

    # Используем id вместо adress_id
    def get_id(self, obj):
        return obj.id

    get_id.short_description = "ID адреса"


@admin.register(Schedule)
class AddressScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "day_of_week",
        "opening_time",
        "closing_time",
        "get_adress_id",  # Добавляем новое поле
    )
    list_filter = ["day_of_week"]

    def get_adress_id(self, obj):  # Создаем новый метод
        return obj.address.id if obj.address else "-"

    get_adress_id.short_description = "ID адреса"  # Устанавливаем описание поля


# Добавить пользователя.
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
