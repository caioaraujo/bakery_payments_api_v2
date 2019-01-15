FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.dev.txt /code/
ADD requirements.txt /code/
RUN pip install -r requirements.dev.txt
ADD . /code/