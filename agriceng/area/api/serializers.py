from rest_framework import serializers

from agriceng.area.models import Crop


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['name', 'initial_moisture', 'final_moisture', 'bulk_density', ]
