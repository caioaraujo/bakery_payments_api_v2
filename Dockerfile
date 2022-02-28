FROM python:3.10.2-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext
RUN mkdir -p /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code/
