import pytest
from django.test import RequestFactory

from agriceng.area.api.views import CropViewSet
from agriceng.area.models import Crop

pytestmark = pytest.mark.django_db


class TestCropViewSet:
    def test_get_queryset(self, crop: Crop, rf: RequestFactory):
        view = CropViewSet()
        request = rf.get("/fake-url/")
        request.crop = crop

        view.request = request

        assert crop in view.get_queryset()

    def test_crop(self, crop: Crop, rf: RequestFactory):
        view = CropViewSet()
        request = rf.get("/fake-url/")
        request.crop = crop

        view.request = request

        response = view.crop(request)

        assert response.data == {
            "name": crop.name,
            "initial_moisture": crop.initial_moisture,
            "final_moisture": crop.final_moisture,
            "bulk_density": crop.bulk_density,
        }
