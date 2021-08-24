import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_solar_dryer():
    assert (reverse("solardryer:dryers") == f"/dryers/~dryers/")
    assert resolve(f"/dryers/~dryers/").view_name == "solardryer:dryers"
