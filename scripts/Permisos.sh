#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python3 manage.py loaddata permissions
python3 manage.py loaddata permissionsProj
python3 manage.py loaddata default_roles_system
