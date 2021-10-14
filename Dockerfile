FROM python:3.9-slim-buster

COPY . .
WORKDIR /image_handler
RUN pip install -r requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "image_handler.asgi:application", "-k", "uvicorn.workers.UvicornWorker","-b",":8000"]

# todo: use poetry
# todo: use good build https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# todo: compose/postgres/volumes