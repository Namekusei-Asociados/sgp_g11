"""
WSGI config for sgp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see

https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
    - El wsgi a ser utilizado por el grupo 11 es Gunicorn"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgp.settings')

application = get_wsgi_application()
