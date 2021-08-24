from django import forms


class LocationForm(forms.Form):
    """ Form for handling location weather search """
    location = forms.CharField()
