FROM python:3.13-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./wait-for-it.sh /code/wait-for-it.sh
COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
