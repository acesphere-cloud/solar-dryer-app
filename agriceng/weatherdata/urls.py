from django.urls import path

from .api.views import weather_view
# from agriceng.weatherdata.views import (,)

app_name = "weatherdata"

urlpatterns = [
     path("", view=weather_view, name="location"),
#     path("~update/", view=user_update_view, name="update"),
#     path("<str:username>/", view=user_detail_view, name="detail"),
]
