# CashBox Management System

***— это веб-приложение, созданное с использованием Django, предназначенное для управления
операциями кассового аппарата для различных видов деятельности, таких как скупка, ломбард и техническое обслуживание.
Эта система предоставляет комплексную платформу для отслеживания финансовых транзакций, управления остатками наличности
и ведения точных записей.***

### Основной функционал.

* Авторизация пользователей.
* Выбор адреса для регистрации кассовых операций в разных странах.
* Форма регистрации изменений в балансах касс.
* Оперативное отслеживание балансов кассы.
* Проверка данных и обработка ошибок.
* Пользовательский интерфейс для удобной навигации и ввода данных.

### Структура проекта

Проект состоит из нескольких представлений Django и форм:

1. Пользовательский вид входа (CustomLoginView):
    - Осуществление авторизации пользователей с использованием пользовательской формы аутентификации.
    - Перенаправляет после получения валидной информации на выбранный адрес.

2. Вид выбора адреса (AddressSelectionView):
    - Выберите адрес для операций регистрации кассы

3. Форма отчета по кассе (CashReportFormView):
    - Предоставляет форму для ввода данных регистрации кассы.
    - Отключить режим поля для предотвращения редактирования чувствительной информации.
    - Получает текущие балансы для каждого типа регистрационных касс.

4. Результат (ReportSubmittedView):
    - Отображает результаты изменений, внесенных в отчет о кассовых операциях.
    - Показывает обновленную информацию балансов касс.

### Технические

+ Использует систему аутентификации Django (django.contrib.auth)
+ Реализовать пользовательские формы для аутентификации и выбора адреса.
+ Применяет представление Django (FormView) для обработки форм данных
+ Использует ORM Django для запросов к базе данных и операциям
+ Реализует управление сессиями для хранения выбранных адресов
+ Использует функцию временных зон Django для формирования даты.

### Лучшая практика

+ Разделение ответственности: каждое производство обрабатывает конкретную часть рабочего процесса.
+ Использование встроенных миксов и утилит Django (например, LoginRequiredMixin)
+ Правильная обработка ошибок и проверка валидации при обработке форм
+ Эффективные запросы с использованием ORM Django для получения недавних данных, отчетов о регистрации кассы.
+ Реализованы меры безопасности через систему аутентификации Django
+ Этот проект обеспечивает надежную поддержку для управления операциями регистрации касс в безопасном и эффективном
  режиме, подходящем для бизнеса, работающем с несколькими регистрациями касс в разных местах.