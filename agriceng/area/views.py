import math
import requests
from requests.exceptions import HTTPError

from django.views.generic.edit import FormView
from rest_framework.renderers import JSONRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from .models import Crop, Coefficient
from .api.serializers import CropSerializer
from .forms import AreaForm, PDFForm
from agriceng.solardryers.models import Dryer, Note
from agriceng.solardryers.api.serializers import DryerSerializer
from agriceng.weatherdata.api import serializers
from agriceng.weatherdata.viewmixins import LocationWeatherMixin


class SolarDryerView(LocationWeatherMixin, FormView):
    form_class = AreaForm, PDFForm
    template_name = 'pages/home.html'

    # Filenames for the content, header, body and footer templates.
    body_template = 'area/body.html'
    header_template = None
    footer_template = None
    cover_template = None

    # Filenames for the content, header, body and footer templates.
    extra_pdf_context = None

    # Filename for downloaded PDF. If None, the response is inline.
    filename = 'rendered_pdf.pdf'

    # Command-line options to pass to wkhtmltopdf
    cmd_options = {
        # 'orientation': 'portrait',
        # 'collate': True,
        # 'quiet': None,
    }

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form(form_class=AreaForm)
        if 'pdf_form'not in kwargs:
            kwargs['pdf_form'] = self.get_form(form_class=PDFForm)
        return kwargs

    def get_cmd_options(self):
        return self.cmd_options

    def get_filename(self):
        return self.filename

    def get_pdf_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_pdf_context is not None:
            kwargs.update(self.extra_pdf_context)
        return kwargs

    def form_invalid(self, form, pdf_form=None, solutions=None):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, solutions=solutions, pdf_form=pdf_form))

    def form_valid(self, form, **kwargs):
        """If the form is valid, render Solar Dryer Design details."""
        """Return a dictionary of solutions from the solar dryer equations"""
        solutions = {}
        # Solar dryer's location weather data
        solutions['location'] = kwargs['location']
        solutions['temp'] = kwargs['average_temp']
        solutions['wspd'] = kwargs['average_wspd']

        # Airflow Requirements
        dp = Coefficient.objects.get(coefficient='dimensionless parameter (0.14-0.25)')
        bt = Coefficient.objects.get(coefficient='boiling temp of water in degrees')
        ft = Coefficient.objects.get(coefficient='freezing temp water in degrees')
        it = Coefficient.objects.get(coefficient='intensity of radiation w/m2')
        sc = Coefficient.objects.get(coefficient='solar constant')
        temp_delta = 2*dp.equivalent*(bt.equivalent-ft.equivalent)*(it.equivalent/sc.equivalent)
        solutions['temperature_diff'] = temp_delta

        # Moisture to be removed
        mass = form.cleaned_data['mass']
        query = form.cleaned_data['location']
        crop = form.cleaned_data['crop']
        crop_obj = Crop.objects.get(name=crop)
        crop_serializer = CropSerializer(crop_obj)
        miwb = crop.initial_moisture
        mfwb = crop.final_moisture
        mw = mass*(miwb/100-mfwb/100)/(1-mfwb/100)
        solutions['crop'] = crop_serializer.data
        solutions['query'] = query
        solutions['mass'] = mass
        solutions['moisture'] = mw

        # Enthalpy of vaporization
        ra = Coefficient.objects.get(coefficient='specifc gass constant')
        rg = Coefficient.objects.get(coefficient='gass constant of water vapor')
        tb2 = Coefficient.objects.get(coefficient='boiling point of water in kelvins')
        pc = Coefficient.objects.get(coefficient='critical pressure of water')
        to_deg = kwargs['average_temp']+temp_delta
        tpt_deg = 0.25*((3*to_deg)+kwargs['average_temp'])
        tpt = tpt_deg+273
        tcr = Coefficient.objects.get(coefficient='critical temp of water in kelvins')
        lt = (rg.equivalent*tcr.equivalent*tb2.equivalent) * \
             (
                 math.log(pc.equivalent/math.pow(10, 5)) *
                 (math.pow((tcr.equivalent-tpt), 0.38)) /
                 (math.pow((tcr.equivalent-tb2.equivalent), 1.38))
             )
        solutions['enthalpy'] = "{:e}".format(lt)

        # Volume of air required
        tf_deg = kwargs['average_temp']+(0.25*temp_delta)
        tf = tf_deg+273
        ta = kwargs['average_temp']+273
        to = to_deg+273
        pa = Coefficient.objects.get(coefficient='partial pressure of dry air in atmosphere')
        cpa = Coefficient.objects.get(coefficient='specific heat capacity of air at constant pressure')
        va = (mw*lt*ra.equivalent*ta)/(cpa.equivalent*pa.equivalent*(to-tf))
        solutions['air_volume'] = va

        # Volume flow rate
        t = Coefficient.objects.get(coefficient='total drying time (24 hours)')
        p = Coefficient.objects.get(coefficient='density of air')
        vfr = va/t.equivalent
        mfr = vfr*p.equivalent
        solutions['volume_fr'] = vfr
        solutions['mass_fr'] = mfr

        # Collecting Area
        n = Coefficient.objects.get(coefficient='efficiency')
        ca = (mw*lt)/(it.equivalent*t.equivalent*n.equivalent)
        a = ca/2
        solutions['area'] = ca
        solutions['improved_area'] = a

        # Chimneys
        w = Coefficient.objects.get(coefficient='width of chimney')
        s = Coefficient.objects.get(coefficient='depth of chimney')
        vc = kwargs['average_wspd']*1000/3600
        cn = vfr/(w.equivalent*s.equivalent*vc)
        ac = cn*vc
        solutions['chimneys'] = cn
        solutions['chimney_area'] = ac

        # Drying Area
        dryers = Dryer.objects.all()
        dryers_serializer = DryerSerializer(dryers, many=True)
        m = Coefficient.objects.get(coefficient='recommended drying thickness')
        bd = crop.bulk_density
        sa = 600/(bd*m.equivalent)
        ld = mass/sa
        solutions['dryers'] = dryers_serializer.data
        solutions['surface_area'] = sa
        solutions['density'] = ld

        # Initialize PDF Generation form
        pdf_context = JSONRenderer().render(solutions)
        pdf_data = {
            'pdf-context': pdf_context,
        }

        pdf_form = PDFForm(data=pdf_data)
        return self.render_to_response(self.get_context_data(
            form=form,
            solutions=solutions,
            pdf_form=pdf_form,
        ))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        if 'generate-dryer' in request.POST:
            form = self.get_form(form_class=AreaForm)
            location = request.POST['dryer-location']
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
                    print(type(location.data['created']))
                if form.is_valid():
                    return self.form_valid(
                        form,
                        average_temp=average_temp,
                        average_wspd=average_wspd,
                        location=location.data
                    )
                else:
                    return self.form_invalid(form)

        elif 'pdf-context' in request.POST:
            pdf_form = self.get_form(form_class=PDFForm)
            if pdf_form.is_valid():
                notes = Note.objects.all()
                dryer = pdf_form.cleaned_data['solar_dryer']
                solutions = pdf_form.cleaned_data['context']
                solutions['notes'] = notes
                solutions['dryer'] = dryer
                return self.pdf_form_valid(solutions, dryer=dryer)

            else:
                solutions = pdf_form.cleaned_data['context']
                crop = solutions['crop']
                crop_name = Crop.objects.get(name=crop['name'])
                data = {
                    'dryer-crop': crop_name,
                    'dryer-location': solutions['query'],
                    'dryer-mass': solutions['mass']
                }
                form = AreaForm(data=data)
                return self.form_invalid(form, pdf_form, solutions)

    def pdf_form_valid(self, solutions, **kwargs):
        if 'dryer' in kwargs:
            filename = "{} Report.pdf".format(kwargs['dryer'])
        return self.render_pdf_response(self.get_pdf_data(solutions=solutions), filename=filename)

    def render_pdf_response(self, context, **response_kwargs):
        """
                Returns a PDF response with a template rendered with the given context.
        """
        filename = response_kwargs.pop('filename', None)
        cmd_options = response_kwargs.pop('cmd_options', None)

        if filename is None:
            filename = self.get_filename()

        if cmd_options is None:
            cmd_options = self.get_cmd_options()

        return PDFTemplateResponse(
            request=self.request,
            template=self.body_template,
            context=context,
            filename=filename,
            show_content_in_browser=None,
            header_template=None,
            footer_template=None,
            cmd_options=cmd_options,
            cover_template=None,
            using=self.template_engine,
            **response_kwargs
        )


solar_dryer_view = SolarDryerView.as_view()
