import pytest
from django.urls import reverse

from agriceng.area.models import Crop

pytestmark = pytest.mark.django_db


class TestAreaAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:area_crop_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client, default_crop):
        url = reverse("admin:area_crop_changelist")
        response = admin_client.get(url, data={"q": "Tea"})
        assert response.status_code == 200
        assert response.context_data['cl'].result_count > 0

    def test_add(self, admin_client):
        url = reverse("admin:area_crop_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "name": "Coffee",
                "initial_moisture": '65',
                "final_moisture": '16',
                "bulk_density": '800',
            },
        )
        print(response.context)
        assert response.status_code == 302
        assert Crop.objects.filter(name="Coffee").exists()

    def test_view_crop(self, admin_client, default_crop):
        crop = Crop.objects.get(name="Tea")
        url = reverse("admin:area_crop_change", kwargs={"object_id": crop.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
