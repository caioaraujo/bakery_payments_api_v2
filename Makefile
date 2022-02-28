install-dependencies:
	pip install -r requirements.txt

install-dependencies-dev:
	pip install -r requirements-dev.txt

run-server:
	python manage.py runserver

test:
	python -Wa manage.py test --settings=bakery_payments_v2.settings.testing

coverage:
	coverage run --source='.' manage.py test --settings=bakery_payments_v2.settings.testing
	coverage report

coverage-erase:
	coverage erase

code-convention:
	flake8
	pycodestyle

collect-static:
	python manage.py collectstatic

make-messages:
	python manage.py makemessages -l pt_BR

compile-messages:
	python manage.py compilemessages

make-migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down
	docker system prune --force
