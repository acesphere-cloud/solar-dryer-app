import requests
from requests.exceptions import HTTPError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from rest_framework import status

from agriceng.weatherdata.viewmixins import LocationWeatherMixin
from .serializers import MetricSerializer, WeatherSerializer, Metric, Weather, Location, LocationSerializer, \
    QuerySerializer


class WeatherView(APIView):
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
        weather_metrics = []
        weather_values = []
        columns = []
        location = []
        messages = []
        if not query.is_valid():
            return Response({
                'location': location,
                'weather_metrics': weather_metrics,
                'weather_values': weather_values,
                'columns': columns,
                'query': query,
            }, status=status.HTTP_400_BAD_REQUEST)
        location = query.data['location']
        url = LocationWeatherMixin.get_weather_url(self, location)
        try:
            response = requests.get(url)
            print(' - Running query URL: ', url)
            # A successful request will raise no error
            response.raise_for_status()
        except HTTPError as http_err:
            response = "HTTP error occurred: {}"
            messages.append(response.format(http_err))
            return Response({
                'location': location,
                'weather_metrics': weather_metrics,
                'weather_values': weather_values,
                'columns': columns,
                'query': query,
                'messages': messages
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            response = "An error occurred: {}"
            messages.append(response.format(err))
            return Response({
                'location': location,
                'weather_metrics': weather_metrics,
                'weather_values': weather_values,
                'columns': columns,
                'query': query,
                'messages': messages
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            weather_data = response.json()
            if 'errorCode' in weather_data:
                response = "API Error {0}: {1}"
                messages.append(response.format(weather_data['errorCode'], weather_data['message']))
                return Response({
                    'location': location,
                    'weather_metrics': weather_metrics,
                    'weather_values': weather_values,
                    'columns': columns,
                    'query': query,
                    'messages': messages
                }, status=status.HTTP_400_BAD_REQUEST)
            for metric, details in weather_data['columns'].items():
                metric = Metric(id=details['id'], name=details['name'], type=details['type'], unit=details['unit'])
                weather_metrics.append(metric)
            for location, weather in weather_data['locations'].items():
                location = Location(id=weather['id'], address=weather['address'], name=weather['name'],
                                    index=weather['index'], latitude=weather['latitude'],
                                    longitude=weather['longitude'],
                                    distance=weather['distance'], time=weather['time'], tz=weather['tz'],
                                    conditions=weather['currentConditions'], alerts=weather['alerts'], )
                for measure in weather['values']:
                    if measure['temp'] and measure['wspd']:
                        weather_value = Weather(
                            datetime=measure['datetime'],
                            temp=measure['temp'],
                            wspd=measure['wspd'],
                            info=measure['info'],
                            location=location,
                        )
                        weather_values.append(weather_value)
            if not weather_values:
                message = "No weather data available for {}"
                messages.append(message.format(location.address))
                return Response({
                    'location': location,
                    'weather_metrics': weather_metrics,
                    'weather_values': weather_values,
                    'columns': columns,
                    'query': query,
                    'messages': messages
                }, status=status.HTTP_400_BAD_REQUEST)
            weather_values = WeatherSerializer(data=weather_values, many=True)
            weather_values.is_valid()
            weather_values.save()
            average_temp = sum([float(reading) for values in weather_values.data for metric, reading in values.items()
                                if metric == 'temp'])/len(weather_values.data)
            average_wspd = sum([float(reading) for values in weather_values.data for metric, reading in values.items()
                                if metric == 'wspd'])/len(weather_values.data)
            location = LocationSerializer(location)
            table_metrics = []
            for table_column in weather_values.data[0].keys():
                for metric in weather_metrics:
                    if metric.id == table_column:
                        table_metrics.append(metric)
            print(table_metrics)
            weather_metrics = MetricSerializer(data=table_metrics, many=True)
            weather_metrics.is_valid()
            weather_metrics.save()
            print(weather_metrics.data)
            return Response({
                'location': location.data,
                'weather_metrics': weather_metrics.data,
                'weather_values': weather_values.data,
                'columns': columns,
                'query': query,
                'temperature': average_temp,
                'windspeed': average_wspd,
            }, status=status.HTTP_201_CREATED)


weather_view = WeatherView.as_view()
