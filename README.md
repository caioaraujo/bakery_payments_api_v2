# Bakery Payments API v2.0

New version developed with Django 4.0

[![Build Status](https://github.com/caioaraujo/bakery_payments_api_v2/actions/workflows/main.yml/badge.svg)](https://github.com/caioaraujo/bakery_payments_api_v2/actions)

[![Coverage Status](https://coveralls.io/repos/github/caioaraujo/bakery_payments_api_v2/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/caioaraujo/bakery_payments_api_v2?branch=master)

## Requirements

- Python 3.10.2
- PostgreSQL

or

- Docker
- Docker compose

Optional:

- Make

You can create and activate a virtual environment by running:

- `python -m venv <path-to-venv>/bakery-payments-api`
- to activate on Linux and Mac: `source <venv>/bin/activate`
- to activate on Windows: `<venv>\Scripts\activate.bat`

And then install the dependencies:

`pip install -r requirements.txt`

or

`make install-dependencies`

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

For tests running, you should install all development dependencies by running:

`pip install -r requirements-dev.txt`

or

`make install-dependencies-dev`

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

