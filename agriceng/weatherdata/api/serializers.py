from datetime import datetime

from rest_framework import serializers


class Metric:
    def __init__(self, id, name, type, unit=None, created=None):
        self.id = id
        self.name = name
        self.type = type
        self.unit = unit
        self.created = created or datetime.now()


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
        self, id, address, name, index, latitude, longitude, distance, time, tz, currentConditions, alerts, created=None
    ):
        self.id = id
        self.address = address
        self.name = name
        self.index = index
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        self.time = time
        self.timezone = tz
        self.conditions = currentConditions
        self.alerts = alerts
        self.created = created or datetime.now()


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField()
    address = serializers.CharField()
    name = serializers.CharField()
    index = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    distance = serializers.FloatField()
    time = serializers.TimeField()
    tz = serializers.CharField()
    currentConditions = serializers.CharField()
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
        self, wdir, temp, maxt, visibility, wspd, datetimeStr, solarenergy, heatindex, cloudcover, mint, datetime,
        precip, solarradiation, weathertype, snowdepth, sealevelpressure, snow, dew, humidity, precipcover, wgust,
        conditions, windchill, info,
    ):
        self.wdir = wdir
        self.maxt = maxt
        self.temp = temp
        self.visibility = visibility
        self.wspd = wspd
        self.datetimestr = datetimeStr
        self.solarenergy = solarenergy
        self.heatindex = heatindex
        self.cloudcover = cloudcover
        self.mint = mint
        self.datetime = datetime
        self.precip = precip
        self.solarradiation = solarradiation
        self.weathertype = weathertype
        self.snowdepth = snowdepth
        self.sealevelpressure = sealevelpressure
        self.snow = snow
        self.dew = dew
        self.humidity = humidity
        self.precipcover = precipcover
        self.wgust = wgust
        self.conditions = conditions
        self.windchill = windchill
        self.info = info


class WeatherSerializer(serializers.Serializer):
    wdir = serializers.DecimalField(max_digits=5, decimal_places=2)
    cloudcover = serializers.IntegerField()
    mint = serializers.IntegerField()
    datetime = serializers.DateTimeField(format=None)
    precip = serializers.IntegerField()
    solarradiation = serializers.IntegerField()
    dew = serializers.IntegerField()
    humidity = serializers.IntegerField()
    precipcover = serializers.IntegerField()
    info = serializers.CharField()
    temp = serializers.IntegerField()
    maxt = serializers.IntegerField()
    visibility = serializers.IntegerField()
    wspd = serializers.IntegerField()
    solarenergy = serializers.IntegerField()
    heatindex = serializers.IntegerField()
    weathertype = serializers.CharField()
    snowdepth = serializers.IntegerField()
    sealevelpressure = serializers.IntegerField()
    snow = serializers.IntegerField()
    wgust = serializers.IntegerField()
    conditions = serializers.CharField()
    windchill = serializers.IntegerField()

    def create(self, validated_data):
        return Weather(**validated_data)

    def update(self, instance, validated_data):
        instance.wdir = validated_data.get('wdir', instance.wdir)
        instance.temp = validated_data.get('temp', instance.temp)
        instance.maxt = validated_data.get('maxt', instance.maxt)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.wspd = validated_data.get('wspd', instance.wspd)
        instance.datetimestr = validated_data.get('datetimeStr', instance.datetimestr)
        instance.solarenergy = validated_data.get('solarenergy', instance.solarenergy)
        instance.heatindex = validated_data.get('heatindex', instance.heatindex)
        instance.cloudcover = validated_data.get('cloudcover', instance.cloudcover)
        instance.mint = validated_data.get('mint', instance.mint)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.precip = validated_data.get('precip', instance.precip)
        instance.solarradiation = validated_data.get('solarradiation', instance.solarradiation)
        instance.weathertype = validated_data.get('weathertype', instance.weathertype)
        instance.snowdepth = validated_data.get('snowdepth', instance.snowdepth)
        instance.sealevelpressure = validated_data.get('sealevelpressure', instance.sealevelpressure)
        instance.snow = validated_data.get('snow', instance.snow)
        instance.dew = validated_data.get('dew', instance.dew)
        instance.humidity = validated_data.get('humidity', instance.humidity)
        instance.precipcover = validated_data.get('precipcover', instance.precipcover)
        instance.wgust = validated_data.get('wgust', instance.wgust)
        instance.conditions = validated_data.get('conditions', instance.conditions)
        instance.windchill = validated_data.get('windchill', instance.windchill)
        instance.info = validated_data.get('info', instance.info)
        instance.save()
        return instance
