FROM python:3.8-alpine

ENV prometheus_multiproc_dir /tmp/prometheus

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

# Creates SSH folder
RUN su python -c 'mkdir -p ~/.ssh'
RUN su python -c 'chmod 0700 ~/.ssh'
RUN su python -c 'ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts'

COPY id_rsa /home/python/.ssh/id_rsa
RUN chown python:python /home/python/.ssh/id_rsa
RUN chmod 400 /home/python/.ssh/id_rsa
RUN eval $(ssh-agent) && ssh-add /home/python/.ssh/id_rsa && ssh-add -l


WORKDIR /app
COPY . /app
COPY ./requirements/requirements.txt /app/requirements.txt

RUN chown -R python /app
RUN su python -c 'python -m venv ~/.env'
RUN su python -c 'source ~/.env/bin/activate  && pip install -r /app/requirements.txt'

RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

USER python

RUN mkdir /tmp/prometheus

RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

EXPOSE 5000
CMD . ~/.env/bin/activate && uwsgi --ini /app/wsgi.ini
