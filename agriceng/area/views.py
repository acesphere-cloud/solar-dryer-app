import requests
from requests.exceptions import HTTPError

from django.views.generic.edit import FormView

from .models import Crop, Coefficient
from .forms import AreaForm
from agriceng.weatherdata.api import serializers
from agriceng.weatherdata.api.viewmixins import LocationWeatherMixin


class SolarDryerView(LocationWeatherMixin, FormView):
    form_class = AreaForm
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form, location, average_temp, average_wspd):
        """If the form is valid, render Solar Dryer Design details."""
        # Airflow Requirements
        airflow = {}
        dp = Coefficient.objects.get(coefficient='dimensionless parameter (0.14-0.25)')
        bt = Coefficient.objects.get(coefficient='boiling temp of water in degrees')
        ft = Coefficient.objects.get(coefficient='freezing temp water in degrees')
        ri = Coefficient.objects.get(coefficient='intensity of radiation w/m2')
        sc = Coefficient.objects.get(coefficient='solar constant')
        print("sc print: {}".format(sc.value))
        airflow['temperature_diff'] = 2*dp.value*(bt.value-ft.value)*(ri.value/sc.value)
        return self.render_to_response(self.get_context_data(
            form=form,
            location=location,
            temperature=average_temp,
            wind_speed=average_wspd,
            airflow=airflow
        ))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        location = request.POST['location']
        url = self.get_weather_url(location)
        try:
            response = requests.get(url)
            print(' - Running query URL: ', url)
            # A successful request will raise no error
            response.raise_for_status()
        except HTTPError as http_err:
            message = "HTTP error occurred: {}"
            form.add_error('location', message.format(http_err))
        except Exception as err:
            message = "An error occurred: {}"
            form.add_error(message.format(err))
        else:
            weather_data = response.json()
            if 'errorCode' in weather_data:
                message = "API Error {0}: {1}"
                form.add_error('location', message.format(weather_data['errorCode'], weather_data['message']))
            else:
                weather_values = []
                for location, weather in weather_data['locations'].items():
                    location = serializers.Location(
                        id=weather['id'],
                        address=weather['address'],
                        name=weather['name'],
                        index=weather['index'],
                        latitude=weather['latitude'],
                        longitude=weather['longitude'],
                        distance=weather['distance'],
                        time=weather['time'],
                        tz=weather['tz'],
                        conditions=weather['currentConditions'],
                        alerts=weather['alerts'],
                    )
                    for measure in weather['values']:
                        if measure['temp'] and measure['wspd']:
                            weather_value = serializers.Weather(
                            datetime=measure['datetime'],
                            temp=measure['temp'],
                            wspd=measure['wspd'],
                            info=measure['info'],
                            location=location,
                            )
                            weather_values.append(weather_value)
                if not weather_values:
                    message = "No weather data available for {}"
                    form.add_error('location', message.format(location.address))
                weather_values = serializers.WeatherSerializer(data=weather_values, many=True)
                weather_values.is_valid()
                average_temp = sum([float(reading) for values in weather_values.data for metric, reading in
                                    values.items() if metric == 'temp'])/len(weather_values.data)
                average_wspd = sum([float(reading) for values in weather_values.data for metric, reading in
                                    values.items() if metric == 'wspd'])/len(weather_values.data)
                location = serializers.LocationSerializer(location)
            if form.is_valid():
                return self.form_valid(form, location.data, average_temp, average_wspd)
            else:
                return self.form_invalid(form)


solar_dryer_view = SolarDryerView.as_view()
