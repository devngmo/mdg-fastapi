FROM python:3.9

WORKDIR /code

COPY ./requiements.txt /code/requiements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requiements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "host", "localhost", "--port", "8000"]