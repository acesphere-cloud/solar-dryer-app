from django.urls import path

from .views import solar_dryer_view


app_name = "area"

urlpatterns = [
    path("", view=solar_dryer_view, name="solar_dryer"),
    #path("<str:username>/", view=user_detail_view, name="detail"),
]
