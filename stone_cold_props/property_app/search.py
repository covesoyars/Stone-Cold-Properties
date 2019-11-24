from django import forms


class searchForm(forms.Form):
    houseType = forms.ChoiceField(choices=[('*', 'ANY'), ('house', 'House'), ('apartment', 'Apartment')])
    #TODO chamge left hand side of chosies to be some version on enums in out database


#CHANGE THIS WHEN YOU WANT MORE FORMS