#!/bin/bash
activate () {
  source ../venv/bin/activate
  pip install -r requirements.txt --no-deps
  python manage.py makemigrations --settings=brf.settings_dev
  python manage.py migrate --settings=brf.settings_dev
  python manage.py runserver --settings=brf.settings_dev 0.0.0.0:8000
}
activate