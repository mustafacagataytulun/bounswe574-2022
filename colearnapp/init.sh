#! /bin/sh

user=admin
email=admin@example.com
password=pass

python3 manage.py migrate
echo "from django.contrib.auth import get_user_model; from django.contrib.auth.models import User; User = get_user_model(); User.objects.create_superuser('$user', '$email', '$password')" | python3 manage.py shell
