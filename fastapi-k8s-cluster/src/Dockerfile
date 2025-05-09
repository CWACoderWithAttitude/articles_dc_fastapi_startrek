FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.in /code/requirements.in

RUN pip install --no-cache-dir --upgrade -r /code/requirements.in

COPY main.py .
COPY ship_model.py .
COPY settings.py .
ADD ./routers /code/routers

CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "8001"]