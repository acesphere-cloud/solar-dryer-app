import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_weather():
    assert (reverse("weather:location") == f"/weather/")
    assert resolve(f"/weather/").view_name == "weather:location"
