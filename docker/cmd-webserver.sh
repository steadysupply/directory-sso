#!/bin/bash -xe

python manage.py createsuperuserwithpsswd --no-input --email=$ADMIN_EMAIL --password=$ADMIN_PASSWORD
