from django import forms

from .models import *


class searchForm(forms.Form):


    houseType = forms.ChoiceField(choices=[('*', '-'), ('house', 'House'), ('apartment', 'Apartment')])
    city = forms.ChoiceField(choices=[(x.building, x.city) for x in Address.objects.all()])
    state = forms.ChoiceField(choices=[(x.state, x.state) for x in Address.objects.all()])
    address = forms.ChoiceField(choices=[(x.street, x.street) for x in Address.objects.all()])  #this one shouldnt be here but is just for tests

    #TODO get duplates out of the for look mayeb a UNIQUE method






    #houseType2 = forms.ChoiceField(choices=['items',items])


#CHANGE THIS WHEN YOU WANT MORE FORMS