"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _

from agriceng.weatherdata.forms import LocationForm

pytestmark = pytest.mark.django_db


class TestLocationForm:
    """
    Test class for all tests related to the LocationForm
    """

    def test_location_field_required(self):
        """
        Test form validation for Location field required value
        """

        # The user already exists,
        # hence cannot be created.
        form = LocationForm({"location": ''})
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "location" in form.errors
        assert form.errors["location"][0] == _("This field is required.")
