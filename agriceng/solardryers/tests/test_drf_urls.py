import pytest
from django.urls import resolve, reverse

from agriceng.solardryers.models import Dryer

pytestmark = pytest.mark.django_db


def test_crop_detail(dryer: Dryer):
    assert (
        reverse("api:dryer-detail", kwargs={"pk": dryer.pk})
        == f"/api/dryers/{dryer.pk}/"
    )
    assert resolve(f"/api/dryers/{dryer.pk}/").view_name == "api:dryer-detail"


def test_crop_list():
    assert reverse("api:dryer-list") == "/api/dryers/"
    assert resolve("/api/dryers/").view_name == "api:dryer-list"


