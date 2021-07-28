from django import forms


class LocationForm(forms.Form):
    """ Form for handling location weather search """
    location = forms.CharField(empty_label="Location for weather data. Multiple locations separated by pipe (|)")
