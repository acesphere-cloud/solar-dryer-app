from django.urls import path
from django.contrib.auth.decorators import login_required

from .api.views import weather_view


app_name = "weatherdata"

urlpatterns = [
     path("", view=login_required(weather_view), name="location"),
]
