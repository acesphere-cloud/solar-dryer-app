from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from agriceng.users.api.views import UserViewSet
from agriceng.area.api.views import CropViewSet
from agriceng.solardryers.api.views import DryerViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("crops", CropViewSet)
router.register("dryers", DryerViewSet)

app_name = "api"
urlpatterns = router.urls
