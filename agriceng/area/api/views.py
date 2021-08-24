from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import CropSerializer
from agriceng.area.models import Crop


class CropViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CropSerializer
    queryset = Crop.objects.all()
    lookup_field = "name"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(name=self.request.crop.name)

    @action(detail=False, methods=["GET"])
    def crop(self, request):
        serializer = CropSerializer(request.crop, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
