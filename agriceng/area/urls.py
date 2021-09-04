from django.urls import path

from .views import solar_dryer_view, crop_list_view


app_name = "area"

urlpatterns = [
    path("", view=solar_dryer_view, name="solar_dryer"),
    path("~crops/", view=crop_list_view, name="crops"),
]
