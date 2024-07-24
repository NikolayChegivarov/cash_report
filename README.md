
Ресурс предназначен для кассовой отчетности. 

Устанавливаем зависимости c помощью requirements.txt или через pip:  

pip install django  # ?
pip install djangorestframework
pip install psycopg2-binary
pip install python-dotenv  # переменные окружения

python manage.py makemigrations  # создать инструкции для изменения в бд.
python manage.py migrate  # применить инструкции.

python manage.py runserver  # запустить сервер