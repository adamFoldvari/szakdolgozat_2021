FROM python:3.7-alpine

# Heroku needs to set the port
ENV PORT 8000

ADD ./requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --update bash libpq postgresql-dev  && \
    apk add --no-cache build-base

RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

ADD ./healthcheck_api /opt/healthcheck_api
WORKDIR /opt

CMD gunicorn --bind 0.0.0.0:$PORT "healthcheck_api:create_app()"
