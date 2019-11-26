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
