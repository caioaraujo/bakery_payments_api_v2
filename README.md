# Bakery Payments v2.0

New version developed with Django 2.1

## Requirements

- Python 3.6
- PostgreSQL <br>
or <br>
- Docker
- Docker compose

Optional:

- Make

For dependencies, see requirements.txt.

In PostgreSQL, create a database named "bakery" and apply all migrations:

`python manage.py migrate`

## API docs

`/docs`

## Running 

### Local

`python manage.py runserver`<br>
or<br>
`make run-server`

### Docker compose

`docker-compose up --build`

## Tests

`python manage.py test --settings=bakery_payments_v2.settings.testing`<br>
or<br>
`make test`

## Coverage

`coverage run --source='.' manage.py test --settings=bakery_payments_v2.settings.testing`<br>
or<br>
`make coverage`


