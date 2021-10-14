run
    gunicorn image_handler.asgi:application -k uvicorn.workers.UvicornWorker -b :8000
    | python manage.py runserver
    | docker run -p 8000:8000 -it $(docker build -q .)
test
    pytest image_handler/

jwt
    to get
        "api/token/"
    to disable
        set debug=False

