from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import DryerSerializer
from agriceng.solardryers.models import Dryer


class DryerViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = DryerSerializer
    queryset = Dryer.objects.all()
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.dryer.id)

    @action(detail=False, methods=["GET"])
    def dry(self, request):
        serializer = DryerSerializer(request.dryer, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
