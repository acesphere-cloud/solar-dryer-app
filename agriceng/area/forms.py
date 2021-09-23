from django import forms
from django.core.validators import MinValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import AppendedText

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
        empty_label="Name of crop:",
        help_text="Determines bulk density, initial and final moisture content",
    )
    location = forms.CharField(
        help_text="Location of Solar Dryer",
        max_length=64,
    )
    mass = forms.FloatField(
        help_text="Initial mass of material to dry in kilograms",
        validators=[MinValueValidator(0.1, message="The mass of crop has to be at least 100 grams (0.1 kg)")]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.field_class = 'mb-4'
        self.helper.layout = Layout(
            'crop',
            Field('location', placeholder="Type in your nearest location:"),
            AppendedText('mass', '㎏', placeholder="Mass of crop to be dried:"),
        )
        self.helper.add_input(Submit('generate-dryer', 'Design Dryer', css_class='btn btn-primary'))


class PDFForm(forms.Form):
    """Form for generating Solar Dryer PDFs"""
    prefix = 'pdf'
    solar_dryer = forms.ModelChoiceField(
        queryset=Dryer.objects.all(),
        empty_label="⛶ Choose preferred Solar Dryer ⛶",
        help_text="To generate PDF report, select your preferred solar dryer from the menu.",
    )
    context = forms.JSONField(
        widget=forms.HiddenInput
    )

    def __init__(self, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if size:
            self.fields['solar_dryer'].queryset = Dryer.objects.filter(size=size)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('generate-pdf', 'Generate PDF Report', css_class='btn btn-primary'))
