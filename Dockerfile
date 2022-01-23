FROM python:3.9-alpine

WORKDIR ./usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip3 install -r requirements.txt

COPY . /usr/src/app
