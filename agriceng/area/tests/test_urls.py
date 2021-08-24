import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_solar_dryer():
    assert (reverse("area:solar_dryer") == f"/area/")
    assert resolve(f"/area/").view_name == "area:solar_dryer"
