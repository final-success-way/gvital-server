#!/bin/bash
sync () {
  git pull
  systemctl restart gunicorn
  systemctl restart djangoq
}
sync