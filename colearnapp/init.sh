#! /bin/sh

user=admin
email=admin@example.com
password=pass

python3 manage.py migrate

python3 manage.py collectstatic
