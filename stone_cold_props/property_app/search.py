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

class searchForm(forms.Form):


    type = forms.ChoiceField(choices=[('*', '-'), ('House', 'House'), ('Apartment', 'Apartment')])
    city = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_city()])
    state = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_state()])
    address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()])  #this one shouldnt be here but is just for tests

    #TODO get duplates out of the for look mayeb a UNIQUE method








