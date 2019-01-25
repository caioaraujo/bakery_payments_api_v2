# Bakery Payments v2.0

New version developed with Django 2.1

## Requirements

- Python 3.6
- PIP
- PostgreSQL

or

- Docker
- Docker compose

Optional:

- Pipenv
- Make

You can install all dependencies and creating a virtualenv with pipenv (https://pipenv.readthedocs.io/en/latest/install/),
running:

`pipenv install`

or

`make pipenv-setup`

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

For tests running, you should install all development dependencies. It can be installed with pipenv by running:

`pipenv install --dev`

or

`make pipenv-setup-dev`

Run all project tests with:

`python manage.py test --settings=bakery_payments_v2.settings.testing`

or

`make test`

## Coverage

For coverage running, you should install all development dependencies. See [Tests section](#Tests).

Run project coverage with:

`coverage run --source='.' manage.py test --settings=bakery_payments_v2.settings.testing`

or

`make coverage`


