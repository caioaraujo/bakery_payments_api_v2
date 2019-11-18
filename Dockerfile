FROM python:3.8.0-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext
RUN mkdir -p /code
WORKDIR /code

ADD Pipfile /code/
ADD Pipfile.lock /code/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

ADD . /code/
