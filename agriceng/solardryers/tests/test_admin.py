from io import BytesIO
import pytest
from django.urls import reverse

from agriceng.solardryers.models import Dryer, Note

pytestmark = pytest.mark.django_db


class TestDryerAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:solardryers_dryer_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_get(self, admin_client, dryer: Dryer):
        url = reverse("admin:solardryers_dryer_add")
        response = admin_client.get(url)
        assert response.status_code == 200
        assert Dryer.objects.filter(version=dryer.version).exists()

    def test_view_dryer(self, admin_client, dryer: Dryer):
        url = reverse("admin:solardryers_dryer_change", kwargs={"object_id": dryer.pk})
        response = admin_client.get(url)
        assert response.status_code == 200


class TestNoteAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:solardryers_note_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client, default_note):
        url = reverse("admin:solardryers_note_changelist")
        response = admin_client.get(url, data={"q": "SM"})
        assert response.status_code == 200

    def test_get(self, admin_client, dryer: Dryer):
        url = reverse("admin:solardryers_note_add")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_view_note(self, admin_client, default_note: Note):
        note = Note.objects.get(note__contains='The quick brown dog')
        url = reverse("admin:solardryers_note_change", kwargs={"object_id": note.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
