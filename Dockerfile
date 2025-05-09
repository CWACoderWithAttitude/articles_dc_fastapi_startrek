
FROM python:3.12-slim


WORKDIR /code


COPY ./requirements.in /code/requirements.in


RUN pip install --no-cache-dir --upgrade -r /code/requirements.in

COPY main.py .
COPY ship_model.py .
COPY settings.py .
ADD ./routers /code/routers

#COPY ./app /code/app


CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "8001"]
#CMD ["bash", "-c", "ls -ltr"]