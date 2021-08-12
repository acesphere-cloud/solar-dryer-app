import math
import requests
from requests.exceptions import HTTPError

from django.views.generic.edit import FormView

from .models import Crop, Coefficient
from .forms import AreaForm
from agriceng.solardryers.models import Dryer
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
        it = Coefficient.objects.get(coefficient='intensity of radiation w/m2')
        sc = Coefficient.objects.get(coefficient='solar constant')
        temp_delta = 2*dp.equivalent*(bt.equivalent-ft.equivalent)*(it.equivalent/sc.equivalent)
        airflow['temperature_diff'] = temp_delta

        # Moisture to be removed
        moisture = {}
        mass = form.cleaned_data['mass']
        crop = form.cleaned_data['crop']
        crop = Crop.objects.get(name=crop)
        miwb = crop.initial_moisture
        mfwb = crop.final_moisture
        mw = mass*(miwb/100-mfwb/100)/(1-mfwb/100)
        moisture['crop'] = crop
        moisture['mass'] = mass
        moisture['to_remove'] = mw


        # Enthalpy of vaporization
        vaporization = {}
        ra = Coefficient.objects.get(coefficient='specifc gass constant')
        rg = Coefficient.objects.get(coefficient='gass constant of water vapor')
        tb2 = Coefficient.objects.get(coefficient='boiling point of water in kelvins')
        pc = Coefficient.objects.get(coefficient='critical pressure of water')
        to_deg = average_temp+temp_delta
        tpt_deg = 0.25*((3*to_deg)+average_temp)
        tpt = tpt_deg+273
        tcr = Coefficient.objects.get(coefficient='critical temp of water in kelvins')
        lt = (rg.equivalent*tcr.equivalent*tb2.equivalent) *\
             (
                 math.log(pc.equivalent/math.pow(10, 5)) *
                 (math.pow((tcr.equivalent-tpt), 0.38)) /
                 (math.pow((tcr.equivalent-tb2.equivalent), 1.38))
             )
        vaporization['enthalpy'] = "{:e}".format(lt)

        # Volume of air required
        airvolume = {}
        tf_deg = average_temp+(0.25*temp_delta)
        tf = tf_deg+273
        ta = average_temp+273
        to = to_deg+273
        pa = Coefficient.objects.get(coefficient='partial pressure of dry air in atmosphere')
        cpa = Coefficient.objects.get(coefficient='specific heat capacity of air at constant pressure')
        va = (mw*lt*ra.equivalent*ta)/(cpa.equivalent*pa.equivalent*(to-tf))
        airvolume['required'] = va

        # Volume flow rate
        flowrate = {}
        t = Coefficient.objects.get(coefficient='total drying time (24 hours)')
        p = Coefficient.objects.get(coefficient='density of air')
        vfr = va/t.equivalent
        mfr = vfr*p.equivalent
        flowrate['volume'] = vfr
        flowrate['mass'] = mfr

        # Collecting Area
        collectorarea = {}
        n = Coefficient.objects.get(coefficient='efficiency')
        ca = (mw*lt)/(it.equivalent*t.equivalent*n.equivalent)
        a = ca/2
        collectorarea['collecting'] = ca
        collectorarea['improved_dryer'] = a

        # Chimneys
        chimneys = {}
        w = Coefficient.objects.get(coefficient='width of chimney')
        s = Coefficient.objects.get(coefficient='depth of chimney')
        vc = average_wspd*1000/3600
        cn = vfr/(w.equivalent*s.equivalent*vc)
        ac = cn*vc
        chimneys['number'] = cn
        chimneys['area'] = ac

        # Drying Area
        dryerarea = {}
        dryers = Dryer.objects.all()
        m = Coefficient.objects.get(coefficient='recommended drying thickness')
        bd = crop.bulk_density
        sa = 600/(bd*m.equivalent)
        ld = mass/sa
        dryerarea['dryers'] = dryers
        dryerarea['surface'] = sa
        dryerarea['density'] = ld

        return self.render_to_response(self.get_context_data(
            form=form,
            location=location,
            temperature=average_temp,
            wind_speed=average_wspd,
            airflow=airflow,
            moisture=moisture,
            vaporization=vaporization,
            airvolume=airvolume,
            flowrate=flowrate,
            collectorarea=collectorarea,
            chimneys=chimneys,
            dryerarea=dryerarea,
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
            form.add_error('location', message.format(err))
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
