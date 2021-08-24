import pytest
from django.test import RequestFactory

from agriceng.solardryers.api.views import DryerViewSet
from agriceng.solardryers.models import Dryer

pytestmark = pytest.mark.django_db


class TestDryerViewSet:
    def test_get_queryset(self, dryer: Dryer, rf: RequestFactory):
        view = DryerViewSet()
        request = rf.get("/fake-url/")
        request.dryer = dryer

        view.request = request

        assert dryer in view.get_queryset()

    def test_dry(self, dryer: Dryer, rf: RequestFactory):
        """
            Ensure we can create a new GameCategory and then retrieve it
        """
        view = DryerViewSet()
        request = rf.get("/fake-url/")
        request.dryer = dryer

        view.request = request

        response = view.dry(request)
        assert response.status_code == 200
