#!/bin/bash
activate () {
  source ../venv/bin/activate
  pip install -r requirements.txt --no-deps
  python manage.py makemigrations --settings=brf.settings_prod
  python manage.py migrate --settings=brf.settings_prod
  sudo systemctl daemon-reload
  sudo systemctl restart gunicorn
}
activate