import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework import status

from agriceng.weatherdata.weather import query_nairobi_weather
from .serializers import MetricSerializer, WeatherSerializer, Metric, Weather


class WeatherView(APIView):
    template_name = 'pages/weather.html'
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        weather_data = query_nairobi_weather()
        weather_metrics = []
        for metric, details in weather_data['columns'].items():
            metric = Metric(id=details['id'], name=details['name'], type=details['type'], unit=details['unit'])
            weather_metrics.append(metric)
        weather_values = []
        for location, weather in weather_data['locations'].items():
            columns = weather['values'][0].keys()
            print(columns)
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
                    datetimeStr=measure['datetimeStr'],
                )
                weather_values.append(weather_value)
        weather_values = WeatherSerializer(data=weather_values, many=True)
        weather_values.is_valid()
        weather_values.save()
        weather_metrics = MetricSerializer(data=weather_metrics, many=True)
        weather_metrics.is_valid()
        weather_metrics.save()
        return Response({
            'weather_metrics': weather_metrics.data,
            'weather_values': weather_values.data,
            'columns': columns,
        }, status=status.HTTP_200_OK)

weather_view = WeatherView.as_view()
