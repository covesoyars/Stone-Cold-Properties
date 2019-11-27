from django import forms
from .models import *

def rem_duplicate_city():
    w = Address.objects.all()
    c = ['*']
    for x in w:
        if x.city not in c:
            c.append(x.city)
    return c

def rem_duplicate_state():
    w = Address.objects.all()
    c = ['*']
    for x in w:
        if x.state not in c:
            c.append(x.state)
    return c
def rem_duplicate_zip():
    w = Address.objects.all()
    c = ['*']
    for x in w:
        if x.zip not in c:
            c.append(x.zip)
    return c

def rem_duplicate_address():
    w = Address.objects.all()
    c = ['*']
    for x in w:
        if x.street not in c:
            c.append(x.street)
    return c

def rem_duplicate_manager():
    w = PropertyManager.objects.all()
    c = ['*']
    for x in w:
        if x.first_name + " "+ x.last_name not in c:
            c.append(x.first_name + " "+ x.last_name)
    return c

def rem_duplicate_owner():
    w = Client.objects.all()
    c = ['*']
    for x in w:
        if x.first_name + " "+ x.last_name not in c:
            c.append(x.first_name + " "+ x.last_name)
    return c