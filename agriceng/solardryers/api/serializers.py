from rest_framework import serializers

from agriceng.solardryers.models import Dryer


class SizeField(serializers.RelatedField):
    queryset = Dryer.objects.all()

    def to_representation(self, value):
        size = Dryer.SIZE_CHOICES[0][1] if value == Dryer.SMALL else Dryer.SIZE_CHOICES[1][1]
        return size


class VersionField(serializers.RelatedField):
    queryset = Dryer.objects.all()

    def to_representation(self, value):
        size = Dryer.VERSION_CHOICES[0][1] if value == Dryer.SIMPLE else Dryer.VERSION_CHOICES[1][1]
        return size


class DryerSerializer(serializers.ModelSerializer):
    size = SizeField()
    version = VersionField()
    class Meta:
        model = Dryer
        fields = ['size', 'version', 'diagram', 'construct', 'variation', ]
