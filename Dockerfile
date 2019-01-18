FROM python:3.6.8
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
ADD requirements.dev.txt /code/
ADD requirements.txt /code/
ADD docker-entrypoint.sh /code/
RUN pip install -r requirements.dev.txt
ADD . /code/
