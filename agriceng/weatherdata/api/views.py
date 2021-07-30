from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from rest_framework import status

from .viewmixins import LocationWeatherMixin
from .serializers import MetricSerializer, WeatherSerializer, Metric, Weather, Location, LocationSerializer, \
    QuerySerializer


class WeatherView(LocationWeatherMixin, APIView):
    template_name = 'pages/weather.html'
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query = QuerySerializer()
        location = LocationSerializer()
        weather_metrics = MetricSerializer()
        weather_values = WeatherSerializer()
        columns = []
        return Response({
            'location': location,
            'weather_metrics': weather_metrics,
            'weather_values': weather_values,
            'columns': columns,
            'query': query,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        query = QuerySerializer(data=request.data)
        print(request.data)
        weather_metrics = []
        weather_values = []
        columns = []
        location = []
        if not query.is_valid():
            return Response({
                'location': location,
                'weather_metrics': weather_metrics,
                'weather_values': weather_values,
                'columns': columns,
                'query': query,
            }, status=status.HTTP_400_BAD_REQUEST)
        location = query.data['location']
        weather_data = self.query_location_weather(location)
        print(weather_data)
        for metric, details in weather_data['columns'].items():
            metric = Metric(id=details['id'], name=details['name'], type=details['type'], unit=details['unit'])
            weather_metrics.append(metric)
        for location, weather in weather_data['locations'].items():
            print(weather)
            location = Location(id=weather['id'], address=weather['address'], name=weather['name'],
                                index=weather['index'], latitude=weather['latitude'], longitude=weather['longitude'],
                                distance=weather['distance'], time=weather['time'], tz=weather['tz'],
                                conditions=weather['currentConditions'], alerts=weather['alerts'],)
            location = LocationSerializer(location)
            print(location.data)
            columns = weather['values'][0].keys()
            for measure in weather['values']:
                weather_value = Weather(
                    wdir=measure['wdir'], cloudcover=measure['cloudcover'], mint=measure['mint'],
                    datetime=measure['datetime'], precip=measure['precip'], solarradiation=measure['solarradiation'],
                    dew=measure['dew'], humidity=measure['humidity'], precipcover=measure['precipcover'],
                    info=measure['info'], temp=measure['temp'], maxt=measure['maxt'], visibility=measure['visibility'],
                    wspd=measure['wspd'], solarenergy=measure['solarenergy'], heatindex=measure['heatindex'],
                    weathertype=measure['weathertype'], snowdepth=measure['snowdepth'],
                    sealevelpressure=measure['sealevelpressure'], snow=measure['snow'], wgust=measure['wgust'],
                    conditions=measure['conditions'], windchill=measure['windchill'],
                    datetimestr=measure['datetimeStr'] or None,
                )
                weather_values.append(weather_value)
        weather_values = WeatherSerializer(data=weather_values, many=True)
        weather_values.is_valid()
        weather_values.save()
        weather_metrics = MetricSerializer(data=weather_metrics, many=True)
        weather_metrics.is_valid()
        weather_metrics.save()
        return Response({
            'location': location.data,
            'weather_metrics': weather_metrics.data,
            'weather_values': weather_values.data,
            'columns': columns,
            'query': query,
        }, status=status.HTTP_201_CREATED)


weather_view = WeatherView.as_view()
