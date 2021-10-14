python manage.py createsuperuser --noinput
python manage.py makemigrations image_handler
python manage.py migrate image_handler
python manage.py collectstatic
