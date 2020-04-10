FROM python:3.8-alpine

RUN apk update

RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev \
            git \
            openssh-client

RUN apk add --no-cache pcre
RUN apk add --no-cache gcc musl-dev

RUN adduser --disabled-password --gecos '' python

WORKDIR /app
COPY . /app
COPY ./requirements/requirements.txt /app/requirements.txt

RUN chown -R python /app
RUN su python -c 'python -m venv ~/.env'
RUN su python -c 'source ~/.env/bin/activate  && pip install -r /app/requirements.txt'

RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

USER python

EXPOSE 5000
CMD . ~/.env/bin/activate && uwsgi --ini /app/wsgi.ini
