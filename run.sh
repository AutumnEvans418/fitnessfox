#!/bin/bash
apt-get update
apt-get -y install apache2 apache2-utils apache2-dev
pip install -r requirements.txt

python manage.py runserver