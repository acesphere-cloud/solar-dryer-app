from django import forms

from .models import Crop, Coefficient

class CropForm(forms.ModelForm):
    """ Form for handling database crop data """

    class Meta:
        model = Crop
        fields = (
            'name',
            'initial_moisture',
            'final_moisture',
            'bulk_density',
        )


class CoefficientForm(forms.ModelForm):
    """ Form for handling database coefficient data """

    class Meta:
        model = Coefficient
        fields = (
            'coefficient',
            'symbol',
            'equivalent',
            'equation',
        )


queryset = Crop.objects.all()


class AreaForm(forms.Form):
    """ Form for handling user input data"""
    crop = forms.ModelChoiceField(
        queryset=queryset,
        empty_label="Name of Crop",
        help_text="Determines bulk density, initial and final moisture content"
    )
    location = forms.CharField(
        max_length=64,
        help_text="Location of the solar dryer"
    )
    mass = forms.FloatField(
        help_text="Initial mass of material to dry in kilograms"
    )

