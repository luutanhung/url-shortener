FROM python:3.13-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./wait-for-it.sh /code/wait-for-it.sh
COPY ./app /code/app

CMD ["./wait-for-it.sh", "mongodb:27017", "-t", "60", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
