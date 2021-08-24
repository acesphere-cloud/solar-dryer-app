"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _

from agriceng.area.forms import CropForm, CoefficientForm, AreaForm
from agriceng.area.models import Crop, Coefficient

pytestmark = pytest.mark.django_db

querysets = Coefficient.objects.all()

class TestCropForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_crop_form_validation_error_msg(self, crop: Crop):
        """
        Tests Crop Form's unique validator functions correctly by testing:
            1) A new crop with an existing crop name cannot be added.
            2) Only 1 error is raised by the CropForm Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = CropForm(
            {
                "name": crop.name,
                "initial_moisture": crop.initial_moisture,
                "final_moisture": crop.final_moisture,
                "bulk_density": crop.bulk_density,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "name" in form.errors
        assert form.errors["name"][0] == _("Crop with this Name already exists.")

    def test_equivalent_field_output_type(self):
        """
        Tests CoefficientForm Form's type validator functions correctly by testing:
            1) A new crop with a non-float equivalent value cannot be added.
            2) Only 1 error is raised by the CoefficientForm Form
            3) The desired error message is raised
        """
        # The equivalent value entry is a non-float type,
        # hence cannot be created.
        form = CoefficientForm(
            {
                "coefficient": 'dryer coefficient',
                "symbol": 'C02',
                "equivalent": 'string-value',
                "equation": 'airflow',
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "equivalent" in form.errors
        assert form.errors["equivalent"][0] == _("Enter a number.")

    def test_coefficent_form_unique_constraint(self, coefficient: Coefficient):
        """
        Tests CoefficientForm Form's unique constraint functions correctly by testing:
            1) A new coefficient with an existing coefficient and equation cannot be added.
            2) Only 1 error is raised by the CropForm Form
            3) The desired error message is raised
        """
        # A Coefficient object with similar a coefficient value and equation value exists,
        # hence cannot be created.
        form = CoefficientForm(
            {
                "coefficient": coefficient.coefficient,
                "symbol": coefficient.symbol,
                "equivalent": coefficient.equivalent,
                "equation": coefficient.equation,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "__all__" in form.errors
        assert form.errors["__all__"][0] == _("Coefficient with this Coefficient and Equation already exists.")

    def test_area_form_accepted_crop(self):
        """
        Tests AreaForm Form's crop field functions correctly by testing:
            1) A crop that does not exist among the available choices is not added.
            2) Only 1 error is raised by the CropForm Form
            3) The desired error message is raised
        """
        # A Coefficient object with similar a coefficient value and equation value exists,
        # hence cannot be created.
        form = AreaForm(
            {
                "dryer-crop": 'Dates',
                "dryer-location": 'Atlanta, GA',
                "dryer-mass": '9999999999',
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "crop" in form.errors
        assert form.errors["crop"][0] == _("Select a valid choice. That choice is not one of the available choices.")

    def test_mass_field_minimum_value(self, crop: Crop):
        """
        Tests AreaForm Form's mass field functions correctly by testing:
            1) A mass value below 0.1 kilograms is not accepted.
            2) Only 1 error is raised by the CropForm Form
            3) The desired error message is raised
        """
        # A Coefficient object with similar a coefficient value and equation value exists,
        # hence cannot be created.
        form = AreaForm(
            {
                "dryer-crop": crop,
                "dryer-location": 'Kitale, Trans Nzoia',
                "dryer-mass": '-1',
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "mass" in form.errors
        assert form.errors["mass"][0] == _("The mass of crop has to be at least 100 grams (0.1 kg)")

    def test_mass_field_minimum_value(self, crop: Crop):
        """
        Tests AreaForm Form's mass field functions correctly by testing:
            1) A mass value below 0.1 kilograms is not accepted.
            2) Only 1 error is raised by the CropForm Form
            3) The desired error message is raised
        """
        # A Coefficient object with similar a coefficient value and equation value exists,
        # hence cannot be created.
        form = AreaForm(
            {
                "dryer-crop": crop,
                "dryer-location": 'Kitale, Trans Nzoia',
                "dryer-mass": '-1',
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "mass" in form.errors
        assert form.errors["mass"][0] == _("The mass of crop has to be at least 100 grams (0.1 kg)")


