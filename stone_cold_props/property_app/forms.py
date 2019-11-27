from django import forms
from .models import *
from .search import *


class searchForm(forms.Form):

    type = forms.ChoiceField(choices=[('*', '-'), ('house', 'House'), ('AptBuild', 'Apartment')])
    city = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_city()])
    state = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_state()])
    #address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()]) #this one shouldnt be here but is just for tests
    Minimum_Bedrooms = forms.ChoiceField(choices=[(x, x) for x in range(1,10)])
    Minimum_Bathrooms = forms.ChoiceField(choices=[(x, x) for x in range(1,10)])
    Minimum_SqFt = forms.CharField(max_length=6, initial='50')
    Max_Rent = forms.CharField(max_length=5, initial='1000')


class loginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class expiringContractForm(forms.Form):
    expr = forms.ChoiceField(label='Expring in:',choices=[('1', '1 month'), ('6', '6 months'), ('12', '12 months')])


class tenantSearchForm(forms.Form):

    city = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_city()])
    zip = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_zip()])
    address = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_address()])
    state = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_state()])
    manager = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_manager()])
    owner = forms.ChoiceField(choices=[(x, x) for x in rem_duplicate_owner()])
    unit = forms.CharField(max_length=5, initial='*')
   # address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()]) #this one shouldnt be here but is just for tests