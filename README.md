# Bakery Payments v2.0

New version developed with Django 2.1

## Requirements

- Python 3.6
- PostgreSQL

For dependencies, see requirements.txt

## API docs

`/docs`

## Running local

`python manage.py runserver`<br>
or<br>
`make runserver`

## Tests

`python manage.py test --settings=bakery_payments_v2.settings.testing`<br>
or<br>
`make test`

## Coverage

`coverage run --source='.' manage.py test --settings=bakery_payments_v2.settings.testing`<br>
or<br>
`make coverage`


