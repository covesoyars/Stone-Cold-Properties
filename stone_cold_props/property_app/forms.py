from django import forms
from .models import *
from .search import rem_duplicate_city, rem_duplicate_state


class searchForm(forms.Form):

    type = forms.ChoiceField(choices=[('*', '-'), ('house', 'House'), ('AptBuild', 'Apartment')])
    city = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_city()])
    state = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_state()])
    address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()]) #this one shouldnt be here but is just for tests
    Minimum_Bedrooms = forms.ChoiceField(choices=[(x, x) for x in range(8)])
    Minimum_Bathrooms = forms.ChoiceField(choices=[(x, x) for x in range(8)])


#TODO add login form here! :P
class loginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
