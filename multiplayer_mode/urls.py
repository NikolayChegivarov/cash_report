"""
Конфигурация URL-адреса для проекта multiplayer_mode.

Список `urlpatterns` направляет URL-адреса в представления. Для получения дополнительной информации см.
https://docs.djangoproject.com/en/5.0/topics/http/urls/.
Примеры:
Представления функций
1. Добавьте импорт: из представлений импорта my_app
2. Добавьте URL-адрес в urlpatterns: path('',views.home, name='home')
Представления на основе классов
1. Добавьте импорт: fromother_app.views import Home
2. Добавьте URL-адрес в urlpatterns: path('', Home.as_view(), name='home')
Включение другого URLconf
1. Импортируйте функцию include(): из django.urls import include, путь
2. Добавьте URL-адрес в urlpatterns: path('blog/', include('blog.urls'))"""
from django.contrib import admin
from django.urls import path
from cashbox_app.views import CustomLoginView, AddressSelectionView, CashReportFormView, ReportSubmittedView, \
    KorolevaView, CountVisitsView, CountVisitsBriefView, CountVisitsFullView, KorolevaCashReportView, CorrectedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('address-selection/', AddressSelectionView.as_view(), name='address_selection'),
    path('cash-report-form/', CashReportFormView.as_view(), name='cash_report_form'),
    path('report-submitted/', ReportSubmittedView.as_view(), name='report_submitted'),
    path('cash-report-form/сorrected/', CorrectedView.as_view(), name='сorrected'),

    path('koroleva/', KorolevaView.as_view(), name='koroleva'),
    path('count_visits/', CountVisitsView.as_view(), name='count_visits'),
    path('count_visits/brief', CountVisitsBriefView.as_view(), name='count_visits_brief'),
    path('count_visits/full', CountVisitsFullView.as_view(), name='count_visits_full'),

    path('cash_report/', KorolevaCashReportView.as_view(), name='coroleva_cash_report'),
]
