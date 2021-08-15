from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework import ISO_8601
from rest_framework.settings import api_settings

class Metric:
    def __init__(self, id, name, type, unit=None, created=None):
        self.id = id
        self.name = name
        self.type = type
        self.unit = unit
        self.created = created or timezone.now()


class MetricSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.IntegerField()
    unit = serializers.CharField()
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Metric(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


class Location:
    def __init__(
        self, id, address, name, index, latitude, longitude, distance, time, tz, conditions, alerts, created=None
    ):
        self.id = id
        self.address = address
        self.name = name
        self.index = index
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        self.time = time
        self.tz = tz
        self.conditions = conditions
        self.alerts = alerts
        self.created = created or timezone.now()


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField()
    address = serializers.CharField()
    name = serializers.CharField()
    index = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    distance = serializers.FloatField()
    time = serializers.FloatField()
    tz = serializers.CharField()
    conditions = serializers.CharField()
    alerts = serializers.CharField()
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Location(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.address = validated_data.get('address', instance.address)
        instance.name = validated_data.get('name', instance.name)
        instance.index = validated_data.get('index', instance.index)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.time = validated_data.get('time', instance.time)
        instance.timezone = validated_data.get('tz', instance.timezone)
        instance.conditions = validated_data.get('currentConditions', instance.conditions)
        instance.alerts = validated_data.get('alerts', instance.alerts)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


class Weather:
    def __init__(
        self, temp, wspd, info, location, datetime,
    ):
        self.temp = temp
        self.wspd = wspd
        self.info = info
        self.location = location
        self.datetime = datetime


class TimestampField(serializers.DateTimeField):

    def to_representation(self, value):
        if not value:
            return None

        value = datetime.fromtimestamp(value/1000)

        output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

        if output_format is None or isinstance(value, str):
            return value

        value = self.enforce_timezone(value)

        if output_format.lower() == ISO_8601:
            value = value.isoformat()
            if value.endswith('+00:00'):
                value = value[:-6] + 'Z'
            return value
        return value.strftime(output_format)


class WeatherSerializer(serializers.Serializer):
    datetime = TimestampField(format='%Y-%m-%d')
    temp = serializers.DecimalField(max_digits=3, decimal_places=1)
    wspd = serializers.DecimalField(max_digits=4, decimal_places=1)
    info = serializers.CharField()
    location = LocationSerializer()

    def create(self, validated_data):
        return Weather(**validated_data)

    def update(self, instance, validated_data):
        instance.temp = validated_data.get('temp', instance.temp)
        instance.wspd = validated_data.get('wspd', instance.wspd)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.info = validated_data.get('info', instance.info)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance


class Query:
    def __init__(self, location='', created=None):
        self.location = location
        self.created = created or timezone.now()


class QuerySerializer(serializers.Serializer):
    location = serializers.CharField(max_length=128, style={'placeholder': 'Enter location to fetch weather data',
                                                            'hide_label': True})
    created = serializers.DateTimeField(default=None, style={'input_type': 'hidden', 'hide_label': True})

    def create(self, validated_data):
        return Query(**validated_data)

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
