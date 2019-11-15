"""
WSGI config for stone_cold_props project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stone_cold_props.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stone_cold_props.settings")

os.environ['DJANGO_SETTINGS_MODULE'] = 'stone_cold_props.settings'

application = get_wsgi_application()
