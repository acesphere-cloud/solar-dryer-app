from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from .models import Crop, Coefficient
from agriceng.solardryers.models import Dryer


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
            'units',
            'symbol',
            'equivalent',
            'equation',
        )


queryset = Crop.objects.all()


class AreaForm(forms.Form):
    prefix = 'dryer'
    """ Form for handling user input data"""
    crop = forms.ModelChoiceField(
        queryset=queryset,
        empty_label="Name of Crop",
        help_text="Determines bulk density, initial and final moisture content",
    )
    location = forms.CharField(
        max_length=64,
        help_text="Location of the solar dryer",
    )
    mass = forms.FloatField(
        help_text="Initial mass of material to dry in kilograms",
        validators=[MinValueValidator(0.1, message="The mass of crop has to be at least 100 grams (0.1 kg)")]
    )


dryerset = Dryer.objects.all()


class PDFForm(forms.Form):
    """Form for generating Solar Dryer PDFs"""
    prefix = 'pdf'
    solar_dryer = forms.ModelChoiceField(
        queryset=dryerset,
        empty_label=">>Preferred Solar Dryer<<",
        help_text="To generate PDF report, select your preferred solar dryer.",
    )
    context = forms.JSONField(
        widget=forms.HiddenInput
    )

    def clean_solar_dryer(self):
        data = self.cleaned_data['solar_dryer']
        if not data:
            raise ValidationError('Select preferred solar dryer from the menu')
        return data


