#!/bin/bash
activate () {
  sudo cp gunicorn.socket /etc/systemd/system/gunicorn.socket
  sudo cp gunicorn.service /etc/systemd/system/gunicorn.service
  sudo systemctl start gunicorn.socket
  sudo systemctl enable gunicorn.socket
  sudo systemctl daemon-reload
  sudo systemctl restart gunicorn

  sudo cp djangoq.socket /etc/systemd/system/djangoq.socket
  sudo cp djangoq.service /etc/systemd/system/djangoq.service
  sudo systemctl start djangoq.socket
  sudo systemctl enable djangoq.socket
  sudo systemctl daemon-reload
  sudo systemctl restart djangoq
}
activate