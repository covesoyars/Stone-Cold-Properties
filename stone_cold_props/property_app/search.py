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

    type = forms.ChoiceField(choices=[('*', '-'), ('house', 'House'), ('AptBuild', 'Apartment')])
    city = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_city()])
    state = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_state()])
    address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()]) #this one shouldnt be here but is just for tests
    Minimum_Bedrooms = forms.ChoiceField(choices=[(x, x) for x in range(8)])
    Minimum_Bathrooms = forms.ChoiceField(choices=[(x, x) for x in range(8)])


class resultForm(forms.Form):
    def __init__(self, queryset):
        super(resultForm, self).__init__()
        self.query = queryset

        for result in self.query:
            street = forms.CharField(disabled=True, initial=str(result.street))
            city = forms.CharField(disabled=True, initial=str(result.city))
            state  = forms.CharField(disabled=True, initial=str(result.state))
            zipcode = forms.CharField(disabled=True, initial=str(result.zip))














