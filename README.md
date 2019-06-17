# Bakery Payments API v2.0

New version developed with Django 2.2

[![Build Status](https://travis-ci.com/caioaraujo/bakery_payments_api_v2.svg?branch=master)](https://travis-ci.com/caioaraujo/bakery_payments_api_v2)

[![Coverage Status](https://coveralls.io/repos/github/caioaraujo/bakery_payments_api_v2/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/caioaraujo/bakery_payments_api_v2?branch=master)

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

### Coding style tests

This project uses flake8 and pycodestyle checking. Install all development dependencies and execute:

`flake8 & pycodestyle`

or

`make code-convention`

## Coverage

For coverage running, you should install all development dependencies. See [Tests section](#Tests).

Run project coverage with:

`coverage run --source='.' manage.py test --settings=bakery_payments_v2.settings.testing`

or

`make coverage`

## Author

**Caio Araujo** - (https://github.com/caioaraujo)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

