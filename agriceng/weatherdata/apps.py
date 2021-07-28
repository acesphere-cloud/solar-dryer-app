from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WeatherDataConfig(AppConfig):
    name = "agriceng.weatherdata"
    verbose_name = _("Weather Data")

    def ready(self):
        try:
            import agriceng.weatherdata.signals  # noqa F401
        except ImportError:
            pass
