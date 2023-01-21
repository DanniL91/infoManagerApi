FROM python:3.8.2-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir code

COPY . /code/

WORKDIR /code

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install -r requeriments.txt

RUN mkdir static

#EXPOSE 8000

#RUN ["chmod", "+x", "/code/Scripts/entrypoint.sh"]
#ENTRYPOINT ["/code/Scripts/entrypoint.sh"]
RUN pip install gunicorn


CMD exec gunicorn --bind :$PORT --workers 3 --threads 8 --timeout 120 infoManagerAPI.wsgi
#CMD ["gunicorn","--bind", "127.0.0.1:8080", "infoManagerAPI.wsgi"]