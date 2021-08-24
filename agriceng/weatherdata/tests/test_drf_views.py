import pytest
from django.test import RequestFactory

from agriceng.weatherdata.api.views import WeatherView


pytestmark = pytest.mark.django_db


class TestWeatherView:

    def test_get(self, rf: RequestFactory):
        """
        Confirm whether a get request is successful and the correct template is used
        """
        view = WeatherView()
        request = rf.get("/fake-url/")
        response = view.get(self, request)

        assert response.status_code == 200
        assert response.status_text == 'OK'

    def test_post(self, rf: RequestFactory,):
        """
        Assert whether a post request is successful
        """
        view = WeatherView()
        request = rf.get("/fake-url/")
        request.data = {"location": 'Tropez'}

        response = view.post(request=request)

        assert response.status_code == 201
        assert response.status_text == 'Created'
