FROM python:3.7-alpine

# Heroku needs to set the port
ENV PORT 8000

RUN apk add --no-cache --update bash

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

ADD ./healthcheck_api /opt/healthcheck_api
WORKDIR /opt

CMD gunicorn --bind 0.0.0.0:$PORT "healthcheck_api:create_app()"
