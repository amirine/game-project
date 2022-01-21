#FROM python:3.9-alpine
#
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1
#
#RUN pip install --upgrade pip
#COPY ./requirements.txt /requirements.txt
#RUN apk add --update --no-cache postgresql-client jpeg-dev
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#    gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
#RUN pip install -r /requirements.txt
#RUN apk del .tmp-build-deps
#
#RUN mkdir /game_project
#COPY ./game_project /game_project
#WORKDIR /game_project

# pull the official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

#EXPOSE 8000

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

