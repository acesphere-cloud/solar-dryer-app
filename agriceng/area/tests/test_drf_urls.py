import pytest
from django.urls import resolve, reverse

from agriceng.area.models import Crop, Coefficient

pytestmark = pytest.mark.django_db


def test_crop_detail(crop: Crop):
    assert (
        reverse("api:crop-detail", kwargs={"name": crop.name})
        == f"/api/crops/{crop.name}/"
    )
    assert resolve(f"/api/crops/{crop.name}/").view_name == "api:crop-detail"


def test_crop_list():
    assert reverse("api:crop-list") == "/api/crops/"
    assert resolve("/api/crops/").view_name == "api:crop-list"


