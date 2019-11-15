"""
Populates the data base with sample data
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stone_cold_props.settings')
django.setup()

from property_app.models import *
# dictionary with models and their respective csv files
MODELS_TO_FILES = {Tenant: 'tenant.csv', Unit: 'unit.csv', Building: 'building.csv'}

