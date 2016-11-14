ENV=./env/bin
SHELL := /bin/bash
PYTHON=$(ENV)/python
PIP=$(ENV)/pip
MANAGE=$(PYTHON) manage.py

migrate:
	$(MANAGE) migrate

make-migrations:
	$(MANAGE) makemigrations

superuser:
	$(MANAGE) createsuperuser

collect-static:
	mkdir -p static
	$(MANAGE) collectstatic --no-input

development:
	$(PIP) install -r requirements/development.txt --upgrade

staging:
	$(PIP) install -r requirements/staging.txt --upgrade

production:
	$(PIP) install -r requirements/production.txt --upgrade

env:
	virtualenv -p `which python3` env

delete-env:
	rm -rf ./env

run:
	$(MANAGE) runserver 0.0.0.0:8000
